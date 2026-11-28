"""Baseline lấy hàng theo chi phí đường đi ngắn nhất tới điểm kế tiếp."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from time import perf_counter
from typing import Literal

from .environment import Coord, MultiPickupProblem, MultiState, WarehouseMap
from .search import SearchEvent, SearchResult, SearchStatus, _validate_event_limit, _validate_limits, search


@dataclass(frozen=True)
class _Leg:
    warehouse: WarehouseMap
    initial_state: Coord
    targets: frozenset[Coord]

    def is_goal(self, state: Coord) -> bool:
        return state in self.targets

    def successors(self, state: Coord) -> Iterator[tuple[Coord, int]]:
        for position in self.warehouse.neighbors(state):
            yield position, self.warehouse.enter_cost(position)

    def heuristic(self, state: Coord) -> int:
        return 0

    def pickup_order(self, path: tuple[Coord, ...]) -> tuple[str, ...]:
        return ()


def nearest_neighbor(
    warehouse: WarehouseMap,
    *,
    timeout_seconds: float | None = None,
    max_expanded_nodes: int | None = None,
    should_cancel: Callable[[], bool] | None = None,
    on_event: Callable[[SearchEvent[MultiState]], None] | None = None,
    max_events: int = 1000,
) -> SearchResult[MultiState]:
    """Dùng một lượt UCS cho mỗi chặng và chia sẻ ngân sách giữa các chặng."""
    _validate_limits(timeout_seconds, max_expanded_nodes)
    _validate_event_limit(max_events)
    started = perf_counter()
    problem = MultiPickupProblem(warehouse)
    state = problem.initial_state
    path = [state]
    expanded = generated = peak = total_cost = 0
    emitted = 0
    interrupted: Literal["cancelled", "timeout"] | None = None

    def should_stop() -> bool:
        nonlocal interrupted
        if should_cancel is not None and should_cancel():
            interrupted = "cancelled"
        elif timeout_seconds is not None and perf_counter() - started >= timeout_seconds:
            interrupted = "timeout"
        return interrupted is not None

    def finish(status: SearchStatus) -> SearchResult[MultiState]:
        route = tuple(path) if status == "success" else ()
        pickup_order = problem.pickup_order(route) if route else ()
        elapsed = perf_counter() - started
        result = SearchResult(
            status=status,
            path=route,
            total_cost=total_cost if route else None,
            steps=len(route) - 1 if route else None,
            expanded_nodes=expanded,
            generated_nodes=generated,
            peak_frontier_entries=peak,
            elapsed_seconds=elapsed,
            pickup_order=pickup_order,
        )
        if on_event is not None:
            on_event(SearchEvent("finish", None, None, None, 0, expanded, generated, result))
        return result

    def forward(event: SearchEvent[Coord]) -> None:
        nonlocal emitted
        if on_event is None or event.state is None or event.g is None:
            return
        emitted += 1
        on_event(SearchEvent(
            event.kind,
            problem.state_at(event.state, state.collected_mask),
            total_cost + event.g,
            event.h,
            event.frontier_entries,
            expanded + event.expanded_nodes,
            generated + event.generated_nodes,
            None,
        ))

    while not should_stop():
        if problem.is_goal(state):
            return finish("success")
        targets = frozenset(problem.remaining_positions(state)) or frozenset({warehouse.depot})
        remaining_nodes = None if max_expanded_nodes is None else max_expanded_nodes - expanded
        leg = search(
            _Leg(warehouse, state.position, targets),
            algorithm="ucs",
            max_expanded_nodes=remaining_nodes,
            should_cancel=should_stop,
            on_event=forward if on_event is not None and emitted < max_events else None,
            max_events=max_events - emitted,
        )
        expanded += leg.expanded_nodes
        generated += leg.generated_nodes
        peak = max(peak, leg.peak_frontier_entries)
        if leg.status != "success":
            return finish(interrupted or leg.status)
        assert leg.total_cost is not None
        total_cost += leg.total_cost
        for position in leg.path[1:]:
            state = problem.state_at(position, state.collected_mask)
            path.append(state)
    assert interrupted is not None
    return finish(interrupted)
