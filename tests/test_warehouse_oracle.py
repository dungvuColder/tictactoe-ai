"""Đối chứng tìm kiếm bằng ma trận khoảng cách và vét cạn thứ tự lấy hàng."""

import unittest
from itertools import pairwise, permutations
from math import inf
from random import Random

from bonus.warehouse.environment import MultiPickupProblem, Pickup, SingleGoalProblem, WarehouseMap
from bonus.warehouse.planning import nearest_neighbor
from bonus.warehouse.search import search


def _manhattan(first, second):
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def _distances(grid):
    """Floyd–Warshall có hướng, xây cạnh trực tiếp từ bảng chi phí."""
    cells = [(r, c) for r, row in enumerate(grid) for c, cost in enumerate(row) if cost > 0]
    distances = {first: dict.fromkeys(cells, inf) for first in cells}
    for first in cells:
        distances[first][first] = 0
        for second in cells:
            if _manhattan(first, second) == 1:
                row, col = second
                distances[first][second] = grid[row][col]
    for via in cells:
        for first in cells:
            for second in cells:
                distances[first][second] = min(
                    distances[first][second], distances[first][via] + distances[via][second]
                )
    return distances


def _optimal_multi_cost(warehouse, distances):
    """Vét cạn thứ tự ghé, dùng khoảng cách thật cho từng cặp liên tiếp."""
    positions = [pickup.position for pickup in warehouse.pickups]
    best = inf
    for order in permutations(positions):
        route = (warehouse.start, *order, warehouse.depot)
        cost = sum(distances[first][second] for first, second in pairwise(route))
        best = min(best, cost)
    return best


def _seeded_warehouses():
    rng = Random(20261126)
    for index in range(16):
        rows, cols = rng.choice((2, 3, 4)), rng.choice((3, 4))
        cells = [(r, c) for r in range(rows) for c in range(cols)]
        grid = [[rng.randint(1, 9) for _ in range(cols)] for _ in range(rows)]
        if index % 4 == 0:
            # Tường kín, điểm lấy đầu tiên luôn ở phía đối diện.
            for row in grid:
                row[1] = 0
            start, depot = (0, 0), (rows - 1, cols - 1)
            positions = [
                depot, *rng.sample([cell for cell in cells if cell[1] != 1 and cell != depot], 2)
            ]
        else:
            start, depot = rng.sample(cells, 2)
            positions = rng.sample(cells, 1 + index % 3)
            if index % 4 == 1:
                # Lưới thông suốt và có hàng ngay tại vị trí xuất phát.
                positions = [start, *(point for point in positions if point != start)][:3]
            else:
                protected = {start, depot, *positions}
                for r, c in cells:
                    if (r, c) not in protected and rng.random() < 0.25:
                        grid[r][c] = 0
        yield WarehouseMap(
            tuple(tuple(row) for row in grid),
            start,
            depot,
            tuple(Pickup(str(i), position) for i, position in enumerate(positions)),
        )


class WarehouseOracleTests(unittest.TestCase):
    def assert_route_valid(self, warehouse, result, single=None):
        self.assertTrue(result.path)
        positions = result.path if single is not None else tuple(state.position for state in result.path)
        self.assertEqual(positions[0], warehouse.start)
        self.assertEqual(positions[-1], single.position if single is not None else warehouse.depot)
        self.assertEqual(result.steps, len(positions) - 1)
        self.assertTrue(all(_manhattan(first, second) == 1 for first, second in pairwise(positions)))

        seen = set()
        order = []
        total_cost = 0
        for index, (row, col) in enumerate(positions):
            self.assertTrue(0 <= row < len(warehouse.grid))
            self.assertTrue(0 <= col < len(warehouse.grid[row]))
            cost = warehouse.grid[row][col]
            self.assertGreater(cost, 0)
            if index:
                total_cost += cost
            if single is None:
                for bit, pickup in enumerate(warehouse.pickups):
                    if pickup.position == (row, col) and bit not in seen:
                        order.append(pickup.id)
                        seen.add(bit)
                self.assertEqual(result.path[index].collected_mask, sum(2 ** bit for bit in seen))

        self.assertEqual(result.total_cost, total_cost)
        if single is None:
            self.assertEqual(len(seen), len(warehouse.pickups))
            self.assertEqual(result.pickup_order, tuple(order))
        else:
            self.assertNotIn(single.position, positions[:-1])
            self.assertEqual(result.pickup_order, (single.id,))

    def assert_matches_oracle(self, warehouse, result, expected, single=None):
        if expected == inf:
            self.assertEqual(result.status, "no_path")
            self.assertEqual(result.path, ())
            self.assertEqual(result.pickup_order, ())
            self.assertIsNone(result.total_cost)
            self.assertIsNone(result.steps)
        else:
            self.assertEqual(result.status, "success")
            self.assert_route_valid(warehouse, result, single)
            self.assertEqual(result.total_cost, expected)

    def test_oracle_agrees_with_hand_calculated_asymmetric_costs(self):
        warehouse = WarehouseMap(
            ((3, 7, 2), (1, 1, 1)), (0, 0), (1, 0),
            (Pickup("A", (0, 2)), Pickup("B", (0, 0))),
        )
        distances = _distances(warehouse.grid)
        pickup = warehouse.pickups[0]
        # Đi vòng qua hàng dưới để đến A (5), rồi về depot qua hàng dưới (3).
        self.assertEqual(distances[warehouse.start][pickup.position], 5)
        self.assertEqual(_optimal_multi_cost(warehouse, distances), 8)
        self.assert_matches_oracle(warehouse, search(SingleGoalProblem(warehouse, "A")), 5, pickup)
        self.assert_matches_oracle(warehouse, search(MultiPickupProblem(warehouse, "mst")), 8)

    def test_seeded_maps_against_independent_optimum_and_route_checker(self):
        for index, warehouse in enumerate(_seeded_warehouses()):
            distances = _distances(warehouse.grid)
            pickup = warehouse.pickups[0]
            single_cost = distances[warehouse.start][pickup.position]
            multi_cost = _optimal_multi_cost(warehouse, distances)
            for algorithm in ("ucs", "astar"):
                with self.subTest(map=index, mode="single", algorithm=algorithm):
                    result = search(SingleGoalProblem(warehouse, pickup.id), algorithm=algorithm)
                    self.assert_matches_oracle(warehouse, result, single_cost, pickup)
            for algorithm, heuristic in (("ucs", "max"), ("astar", "max"), ("astar", "mst")):
                with self.subTest(map=index, mode="multi", algorithm=algorithm, heuristic=heuristic):
                    result = search(MultiPickupProblem(warehouse, heuristic), algorithm=algorithm)
                    self.assert_matches_oracle(warehouse, result, multi_cost)
            with self.subTest(map=index, mode="multi", algorithm="nearest_neighbor"):
                result = nearest_neighbor(warehouse)
                if multi_cost == inf:
                    self.assert_matches_oracle(warehouse, result, inf)
                else:
                    self.assertEqual(result.status, "success")
                    self.assert_route_valid(warehouse, result)
                    self.assert_nearest_legs(warehouse, distances, result)

    def assert_nearest_legs(self, warehouse, distances, result):
        remaining = {pickup.position for pickup in warehouse.pickups} - {warehouse.start}
        previous_checkpoint = warehouse.start
        leg_cost = 0
        for state in result.path[1:]:
            row, col = state.position
            leg_cost += warehouse.grid[row][col]
            if state.position in remaining:
                cheapest = min(distances[previous_checkpoint][candidate] for candidate in remaining)
                self.assertEqual(leg_cost, cheapest)
                remaining.remove(state.position)
                previous_checkpoint, leg_cost = state.position, 0
        self.assertFalse(remaining)
        self.assertEqual(leg_cost, distances[previous_checkpoint][warehouse.depot])
