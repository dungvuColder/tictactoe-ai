"""Tìm kiếm đồ thị bằng BFS, UCS, Greedy Best-First và A*."""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from math import isfinite
from time import perf_counter
from typing import Generic, Literal, Protocol, TypeVar

S = TypeVar("S", bound=Hashable)
SearchAlgorithm = Literal["bfs", "ucs", "greedy", "astar"]
ALGORITHMS = ("bfs", "ucs", "greedy", "astar")
SearchStatus = Literal["success", "no_path", "timeout", "node_limit", "cancelled"]
EventKind = Literal["frontier_push", "expand", "finish"]


class SearchProblem(Protocol[S]):
    @property
    def initial_state(self) -> S: ...

    def is_goal(self, state: S) -> bool: ...
    def successors(self, state: S) -> Iterable[tuple[S, int]]: ...
    def heuristic(self, state: S) -> int: ...
    def pickup_order(self, path: tuple[S, ...]) -> tuple[str, ...]: ...


@dataclass(frozen=True)
class SearchResult(Generic[S]):
    status: SearchStatus
    path: tuple[S, ...]
    total_cost: int | None
    steps: int | None
    expanded_nodes: int
    generated_nodes: int
    peak_frontier_entries: int
    elapsed_seconds: float
    pickup_order: tuple[str, ...]


@dataclass(frozen=True)
class SearchEvent(Generic[S]):
    kind: EventKind
    state: S | None
    g: int | None
    h: int | None
    frontier_entries: int
    expanded_nodes: int
    generated_nodes: int
    result: SearchResult[S] | None


def _reconstruct_path(parents: dict[S, S], goal: S) -> tuple[S, ...]:
    path = [goal]
    while path[-1] in parents:
        path.append(parents[path[-1]])
    return tuple(reversed(path))


def _validate_limits(
    timeout_seconds: float | None, max_expanded_nodes: int | None
) -> None:
    if timeout_seconds is not None and (
        type(timeout_seconds) not in (int, float)
        or timeout_seconds < 0
        or (isinstance(timeout_seconds, float) and not isfinite(timeout_seconds))
    ):
        raise ValueError("timeout_seconds phải là số hữu hạn không âm")
    if max_expanded_nodes is not None and (
        type(max_expanded_nodes) is not int or max_expanded_nodes < 0
    ):
        raise ValueError("max_expanded_nodes phải là số nguyên không âm")


def _validate_event_limit(max_events: int) -> None:
    if type(max_events) is not int or max_events < 0:
        raise ValueError("max_events phải là số nguyên không âm")


def search(
    problem: SearchProblem[S],
    *,
    algorithm: SearchAlgorithm = "astar",
    timeout_seconds: float | None = None,
    max_expanded_nodes: int | None = None,
    should_cancel: Callable[[], bool] | None = None,
    on_event: Callable[[SearchEvent[S]], None] | None = None,
    max_events: int = 1000,
) -> SearchResult[S]:
    """Trả kết quả của một lượt tìm kiếm.

    max_events giới hạn tổng sự kiện trung gian. Sự kiện finish được gửi riêng.
    """
    if algorithm not in ALGORITHMS:
        raise ValueError(f"Thuật toán tìm kiếm không hợp lệ: {algorithm!r}")
    _validate_limits(timeout_seconds, max_expanded_nodes)
    _validate_event_limit(max_events)

    started = perf_counter()
    frontier: deque[tuple[int, int, S, int, int]] | list[tuple[int, int, S, int, int]]
    frontier = deque() if algorithm == "bfs" else []
    sequence = count()
    use_heuristic = algorithm in ("astar", "greedy")
    improve_cost = algorithm in ("ucs", "astar")
    best_g: dict[S, int] = {}
    parents: dict[S, S] = {}
    expanded_nodes = generated_nodes = peak_frontier_entries = emitted = 0

    def interruption() -> SearchStatus | None:
        if should_cancel is not None and should_cancel():
            return "cancelled"
        if timeout_seconds is not None and perf_counter() - started >= timeout_seconds:
            return "timeout"
        return None

    def emit(kind: EventKind, state: S, g: int, h: int) -> None:
        nonlocal emitted
        if on_event is not None and emitted < max_events:
            on_event(SearchEvent(
                kind, state, g, h, len(frontier), expanded_nodes, generated_nodes, None
            ))
            emitted += 1

    def push(state: S, g: int) -> None:
        nonlocal peak_frontier_entries
        h = problem.heuristic(state) if use_heuristic else 0
        priority = g + h if improve_cost else h
        entry = (priority, next(sequence), state, g, h)
        if isinstance(frontier, deque):
            frontier.append(entry)
        else:
            heappush(frontier, entry)
        peak_frontier_entries = max(peak_frontier_entries, len(frontier))
        if on_event is not None:
            emit("frontier_push", state, g, h)

    def finish(
        status: SearchStatus, path: tuple[S, ...] = (), cost: int | None = None
    ) -> SearchResult[S]:
        pickup_order = problem.pickup_order(path) if path else ()
        result = SearchResult(
            status=status,
            path=path,
            total_cost=cost,
            steps=len(path) - 1 if path else None,
            expanded_nodes=expanded_nodes,
            generated_nodes=generated_nodes,
            peak_frontier_entries=peak_frontier_entries,
            elapsed_seconds=perf_counter() - started,
            pickup_order=pickup_order,
        )
        if on_event is not None:
            on_event(SearchEvent(
                "finish", None, None, None, len(frontier), expanded_nodes, generated_nodes, result
            ))
        return result

    stopped = interruption()
    if stopped is not None:
        return finish(stopped)
    root = problem.initial_state
    best_g[root] = 0
    push(root, 0)

    while True:
        stopped = interruption()
        if stopped is not None:
            return finish(stopped)
        if not frontier:
            return finish("no_path")
        entry = frontier.popleft() if isinstance(frontier, deque) else heappop(frontier)
        _, _, state, g, h = entry
        if g != best_g[state]:
            continue
        if problem.is_goal(state):
            return finish("success", _reconstruct_path(parents, state), g)
        if max_expanded_nodes is not None and expanded_nodes >= max_expanded_nodes:
            return finish("node_limit")

        expanded_nodes += 1
        if on_event is not None:
            emit("expand", state, g, h)
        for successor, cost in problem.successors(state):
            generated_nodes += 1
            next_g = g + cost
            previous_g = best_g.get(successor)
            if previous_g is not None and (not improve_cost or next_g >= previous_g):
                continue
            best_g[successor] = next_g
            parents[successor] = state
            push(successor, next_g)
