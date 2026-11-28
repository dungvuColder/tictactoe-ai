import unittest
from collections import deque
from unittest.mock import patch

from bonus.warehouse.environment import MAPS_DIR, MultiPickupProblem, MultiState, Pickup, WarehouseMap, load_map
from bonus.warehouse.planning import nearest_neighbor
from bonus.warehouse.search import search


class _FromState(MultiPickupProblem):
    def __init__(self, warehouse, state):
        super().__init__(warehouse)
        self._state = state

    @property
    def initial_state(self):
        return self._state


def _corridor(start=(0, 0)):
    return WarehouseMap(
        ((1, 1, 1),), start, start, (Pickup("A", (0, 1)), Pickup("B", (0, 2)))
    )


class MultiSearchTests(unittest.TestCase):
    def assert_valid_route(self, warehouse, result):
        problem = MultiPickupProblem(warehouse)
        self.assertEqual(result.status, "success")
        self.assertEqual(result.path[0], problem.initial_state)
        self.assertTrue(problem.is_goal(result.path[-1]))
        self.assertEqual(result.steps, len(result.path) - 1)
        self.assertEqual(set(result.pickup_order), {pickup.id for pickup in warehouse.pickups})
        cost = 0
        for previous, state in zip(result.path, result.path[1:]):
            successors = dict(problem.successors(previous))
            self.assertIn(state, successors)
            cost += successors[state]
        self.assertEqual(result.total_cost, cost)

    def test_ucs_and_astar_agree_on_weighted_multi_pickup(self):
        warehouse = load_map(MAPS_DIR / "multi_pickup.json")
        ucs = search(MultiPickupProblem(warehouse), algorithm="ucs")
        self.assert_valid_route(warehouse, ucs)
        self.assertEqual(ucs.pickup_order[0], "A")
        for heuristic in ("max", "mst"):
            with self.subTest(heuristic=heuristic):
                astar = search(MultiPickupProblem(warehouse, heuristic), algorithm="astar")
                self.assert_valid_route(warehouse, astar)
                self.assertEqual(astar.total_cost, ucs.total_cost)

    def test_search_collects_on_entry_and_revisits_same_position_with_new_mask(self):
        warehouse = _corridor()
        problem = MultiPickupProblem(warehouse)
        result = search(problem, algorithm="ucs")
        self.assert_valid_route(warehouse, result)
        self.assertEqual(result.path, (
            MultiState((0, 0), 0b00),
            MultiState((0, 1), 0b01),
            MultiState((0, 2), 0b11),
            MultiState((0, 1), 0b11),
            MultiState((0, 0), 0b11),
        ))
        self.assertEqual(result.pickup_order, ("A", "B"))
        self.assertEqual(len(set(result.path)), len(result.path))
        baseline = nearest_neighbor(warehouse)
        self.assertEqual(baseline.path, result.path)
        self.assertEqual(baseline.pickup_order, ("A", "B"))

    def test_heuristics_are_lower_bounds_from_all_reachable_small_states(self):
        warehouse = load_map(MAPS_DIR / "multi_pickup.json")
        problem = MultiPickupProblem(warehouse)
        frontier = deque([problem.initial_state])
        seen = {problem.initial_state}
        while frontier:
            state = frontier.popleft()
            with self.subTest(state=state):
                exact = search(_FromState(warehouse, state), algorithm="ucs")
                self.assertEqual(exact.status, "success")
                for estimate in (problem.h_max(state), problem.h_mst(state)):
                    self.assertGreaterEqual(estimate, 0)
                    self.assertLessEqual(estimate, exact.total_cost)
                    if problem.is_goal(state):
                        self.assertEqual(estimate, 0)
            for successor, _ in problem.successors(state):
                if successor not in seen:
                    seen.add(successor)
                    frontier.append(successor)

    def test_heuristic_formulas_and_depot_deduplication(self):
        warehouse = WarehouseMap(
            ((2, 3, 2), (2, 2, 2)), (0, 0), (1, 2), (Pickup("A", (0, 2)), Pickup("B", (1, 0)))
        )
        problem = MultiPickupProblem(warehouse)
        self.assertEqual(problem.h_max(problem.initial_state), 4)
        self.assertEqual(problem.h_mst(problem.initial_state), 8)
        returning = MultiState((0, 0), 0b11)
        self.assertEqual(problem.h_max(returning), 6)
        self.assertEqual(problem.h_mst(returning), 6)
        done = MultiState(warehouse.depot, 0b11)
        self.assertEqual((problem.h_max(done), problem.h_mst(done)), (0, 0))

    def test_nearest_neighbor_counterexample(self):
        warehouse = load_map(MAPS_DIR / "nearest_neighbor_trap.json")
        ucs = search(MultiPickupProblem(warehouse), algorithm="ucs")
        baseline = nearest_neighbor(warehouse)
        self.assert_valid_route(warehouse, baseline)
        self.assertEqual((ucs.total_cost, baseline.total_cost), (6, 8))
        self.assertEqual(baseline.pickup_order, ("C", "A", "B"))

    def test_nearest_neighbor_prefers_actual_cost_and_records_start_pickup(self):
        warehouse = WarehouseMap(
            ((1, 9), (1, 1), (1, 1)), (0, 0), (0, 0),
            (Pickup("start", (0, 0)), Pickup("near", (0, 1)), Pickup("cheap", (2, 0))),
        )
        result = nearest_neighbor(warehouse)
        self.assert_valid_route(warehouse, result)
        self.assertEqual(result.pickup_order, ("start", "cheap", "near"))

    def test_nearest_neighbor_node_budget_and_frontier_stats(self):
        warehouse = _corridor()
        with patch("bonus.warehouse.planning.search", wraps=search) as solve:
            result = nearest_neighbor(warehouse, max_expanded_nodes=1)
        self.assertEqual(result.status, "node_limit")
        self.assertEqual(result.expanded_nodes, 1)
        self.assertEqual(result.path, ())
        self.assertEqual([call.kwargs["max_expanded_nodes"] for call in solve.call_args_list], [1, 0])

        legs = []

        def record(*args, **kwargs):
            leg = search(*args, **kwargs)
            legs.append(leg)
            return leg

        with patch("bonus.warehouse.planning.search", side_effect=record):
            result = nearest_neighbor(warehouse)
        self.assertEqual(len(legs), 3)
        self.assertEqual(result.expanded_nodes, sum(leg.expanded_nodes for leg in legs))
        self.assertEqual(result.generated_nodes, sum(leg.generated_nodes for leg in legs))
        self.assertEqual(result.peak_frontier_entries, max(leg.peak_frontier_entries for leg in legs))

    def test_nearest_neighbor_shares_wall_clock_between_legs(self):
        clock = 0

        def solve_leg(*args, **kwargs):
            nonlocal clock
            leg = search(*args, **kwargs)
            clock += 1
            return leg

        with patch("bonus.warehouse.planning.perf_counter", side_effect=lambda: clock):
            with patch("bonus.warehouse.planning.search", side_effect=solve_leg) as solve:
                result = nearest_neighbor(_corridor(), timeout_seconds=1.5)
        self.assertEqual(result.status, "timeout")
        self.assertEqual(solve.call_count, 2)
        self.assertEqual(result.elapsed_seconds, 2)
        self.assertEqual(result.path, ())

    def test_nearest_neighbor_no_path_and_cancellation(self):
        warehouse = load_map(MAPS_DIR / "no_path.json")
        self.assertEqual(nearest_neighbor(warehouse).status, "no_path")
        self.assertEqual(nearest_neighbor(warehouse, should_cancel=lambda: True).status, "cancelled")

    def test_nearest_neighbor_event_totals_and_shared_replay_limit(self):
        warehouse = _corridor()
        complete_events = []
        complete = nearest_neighbor(warehouse, on_event=complete_events.append)
        expansions = [event for event in complete_events if event.kind == "expand"]
        self.assertEqual([event.expanded_nodes for event in expansions],
                         list(range(1, complete.expanded_nodes + 1)))
        self.assertEqual(complete_events[-1].kind, "finish")
        self.assertIs(complete_events[-1].result, complete)
        limited_events = []
        limited = nearest_neighbor(warehouse, on_event=limited_events.append, max_events=2)
        self.assertEqual(limited_events[:2], complete_events[:2])
        self.assertEqual(len(limited_events), 3)
        self.assertEqual(limited.path, complete.path)
        self.assertEqual(limited.expanded_nodes, complete.expanded_nodes)


if __name__ == "__main__":
    unittest.main()
