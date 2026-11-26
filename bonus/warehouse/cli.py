"""Chạy lập kế hoạch lấy hàng trên bản đồ kho từ dòng lệnh."""

from __future__ import annotations

import argparse
import json
import signal
import sys
from dataclasses import asdict
from pathlib import Path

from .environment import Coord, MultiPickupProblem, MultiState, SingleGoalProblem, load_map
from .planning import nearest_neighbor
from .search import ALGORITHMS, SearchResult, search


def _print_result(result: SearchResult[Coord] | SearchResult[MultiState]) -> None:
    print(f"Trạng thái: {result.status}")
    if result.path:
        positions = (state.position if isinstance(state, MultiState) else state for state in result.path)
        path = " → ".join(f"({row}, {col})" for row, col in positions)
        print(f"Thứ tự lấy hàng: {', '.join(result.pickup_order)}")
        print(f"Đường đi: {path}")
        print(f"Chi phí: {result.total_cost}")
        print(f"Số bước: {result.steps}")
    else:
        print("Chưa có đường đi để báo cáo.")
    print(f"Nút mở rộng: {result.expanded_nodes}")
    print(f"Nút sinh: {result.generated_nodes}")
    print(f"Số entry tối đa trong frontier: {result.peak_frontier_entries}")
    print(f"Thời gian tìm kiếm: {result.elapsed_seconds:.6f} giây")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Tìm đường lấy hàng trong kho, với một hoặc nhiều điểm lấy hàng.",
        epilog=(
            "BFS tối ưu số bước và bảo đảm tối ưu chi phí khi mọi bước có cùng chi phí. "
            "Greedy Best-First không bảo đảm nghiệm tối ưu."
        ),
    )
    parser.add_argument("--map", type=Path, required=True, help="Đường dẫn bản đồ JSON")
    parser.add_argument("--algorithm", choices=(*ALGORITHMS, "nearest_neighbor"), default="astar")
    parser.add_argument("--mode", choices=("single", "multi"), default="single", help="Chế độ lấy hàng")
    parser.add_argument("--heuristic", choices=("max", "mst"), help="Heuristic A* nhiều điểm, mặc định max")
    parser.add_argument("--pickup", metavar="ID", help="ID điểm lấy hàng. Mặc định là điểm đầu tiên.")
    parser.add_argument("--timeout", type=float, metavar="SECONDS", help="Giới hạn thời gian tìm kiếm")
    parser.add_argument(
        "--max-expanded-nodes", type=int, metavar="N", help="Giới hạn số lần mở rộng nút"
    )
    parser.add_argument("--json", action="store_true", help="Xuất kết quả dưới dạng JSON")
    args = parser.parse_args(argv)

    if args.mode == "multi":
        if args.algorithm not in ("ucs", "astar", "nearest_neighbor"):
            parser.error("--mode multi hỗ trợ ucs, astar và nearest_neighbor")
        if args.pickup is not None:
            parser.error("--pickup chỉ dùng với --mode single")
    elif args.heuristic is not None or args.algorithm == "nearest_neighbor":
        parser.error("--heuristic và nearest_neighbor chỉ dùng với --mode multi")

    try:
        warehouse = load_map(args.map)
        cancelled = False

        def should_cancel() -> bool:
            return cancelled

        def request_cancel(_signum, _frame) -> None:
            nonlocal cancelled
            cancelled = True

        old_handler = signal.signal(signal.SIGINT, request_cancel)
        try:
            limits = dict(
                timeout_seconds=args.timeout,
                max_expanded_nodes=args.max_expanded_nodes,
                should_cancel=should_cancel,
            )
            if args.algorithm == "nearest_neighbor":
                result = nearest_neighbor(warehouse, **limits)
            elif args.mode == "multi":
                problem = MultiPickupProblem(warehouse, args.heuristic or "max")
                result = search(problem, algorithm=args.algorithm, **limits)
            else:
                pickup_id = warehouse.pickups[0].id if args.pickup is None else args.pickup
                result = search(SingleGoalProblem(warehouse, pickup_id), algorithm=args.algorithm, **limits)
        finally:
            signal.signal(signal.SIGINT, old_handler)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False))
    else:
        _print_result(result)
    return 0 if result.status == "success" else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
