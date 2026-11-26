"""Tạo bản đồ tái lập và chạy benchmark robot kho tuần tự."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from contextlib import contextmanager
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from random import Random
from tempfile import NamedTemporaryFile
from time import get_clock_info, perf_counter

from .environment import MultiPickupProblem, SingleGoalProblem, load_map
from .planning import nearest_neighbor
from .search import search

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "results"
SCHEMA_VERSION = 1
PICKUP_COUNTS = (1, 3, 5)
VARIANTS = {
    "bfs": ("bfs", None),
    "ucs": ("ucs", None),
    "greedy": ("greedy", "manhattan"),
    "astar": ("astar", "manhattan"),
    "astar_max": ("astar", "max"),
    "astar_mst": ("astar", "mst"),
    "nearest_neighbor": ("nearest_neighbor", None),
}
COMPARISONS = {
    ("single", "uniform"): ("bfs", "ucs", "greedy", "astar"),
    ("single", "weighted"): ("ucs", "greedy", "astar"),
    ("multi", "weighted"): ("ucs", "astar_max", "astar_mst", "nearest_neighbor"),
}
PROFILES = {
    "quick": {
        "single_sizes": (8, 14), "multi_sizes": (7, 10),
        "single_densities": (10, 30), "multi_densities": (10, 30),
        "seeds": (11, 29), "timeout_seconds": 0.5, "max_expanded_nodes": 12_000,
    },
    "full": {
        "single_sizes": (12, 24, 40, 64), "multi_sizes": (8, 12, 16),
        "single_densities": (10, 25, 40), "multi_densities": (10, 30),
        "seeds": (11, 29, 47, 71, 101, 137), "timeout_seconds": 2.0, "max_expanded_nodes": 50_000,
    },
}
STATUSES = ("success", "no_path", "timeout", "node_limit", "cancelled")


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)


def _digest(value) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def read_json(path: Path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, suffix=".tmp", delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(_json(value) + "\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _save_input(path: Path, value) -> None:
    if not path.exists():
        write_json(path, value)
    elif _digest(read_json(path)) != _digest(value):
        raise ValueError(f"Dữ liệu đã lưu không khớp cấu hình: {path}")


@contextmanager
def _run_lock(directory: Path):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".lock").open("a+b") as lock:
        try:
            if os.name == "nt":
                import msvcrt

                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise ValueError(f"Không lấy được khóa ghi cho {directory}: {exc}") from exc
        yield


def _environment() -> dict:
    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "system": platform.system(),
        "system_release": platform.release(),
        "machine": platform.machine(),
        "logical_cpus": os.cpu_count(),
        "perf_counter_resolution": get_clock_info("perf_counter").resolution,
    }


def _map(size: int, density: int, seed: int, cost: str, mode: str) -> dict:
    rng = Random(seed)
    start = (0, 0)
    candidates = [(r, c) for r in range(size) for c in range(size) if (r, c) != start]
    points = [(size - 1, size - 1)] if mode == "single" else rng.sample(candidates, max(PICKUP_COUNTS))
    walkable = {start, *points}
    grid = []
    for row in range(size):
        line = []
        for col in range(size):
            blocked = rng.randrange(100) < density and (row, col) not in walkable
            weight = rng.randint(1, 9)
            line.append(0 if blocked else (weight if cost == "weighted" else 1))
        grid.append(line)
    return {
        "schema_version": 1, "grid": grid, "start": start, "depot": start,
        "pickups": [{"id": f"P{i + 1}", "position": point} for i, point in enumerate(points)],
    }


def _inputs(profile: dict) -> tuple[dict, list]:
    maps, tasks = {}, []
    for (mode, cost), variants in COMPARISONS.items():
        for size in profile[f"{mode}_sizes"]:
            for density in profile[f"{mode}_densities"]:
                for seed in profile["seeds"]:
                    map_id = f"{mode}-{cost}-{size}-d{density}-s{seed}"
                    warehouse = maps[map_id] = _map(size, density, seed, cost, mode)
                    blocked = sum(cell == 0 for row in warehouse["grid"] for cell in row)
                    for count in PICKUP_COUNTS if mode == "multi" else (1,):
                        tasks.append({
                            "task_id": f"{map_id}-p{count}",
                            "map_id": map_id, "seed": seed, "mode": mode, "cost_kind": cost,
                            "size": size, "density_percent": density, "blocked_cells": blocked,
                            "pickup_ids": [p["id"] for p in warehouse["pickups"][:count]],
                            "pickup_count": count, "variants": variants,
                        })
    return maps, tasks


def _manifest(profile_name: str, maps: dict, tasks: list) -> dict:
    settings = {
        "schema_version": SCHEMA_VERSION,
        "profile": profile_name,
        "settings": PROFILES[profile_name],
        "variants": VARIANTS,
        "environment": _environment(),
        "code_sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ("benchmark.py", "environment.py", "search.py", "planning.py")
        },
        "maps_sha256": _digest(maps),
        "tasks_sha256": _digest(tasks),
    }
    return {**settings, "config_id": _digest(settings)}


def load_run(directory: Path) -> tuple[dict, list]:
    manifest = read_json(directory / "manifest.json")
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"Phiên bản dữ liệu benchmark không được hỗ trợ: {directory}")
    config_id = manifest["config_id"]
    if config_id != _digest({key: value for key, value in manifest.items() if key != "config_id"}):
        raise ValueError(f"Manifest không khớp mã cấu hình: {directory}")
    tasks = read_json(directory / "tasks.json")
    if _digest(tasks) != manifest["tasks_sha256"]:
        raise ValueError(f"Danh sách nhiệm vụ không khớp manifest: {directory}")
    return manifest, tasks


def _identity(manifest: dict, task: dict, variant: str) -> dict:
    algorithm, heuristic = manifest["variants"][variant]
    return {
        "config_id": manifest["config_id"],
        "task_id": task["task_id"],
        "map_id": task["map_id"],
        "seed": task["seed"],
        "variant": variant,
        "algorithm": algorithm,
        "heuristic": heuristic,
        "limits": {
            key: manifest["settings"][key] for key in ("timeout_seconds", "max_expanded_nodes")
        },
        "environment": manifest["environment"],
    }


def _row_path(directory: Path, task: dict, variant: str) -> Path:
    return directory / "raw" / f"{task['task_id']}__{variant}.json"


def read_attempt(directory: Path, manifest: dict, task: dict, variant: str) -> dict | None:
    path = _row_path(directory, task, variant)
    try:
        row = read_json(path)
    except FileNotFoundError:
        return None
    if any(row.get(key) != value for key, value in _identity(manifest, task, variant).items()):
        raise ValueError(f"Lần chạy không khớp cấu hình hoặc nhiệm vụ: {path}")
    if row.get("status") not in STATUSES:
        raise ValueError(f"Trạng thái không hợp lệ: {path}")
    return row


def _measure(directory: Path, identity: dict, task: dict) -> dict:
    # Nạp bản đồ riêng cho từng lượt để không chia sẻ min_enter_cost đã cache.
    warehouse = load_map(directory / "maps" / f"{task['map_id']}.json")
    algorithm = identity["algorithm"]
    limits = identity["limits"]
    started = perf_counter()

    def deadline_reached() -> bool:
        return perf_counter() - started >= limits["timeout_seconds"]

    if task["mode"] == "multi":
        pickup_ids = set(task["pickup_ids"])
        warehouse = replace(warehouse, pickups=tuple(p for p in warehouse.pickups if p.id in pickup_ids))
    options = dict(
        should_cancel=deadline_reached, max_expanded_nodes=limits["max_expanded_nodes"], on_event=None
    )
    if algorithm == "nearest_neighbor":
        result = nearest_neighbor(warehouse, **options)
    else:
        if task["mode"] == "single":
            problem = SingleGoalProblem(warehouse, task["pickup_ids"][0])
        else:
            problem = MultiPickupProblem(warehouse, identity["heuristic"] or "max")
        result = search(problem, algorithm=algorithm, **options)
    elapsed = perf_counter() - started
    # Trong benchmark, callback dừng chỉ đại diện cho đồng hồ chung của lượt chạy.
    status = "timeout" if result.status == "cancelled" else result.status
    return {
        **identity,
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "elapsed_seconds": elapsed,
        "solver_elapsed_seconds": result.elapsed_seconds,
        "total_cost": result.total_cost,
        "steps": result.steps,
        "expanded_nodes": result.expanded_nodes,
        "generated_nodes": result.generated_nodes,
        "peak_frontier_entries": result.peak_frontier_entries,
        "pickup_order": result.pickup_order,
    }


def run(profile_name: str, output_dir: Path = OUTPUT_DIR) -> Path:
    maps, tasks = _inputs(PROFILES[profile_name])
    manifest = _manifest(profile_name, maps, tasks)
    directory = output_dir / profile_name / manifest["config_id"][:20]
    expected = sum(len(task["variants"]) for task in tasks)
    completed = 0
    print(f"Profile {profile_name} · {len(maps)} bản đồ · {len(tasks)} nhiệm vụ · {expected} lần chạy")
    print(f"Thư mục {directory}")
    with _run_lock(directory):
        # Kiểm tra danh tính trước khi ghi bất kỳ bản đồ hay số liệu mới nào.
        if (directory / "manifest.json").exists():
            _save_input(directory / "manifest.json", manifest)
        _save_input(directory / "tasks.json", tasks)
        for map_id, data in maps.items():
            _save_input(directory / "maps" / f"{map_id}.json", data)
        _save_input(directory / "manifest.json", manifest)
        existing = {
            (task["task_id"], variant)
            for task in tasks for variant in task["variants"]
            if read_attempt(directory, manifest, task, variant) is not None
        }
        for index, task in enumerate(tasks):
            variants = task["variants"]
            offset = index % len(variants)
            for variant in (*variants[offset:], *variants[:offset]):
                if (task["task_id"], variant) in existing:
                    continue
                identity = _identity(manifest, task, variant)
                row = _measure(directory, identity, task)
                write_json(_row_path(directory, task, variant), row)
                completed += 1
                if completed % 50 == 0:
                    print(f"Đã ghi {completed} lần chạy mới", flush=True)
    print(f"Hoàn tất {completed} lần chạy mới, giữ {len(existing)} lần chạy đã lưu")
    return directory


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Benchmark thuật toán lập kế hoạch robot kho.")
    parser.add_argument("--profile", choices=PROFILES, default="quick")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR, help="Thư mục gốc cho các lần chạy")
    args = parser.parse_args(argv)
    try:
        run(args.profile, args.output_dir)
    except KeyboardInterrupt:
        print("Đã dừng. Chạy lại cùng lệnh để tiếp tục các mẫu chưa lưu.", file=sys.stderr)
        return 130
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
