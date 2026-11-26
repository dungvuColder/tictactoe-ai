import json
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from bonus.warehouse.environment import (
    MAPS_DIR,
    MultiPickupProblem,
    MultiState,
    Pickup,
    SingleGoalProblem,
    WarehouseMap,
    load_map,
)


class MapParserTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "warehouse.json"
        self.data = {
            "schema_version": 1,
            "grid": [[2, 0, 4], [1, 3, 5]],
            "start": [0, 0],
            "depot": [1, 0],
            "pickups": [{"id": "A", "position": [1, 1]}, {"id": "B", "position": [0, 2]}],
        }

    def load_data(self, data):
        self.path.write_text(json.dumps(data), encoding="utf-8")
        return load_map(self.path)

    def test_parses_weighted_rectangular_map(self):
        warehouse = self.load_data(self.data)
        self.assertEqual(warehouse.grid, ((2, 0, 4), (1, 3, 5)))
        self.assertEqual((warehouse.rows, warehouse.cols), (2, 3))
        self.assertEqual(warehouse.min_enter_cost, 1)
        self.assertEqual(warehouse.start, (0, 0))
        self.assertEqual(warehouse.depot, (1, 0))
        self.assertEqual(warehouse.pickups, (Pickup("A", (1, 1)), Pickup("B", (0, 2))))

    def test_invalid_dimensions_and_costs(self):
        cases = [
            ([], "grid"),
            ([[]], "grid[0]"),
            ([[1, 1], [1]], "grid[1] có 1 ô"),
            ([[1, 1], "bad"], "grid[1]"),
        ]
        cases.extend(([[1, value]], "grid[0][1]") for value in (-1, 1.5, True, "2"))
        for grid, message in cases:
            with self.subTest(grid=grid), self.assertRaisesRegex(ValueError, re.escape(message)):
                self.load_data({**self.data, "grid": grid})

    def test_invalid_start_and_depot_coordinates(self):
        cases = [
            ("start", [0, 3], "ngoài bản đồ"),
            ("depot", [-1, 0], "ngoài bản đồ"),
            ("depot", [0, 1], "vật cản"),
            ("start", [0, 1], "vật cản"),
            ("start", [True, 0], "hai số nguyên"),
            ("depot", [1], "hai số nguyên"),
        ]
        for field, position, message in cases:
            with self.subTest(field=field, position=position):
                with self.assertRaisesRegex(ValueError, rf"{field}.*{message}"):
                    self.load_data({**self.data, field: position})

    def test_invalid_pickup_coordinates_and_duplicates(self):
        cases = [
            ({"id": "C", "position": [0, 1]}, "position.*vật cản"),
            ({"id": "C", "position": [2, 0]}, "position.*ngoài bản đồ"),
            ({"id": "C", "position": [1, 1]}, "position.*trùng tọa độ"),
            ({"id": "A", "position": [1, 2]}, "id.*trùng ID"),
            ({"id": " ", "position": [1, 2]}, "id.*khác khoảng trắng"),
        ]
        for pickup, message in cases:
            with self.subTest(pickup=pickup):
                with self.assertRaisesRegex(ValueError, rf"pickups\[2\]\.{message}"):
                    self.load_data({**self.data, "pickups": [*self.data["pickups"], pickup]})

    def test_missing_required_fields(self):
        for field in self.data:
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, rf"bắt buộc {field}"):
                data = self.data.copy()
                del data[field]
                self.load_data(data)
        with self.assertRaisesRegex(ValueError, r"pickups\[0\].*bắt buộc position"):
            self.load_data({**self.data, "pickups": [{"id": "A"}]})

    def test_rejects_invalid_schema_objects(self):
        cases = [
            ([], "đối tượng JSON"),
            ({**self.data, "schema_version": True}, "schema_version"),
            ({**self.data, "schema_version": 2}, "schema_version"),
            ({**self.data, "name": "extra"}, "không được hỗ trợ name"),
            ({**self.data, "pickups": []}, "ít nhất một điểm"),
            ({**self.data, "pickups": [{"id": "A", "position": [1, 1], "extra": 0}]}, "extra"),
        ]
        for data, message in cases:
            with self.subTest(data=data), self.assertRaisesRegex(ValueError, message):
                self.load_data(data)

    def test_malformed_json_and_duplicate_keys_report_source(self):
        for text, message in (("{", "line 1"), ('{"grid": [], "grid": []}', "khóa JSON bị lặp")):
            with self.subTest(text=text):
                self.path.write_text(text, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, rf"warehouse\.json:.*{message}"):
                    load_map(self.path)

    def test_invalid_encoding_and_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            load_map(self.path)
        self.path.write_bytes(b"\xff")
        with self.assertRaisesRegex(ValueError, r"warehouse\.json:.*utf-8"):
            load_map(self.path)

    def test_all_sample_paths_load(self):
        for name in ("small_uniform", "detour", "weighted", "multi_pickup", "no_path"):
            with self.subTest(name=name):
                path = MAPS_DIR / f"{name}.json"
                self.assertIsInstance(load_map(path), WarehouseMap)


class WarehouseProblemTests(unittest.TestCase):
    def setUp(self):
        self.warehouse = load_map(MAPS_DIR / "multi_pickup.json")

    def test_neighbors_filter_edges_and_racks_in_direction_order(self):
        open_grid = load_map(MAPS_DIR / "small_uniform.json")
        self.assertEqual(list(open_grid.neighbors((0, 1))), [(0, 2), (1, 1), (0, 0)])
        self.assertEqual(list(self.warehouse.neighbors((1, 0))), [(0, 0), (1, 1), (2, 0)])
        self.assertEqual(list(self.warehouse.neighbors((1, 1))), [(0, 1), (1, 2), (1, 0)])
        self.assertFalse(self.warehouse.is_walkable((-1, 0)))
        self.assertFalse(self.warehouse.is_walkable((0, 2)))

    def test_step_cost_uses_destination_in_both_modes(self):
        single = SingleGoalProblem(self.warehouse, "B")
        self.assertEqual(list(single.successors((1, 0))), [((0, 0), 2), ((1, 1), 3), ((2, 0), 1)])
        multi = MultiPickupProblem(self.warehouse)
        self.assertEqual(dict(multi.successors(MultiState((1, 0), 1)))[MultiState((0, 0), 1)], 2)
        with self.assertRaisesRegex(ValueError, r"\(0, 2\)"):
            self.warehouse.enter_cost((0, 2))

    def test_single_goal_and_pickup_at_start(self):
        problem = SingleGoalProblem(self.warehouse, "B")
        self.assertFalse(problem.is_goal(problem.initial_state))
        self.assertFalse(problem.is_goal((2, 0)))
        self.assertTrue(problem.is_goal((0, 3)))
        self.assertEqual(problem.heuristic((0, 3)), 0)
        immediate = SingleGoalProblem(self.warehouse, "A")
        self.assertTrue(immediate.is_goal(immediate.initial_state))
        self.assertEqual(immediate.pickup_order((immediate.initial_state,)), ("A",))
        with self.assertRaisesRegex(ValueError, "missing"):
            SingleGoalProblem(self.warehouse, "missing")

    def test_multi_updates_mask_and_requires_return_to_depot(self):
        problem = MultiPickupProblem(self.warehouse)
        start = problem.initial_state
        self.assertEqual(start, MultiState((0, 0), 0b001))
        self.assertFalse(problem.is_goal(start))
        positions = [(1, 0), (2, 0), (1, 0), (1, 1), (1, 2), (1, 3), (0, 3),
                     (1, 3), (1, 2), (1, 1), (1, 0), (0, 0)]
        path = [start]
        for position in positions:
            state = next(state for state, _ in problem.successors(path[-1]) if state.position == position)
            path.append(state)
        self.assertEqual(path[2], MultiState((2, 0), 0b101))
        self.assertEqual(path[3], MultiState((1, 0), 0b101))
        self.assertEqual(path[7], MultiState((0, 3), 0b111))
        self.assertFalse(problem.is_goal(path[7]))
        self.assertTrue(problem.is_goal(path[-1]))
        self.assertEqual(problem.heuristic(path[-1]), 0)
        self.assertEqual(problem.pickup_order(tuple(path)), ("A", "C", "B"))

    def test_same_position_with_different_masks_is_distinct(self):
        partial = MultiState((0, 0), 0b001)
        complete = MultiState((0, 0), 0b111)
        self.assertNotEqual(partial, complete)
        self.assertEqual(len({partial, complete}), 2)


if __name__ == "__main__":
    unittest.main()
