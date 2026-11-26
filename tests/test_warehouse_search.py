import os
import subprocess
import sys
import unittest
from threading import Event

from bonus.warehouse.environment import MAPS_DIR, Pickup, SingleGoalProblem, WarehouseMap, load_map
from bonus.warehouse.search import ALGORITHMS, search


def example(name, pickup_id="A"):
    return SingleGoalProblem(load_map(MAPS_DIR / f"{name}.json"), pickup_id)


class WarehouseSearchTests(unittest.TestCase):
    def test_all_algorithms_return_valid_paths_and_costs(self):
        problem = example("detour")
        warehouse = problem.warehouse
        for algorithm in ALGORITHMS:
            with self.subTest(algorithm=algorithm):
                result = search(problem, algorithm=algorithm)
                self.assertEqual(result.status, "success")
                self.assertEqual(result.path[0], problem.initial_state)
                self.assertTrue(problem.is_goal(result.path[-1]))
                for first, second in zip(result.path, result.path[1:]):
                    self.assertIn(second, warehouse.neighbors(first))
                self.assertEqual(result.total_cost, sum(map(warehouse.enter_cost, result.path[1:])))
                self.assertEqual(result.steps, len(result.path) - 1)
                self.assertEqual(result.pickup_order, ("A",))

    def test_bfs_and_ucs_agree_on_uniform_grid(self):
        problem = example("small_uniform")
        bfs = search(problem, algorithm="bfs")
        ucs = search(problem, algorithm="ucs")
        self.assertEqual((bfs.total_cost, ucs.total_cost), (3, 3))
        self.assertEqual(bfs.steps, 3)

    def test_astar_and_ucs_agree_on_weighted_grid(self):
        problem = example("weighted")
        astar = search(problem, algorithm="astar")
        ucs = search(problem, algorithm="ucs")
        bfs = search(problem, algorithm="bfs")
        greedy = search(problem, algorithm="greedy")
        self.assertEqual((astar.total_cost, ucs.total_cost), (5, 5))
        self.assertEqual((astar.steps, bfs.steps), (5, 3))
        self.assertEqual((bfs.total_cost, greedy.total_cost), (19, 19))

    def test_manhattan_uses_global_minimum_enter_cost(self):
        warehouse = WarehouseMap(((3, 0, 8), (4, 6, 7)), (0, 0), (0, 0), (Pickup("A", (0, 2)),))
        self.assertEqual(SingleGoalProblem(warehouse, "A").heuristic((0, 0)), 6)

    def test_start_is_goal_even_with_zero_node_limit(self):
        problem = example("multi_pickup")
        for algorithm in ALGORITHMS:
            with self.subTest(algorithm=algorithm):
                result = search(problem, algorithm=algorithm, max_expanded_nodes=0)
                self.assertEqual(result.status, "success")
                self.assertEqual(result.path, (problem.initial_state,))
                self.assertEqual((result.total_cost, result.steps), (0, 0))
                self.assertEqual((result.expanded_nodes, result.generated_nodes), (0, 0))
                self.assertEqual(result.peak_frontier_entries, 1)

    def test_no_path_counts_repeated_successors(self):
        problem = example("no_path")
        for algorithm in ALGORITHMS:
            with self.subTest(algorithm=algorithm):
                result = search(problem, algorithm=algorithm)
                self.assertEqual(result.status, "no_path")
                self.assertEqual((result.expanded_nodes, result.generated_nodes), (2, 2))
                self.assertEqual(result.peak_frontier_entries, 1)
                self.assertEqual(result.path, ())
                self.assertIsNone(result.total_cost)
                self.assertIsNone(result.steps)
                self.assertEqual(result.pickup_order, ())

    def test_timeout_node_limit_and_cancellation_have_distinct_statuses(self):
        problem = example("weighted")
        cancel = Event()
        cancel.set()
        for algorithm in ALGORITHMS:
            with self.subTest(algorithm=algorithm):
                timeout = search(problem, algorithm=algorithm, timeout_seconds=0)
                limited = search(problem, algorithm=algorithm, max_expanded_nodes=1)
                cancelled = search(problem, algorithm=algorithm, should_cancel=cancel.is_set)
                self.assertEqual(timeout.status, "timeout")
                self.assertEqual(timeout.peak_frontier_entries, 0)
                self.assertEqual(limited.status, "node_limit")
                self.assertEqual(limited.expanded_nodes, 1)
                self.assertEqual(cancelled.status, "cancelled")
                for result in (timeout, limited, cancelled):
                    self.assertEqual(result.path, ())
                    self.assertIsNone(result.total_cost)

    def test_event_budget_and_cancellation_after_expansion(self):
        problem = example("weighted")
        cancel = Event()
        events = []

        def record(event):
            events.append(event)
            if event.kind == "expand":
                cancel.set()

        result = search(problem, on_event=record, max_events=2, should_cancel=cancel.is_set)
        self.assertEqual([event.kind for event in events], ["frontier_push", "expand", "finish"])
        self.assertEqual(result.status, "cancelled")
        self.assertEqual(result.expanded_nodes, 1)
        self.assertIs(events[-1].result, result)
        events.clear()
        search(problem, on_event=events.append, max_events=0)
        self.assertEqual([event.kind for event in events], ["finish"])


class Graph:
    initial_state = "start"

    def __init__(self, edges, heuristics=None):
        self.edges = edges
        self.heuristics = heuristics or {}

    def is_goal(self, state):
        return state == "goal"

    def successors(self, state):
        return self.edges.get(state, ())

    def heuristic(self, state):
        return self.heuristics.get(state, 0)

    def pickup_order(self, path):
        return ()


class GraphSearchTests(unittest.TestCase):
    def test_astar_reopens_an_expanded_state_with_better_g(self):
        graph = Graph(
            {"start": (("a", 5), ("b", 1)), "a": (("goal", 10),), "b": (("a", 1),)},
            {"b": 10},
        )
        events = []
        result = search(graph, algorithm="astar", on_event=events.append)
        self.assertEqual(result.path, ("start", "b", "a", "goal"))
        self.assertEqual(result.total_cost, 12)
        self.assertEqual([event.state for event in events if event.kind == "expand"],
                         ["start", "a", "b", "a"])

    def test_cost_search_ignores_stale_entries(self):
        graph = Graph(
            {"start": (("x", 9), ("y", 1)), "y": (("x", 1),), "x": (("start", 1),)}
        )
        for algorithm in ("ucs", "astar"):
            with self.subTest(algorithm=algorithm):
                result = search(graph, algorithm=algorithm, max_expanded_nodes=3)
                self.assertEqual(result.status, "no_path")
                self.assertEqual((result.expanded_nodes, result.generated_nodes), (3, 4))
                self.assertEqual(result.peak_frontier_entries, 2)

    def test_goal_must_be_popped_before_search_succeeds(self):
        graph = Graph({"start": (("goal", 9), ("x", 1)), "x": (("goal", 1),)})
        for algorithm in ("ucs", "astar"):
            with self.subTest(algorithm=algorithm):
                self.assertEqual(search(graph, algorithm=algorithm).total_cost, 2)
        self.assertEqual(search(graph, algorithm="bfs", max_expanded_nodes=1).total_cost, 9)


class WarehouseCLITests(unittest.TestCase):
    def test_text_help_and_errors_use_utf8_even_with_legacy_stdio(self):
        env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
        command = [sys.executable, "-m", "bonus.warehouse.cli"]
        arguments = ["--map", "bonus/warehouse/maps/weighted.json", "--mode", "single"]
        cases = [
            (["--help"], 0, "Tìm đường", "stdout"),
            (arguments, 0, "Trạng thái: success", "stdout"),
            ([*arguments, "--pickup", "absent"], 2, "Không có điểm lấy hàng", "stderr"),
        ]
        for args, status, message, stream in cases:
            with self.subTest(args=args):
                run = subprocess.run([*command, *args], capture_output=True, env=env)
                self.assertEqual(run.returncode, status)
                self.assertIn(message, getattr(run, stream).decode("utf-8"))


if __name__ == "__main__":
    unittest.main()
