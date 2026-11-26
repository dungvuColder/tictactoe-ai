"""Bản đồ kho và các bài toán di chuyển trên lưới."""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Literal

Coord = tuple[int, int]
MultiHeuristic = Literal["max", "mst"]
MAPS_DIR = Path(__file__).resolve().with_name("maps")
_DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


@dataclass(frozen=True)
class Pickup:
    id: str
    position: Coord


@dataclass(frozen=True)
class WarehouseMap:
    grid: tuple[tuple[int, ...], ...]
    start: Coord
    depot: Coord
    pickups: tuple[Pickup, ...]

    @property
    def rows(self) -> int:
        return len(self.grid)

    @property
    def cols(self) -> int:
        return len(self.grid[0])

    @cached_property
    def min_enter_cost(self) -> int:
        return min(cost for row in self.grid for cost in row if cost > 0)

    def is_walkable(self, position: Coord) -> bool:
        row, col = position
        return 0 <= row < self.rows and 0 <= col < self.cols and self.grid[row][col] > 0

    def enter_cost(self, position: Coord) -> int:
        if not self.is_walkable(position):
            raise ValueError(f"Ô {position} nằm ngoài bản đồ hoặc là vật cản")
        row, col = position
        return self.grid[row][col]

    def neighbors(self, position: Coord) -> Iterator[Coord]:
        """Sinh các ô đi được theo thứ tự lên, phải, xuống, trái."""
        row, col = position
        for dr, dc in _DIRECTIONS:
            neighbor = (row + dr, col + dc)
            if self.is_walkable(neighbor):
                yield neighbor


def _unique_object(items: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"khóa JSON bị lặp {key!r}")
        result[key] = value
    return result


def _check_fields(value: object, fields: tuple[str, ...], label: str) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{label} phải là một đối tượng JSON")
    missing = [field for field in fields if field not in value]
    if missing:
        raise ValueError(f"{label} thiếu trường bắt buộc {', '.join(missing)}")
    unknown = sorted(value.keys() - set(fields))
    if unknown:
        raise ValueError(f"{label} có trường không được hỗ trợ {', '.join(unknown)}")


def _parse_grid(value: object) -> tuple[tuple[int, ...], ...]:
    if not isinstance(value, list) or not value:
        raise ValueError("grid phải là mảng có ít nhất một hàng")
    grid = []
    for index, row in enumerate(value):
        if not isinstance(row, list) or not row:
            raise ValueError(f"grid[{index}] phải là mảng có ít nhất một ô")
        if grid and len(row) != len(grid[0]):
            raise ValueError(f"grid[{index}] có {len(row)} ô, cần {len(grid[0])} ô")
        for col, cost in enumerate(row):
            if type(cost) is not int or cost < 0:
                raise ValueError(
                    f"grid[{index}][{col}] phải là 0 (kệ) hoặc số nguyên dương, nhận {cost!r}"
                )
        grid.append(tuple(row))
    return tuple(grid)


def _parse_position(
    value: object, grid: tuple[tuple[int, ...], ...], label: str
) -> Coord:
    if not isinstance(value, list) or len(value) != 2 or any(type(i) is not int for i in value):
        raise ValueError(f"{label} phải là mảng [hàng, cột] gồm hai số nguyên, nhận {value!r}")
    row, col = value
    if not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
        raise ValueError(f"{label} {value} nằm ngoài bản đồ")
    if grid[row][col] == 0:
        raise ValueError(f"{label} {value} nằm trên vật cản")
    return row, col


def _parse_pickups(
    value: object, grid: tuple[tuple[int, ...], ...]
) -> tuple[Pickup, ...]:
    if not isinstance(value, list) or not value:
        raise ValueError("pickups phải là mảng có ít nhất một điểm lấy hàng")
    pickups = []
    ids = set()
    positions = {}
    for index, item in enumerate(value):
        label = f"pickups[{index}]"
        _check_fields(item, ("id", "position"), label)
        pickup_id = item["id"]
        if not isinstance(pickup_id, str) or not pickup_id.strip():
            raise ValueError(f"{label}.id phải là chuỗi có ít nhất một ký tự khác khoảng trắng")
        if pickup_id in ids:
            raise ValueError(f"{label}.id trùng ID {pickup_id!r}")
        position = _parse_position(item["position"], grid, f"{label}.position")
        if position in positions:
            raise ValueError(
                f"{label}.position {position} trùng tọa độ của điểm {positions[position]!r}"
            )
        pickups.append(Pickup(pickup_id, position))
        ids.add(pickup_id)
        positions[position] = pickup_id
    return tuple(pickups)


def load_map(path: str | Path) -> WarehouseMap:
    """Đọc bản đồ JSON UTF-8 và kiểm tra schema phiên bản 1."""
    source = Path(path)
    try:
        data = json.loads(source.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
        _check_fields(data, ("schema_version", "grid", "start", "depot", "pickups"), "bản đồ")
        version = data["schema_version"]
        if type(version) is not int or version != 1:
            raise ValueError(f"schema_version phải là số nguyên 1, nhận {version!r}")
        grid = _parse_grid(data["grid"])
        start = _parse_position(data["start"], grid, "start")
        depot = _parse_position(data["depot"], grid, "depot")
        pickups = _parse_pickups(data["pickups"], grid)
    except ValueError as exc:
        raise ValueError(f"{source}: {exc}") from exc
    return WarehouseMap(grid, start, depot, pickups)


@dataclass(frozen=True)
class MultiState:
    position: Coord
    collected_mask: int


def _manhattan(first: Coord, second: Coord) -> int:
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


class SingleGoalProblem:
    def __init__(self, warehouse: WarehouseMap, pickup_id: str) -> None:
        self.warehouse = warehouse
        for pickup in warehouse.pickups:
            if pickup.id == pickup_id:
                self._pickup = pickup
                break
        else:
            raise ValueError(f"Không có điểm lấy hàng với ID {pickup_id!r}")

    @property
    def initial_state(self) -> Coord:
        return self.warehouse.start

    def is_goal(self, state: Coord) -> bool:
        return state == self._pickup.position

    def successors(self, state: Coord) -> Iterator[tuple[Coord, int]]:
        for position in self.warehouse.neighbors(state):
            yield position, self.warehouse.enter_cost(position)

    def heuristic(self, state: Coord) -> int:
        return self.warehouse.min_enter_cost * _manhattan(state, self._pickup.position)

    def pickup_order(self, path: tuple[Coord, ...]) -> tuple[str, ...]:
        return (self._pickup.id,)


class MultiPickupProblem:
    def __init__(self, warehouse: WarehouseMap, heuristic: MultiHeuristic = "max") -> None:
        if heuristic not in ("max", "mst"):
            raise ValueError(f"Heuristic nhiều điểm không hợp lệ: {heuristic!r}")
        self.warehouse = warehouse
        self._heuristic = heuristic
        self._bits_by_position = {
            pickup.position: 1 << index for index, pickup in enumerate(warehouse.pickups)
        }
        self._all_mask = (1 << len(warehouse.pickups)) - 1

    @property
    def initial_state(self) -> MultiState:
        return self.state_at(self.warehouse.start)

    def state_at(self, position: Coord, collected_mask: int = 0) -> MultiState:
        return MultiState(position, collected_mask | self._bits_by_position.get(position, 0))

    def remaining_positions(self, state: MultiState) -> Iterator[Coord]:
        for position, bit in self._bits_by_position.items():
            if not state.collected_mask & bit:
                yield position

    def is_goal(self, state: MultiState) -> bool:
        return state.position == self.warehouse.depot and state.collected_mask == self._all_mask

    def successors(self, state: MultiState) -> Iterator[tuple[MultiState, int]]:
        for position in self.warehouse.neighbors(state.position):
            yield self.state_at(position, state.collected_mask), self.warehouse.enter_cost(position)

    def heuristic(self, state: MultiState) -> int:
        return self.h_mst(state) if self._heuristic == "mst" else self.h_max(state)

    def h_max(self, state: MultiState) -> int:
        steps = max(
            (_manhattan(state.position, position) for position in self.remaining_positions(state)),
            default=_manhattan(state.position, self.warehouse.depot),
        )
        return self.warehouse.min_enter_cost * steps

    def h_mst(self, state: MultiState) -> int:
        root = state.position
        points = set(self.remaining_positions(state))
        points.add(self.warehouse.depot)
        points.discard(root)
        # Prim trên đồ thị đầy đủ. Nhân hệ số chung sau khi tìm cây.
        distances = {position: _manhattan(root, position) for position in sorted(points)}
        steps = 0
        while distances:
            closest = min(distances, key=distances.__getitem__)
            steps += distances.pop(closest)
            for position, distance in distances.items():
                distances[position] = min(distance, _manhattan(closest, position))
        return self.warehouse.min_enter_cost * steps

    def pickup_order(self, path: tuple[MultiState, ...]) -> tuple[str, ...]:
        order = []
        seen = 0
        for state in path:
            new_bits = state.collected_mask & ~seen
            while new_bits:
                bit = new_bits & -new_bits
                order.append(self.warehouse.pickups[bit.bit_length() - 1].id)
                new_bits ^= bit
            seen |= state.collected_mask
        return tuple(order)
