"""Tổng hợp một lần benchmark và vẽ biểu đồ bằng Matplotlib."""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

from .benchmark import OUTPUT_DIR, PROFILES, load_run, read_attempt

LABELS = {
    "bfs": "BFS", "ucs": "UCS", "greedy": "Greedy", "astar": "A*",
    "astar_max": "A* max", "astar_mst": "A* MST", "nearest_neighbor": "Nearest-neighbor",
}
COLORS = {
    "bfs": "#426fa6", "ucs": "#58546f", "greedy": "#bb7035", "astar": "#0d8378",
    "astar_max": "#0d8378", "astar_mst": "#3169ae", "nearest_neighbor": "#bb7035",
}
CATEGORIES = (
    ("single", "uniform", "Một đích · chi phí đồng nhất"),
    ("single", "weighted", "Một đích · chi phí có trọng số"),
    ("multi", "weighted", "Nhiều điểm · chi phí có trọng số"),
)


def _variants(cases: list) -> tuple:
    return tuple(dict.fromkeys(variant for task, _ in cases for variant in task["variants"]))


def _paired(cases: list, variants: tuple) -> list:
    return [
        rows for _, rows in cases
        if all(variant in rows and rows[variant]["status"] == "success" for variant in variants)
    ] if variants else []


def _ratios(cases: list, variant: str) -> list[float]:
    values = []
    for _, rows in cases:
        reference, row = rows.get("ucs"), rows.get(variant)
        if not reference or reference["status"] != "success" or not reference["total_cost"]:
            continue
        if row and row["status"] == "success":
            values.append(row["total_cost"] / reference["total_cost"])
    return values


def collect(directory: Path, manifest: dict, tasks: list) -> list:
    cases = []
    for task in tasks:
        rows = {}
        for variant in task["variants"]:
            row = read_attempt(directory, manifest, task, variant)
            if row is not None:
                rows[variant] = row
        cases.append((task, rows))
    return cases


def _scope(manifest: dict) -> str:
    return "Quick · kiểm tra pipeline" if manifest["profile"] == "quick" else "Full"


def _groups(cases: list) -> dict:
    groups = defaultdict(list)
    for task, rows in cases:
        key = (task["mode"], task["cost_kind"], task["size"], task["density_percent"], task["pickup_count"])
        groups[key].append((task, rows))
    return groups


def _format_median(values: list, scale: int = 1) -> str:
    return f"{median(values) * scale:.3g}" if values else "—"


def summary(manifest: dict, cases: list) -> str:
    expected = sum(len(task["variants"]) for task, _ in cases)
    observed = sum(len(rows) for _, rows in cases)
    env = manifest["environment"]
    lines = [
        f"# Benchmark robot kho · {_scope(manifest)}",
        "",
        f"- Mã cấu hình `{manifest['config_id']}`.",
        f"- Python {env['python_version']} ({env['python_implementation']}) trên "
        f"{env['system']} {env['system_release']} · {env['machine']}.",
        f"- Có dữ liệu **{observed}/{expected}** lần chạy. Còn thiếu **{expected - observed}**.",
        "",
        "Tỷ lệ thành công tính trên số lần đã ghi. Vô nghiệm, timeout, giới hạn nút, hủy và "
        "thiếu dữ liệu được đếm riêng. Chi phí, thời gian và số nút là trung vị trên tập nhiệm vụ "
        "mà mọi thuật toán so sánh đều thành công trong cùng nhóm. Timeout và giới hạn nút chỉ xuất "
        "hiện trong thống kê trạng thái. Ô trống được ký hiệu bằng —.",
        "",
        "Tỷ số chi phí dùng cặp nghiệm cùng nhiệm vụ mà UCS có chi phí dương. "
        "Nghiệm UCS chi phí 0 cho tỷ số không xác định.",
    ]
    groups = _groups(cases)
    for mode, cost, title in CATEGORIES:
        lines.extend([
            "", f"## {title}", "",
            "| Cỡ | Cản danh nghĩa | Điểm | Thuật toán | Ghi/kỳ vọng | Thiếu | Thành công | Vô nghiệm | "
            "Timeout | Giới hạn nút | Hủy | n chung | Chi phí | Thời gian (ms) | Nút mở rộng | "
            "n tỷ số | Chi phí/UCS |",
            "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ])
        for (group_mode, group_cost, size, density, count), group in sorted(groups.items()):
            if (mode, cost) != (group_mode, group_cost):
                continue
            variants = _variants(group)
            paired = _paired(group, variants)
            for variant in variants:
                wanted = sum(variant in task["variants"] for task, _ in group)
                status = Counter(rows[variant]["status"] for _, rows in group if variant in rows)
                recorded = sum(status.values())
                rate = f"{status['success']}/{recorded} ({status['success'] / recorded:.0%})" if recorded else "—"
                ratios = _ratios(group, variant)
                data = [rows[variant] for rows in paired]
                lines.append(
                    f"| {size}×{size} | {density}% | {count} | {LABELS.get(variant, variant)} | "
                    f"{recorded}/{wanted} | {wanted - recorded} | {rate} | {status['no_path']} | "
                    f"{status['timeout']} | {status['node_limit']} | {status['cancelled']} | {len(paired)} | "
                    f"{_format_median([row['total_cost'] for row in data])} | "
                    f"{_format_median([row['elapsed_seconds'] for row in data], 1000)} | "
                    f"{_format_median([row['expanded_nodes'] for row in data])} | "
                    f"{len(ratios)} | {_format_median(ratios)} |"
                )
    return "\n".join(lines) + "\n"


def _select(cases: list, mode: str, cost: str) -> list:
    return [(task, rows) for task, rows in cases if (task["mode"], task["cost_kind"]) == (mode, cost)]


def _empty(axis, message: str) -> None:
    axis.text(0.5, 0.52, message, ha="center", va="center", transform=axis.transAxes, color="#475569")


def _curve(axis, cases: list, group_key: str, metric: str, scale: int, ylabel: str) -> None:
    variants = _variants(cases)
    buckets = defaultdict(list)
    for task, rows in cases:
        buckets[task[group_key]].append((task, rows))
    groups = sorted(buckets)
    paired = [_paired(buckets[value], variants) for value in groups]
    axis.set_ylabel(ylabel)
    if group_key == "size":
        axis.set_xlabel("Kích thước (ô mỗi cạnh) · n mẫu chung")
    else:
        axis.set_xlabel("Số điểm lấy hàng · n mẫu chung")
    axis.set_xticks(groups)
    axis.set_xticklabels([f"{value}\n(n={len(rows)})" for value, rows in zip(groups, paired)])
    if not any(paired):
        _empty(axis, "Không có mẫu thành công chung")
        return
    for variant in variants:
        # NaN giữ khoảng trống ở cỡ thiếu dữ liệu, tránh nối hai điểm qua cỡ đó.
        values = [
            median(row[variant][metric] for row in rows) * scale if rows else float("nan")
            for rows in paired
        ]
        axis.plot(
            groups, values, marker="o", linewidth=2, color=COLORS.get(variant),
            linestyle="--" if variant == "ucs" else "-", label=LABELS.get(variant, variant),
        )
    axis.set_ylim(bottom=0)
    axis.grid(axis="y", alpha=0.2)
    axis.legend(frameon=False, fontsize=8)


def _ratio_chart(axis, cases: list) -> None:
    variants = _variants(cases)
    series = [_ratios(cases, variant) for variant in variants]
    positions = list(range(len(variants)))
    labels = {**LABELS, "nearest_neighbor": "Nearest\nneighbor"}
    axis.set_xticks(positions)
    axis.set_xticklabels([
        f"{labels.get(variant, variant)}\n(n={len(values)})"
        for variant, values in zip(variants, series)
    ], fontsize=8)
    axis.axhline(1, color="#64748b", linestyle="--", linewidth=1)
    axis.set_ylabel("Chi phí / chi phí UCS")
    if not any(series):
        _empty(axis, "Không có cặp với UCS\nchi phí dương")
        return
    ratios = [value for values in series for value in values]
    bottom, top = min(1, min(ratios)), max(1, max(ratios))
    padding = max(0.05, 0.1 * (top - bottom))
    axis.set_ylim(max(0, bottom - padding), top + padding)
    axis.grid(axis="y", alpha=0.2)
    for position, variant, values in zip(positions, variants, series):
        if values:
            color = COLORS.get(variant, "#334155")
            offsets = [0] if len(values) == 1 else [
                -0.19 + 0.38 * index / (len(values) - 1) for index in range(len(values))
            ]
            axis.scatter([position + offset for offset in offsets], sorted(values), color=color,
                         alpha=0.5, s=20, linewidths=0)
            axis.hlines(median(values), position - 0.28, position + 0.28, color=color, linewidth=2)


def _charts(directory: Path, manifest: dict, cases: list) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        from matplotlib import pyplot as plt
    except ImportError as exc:
        raise ValueError("Cần cài Matplotlib để vẽ biểu đồ") from exc

    destination = directory / "figures"
    destination.mkdir(exist_ok=True)
    scope = _scope(manifest)
    for name, metric, scale, label in (
        ("expanded_by_size", "expanded_nodes", 1, "Nút mở rộng"),
        ("time_by_size", "elapsed_seconds", 1000, "Thời gian (ms)"),
    ):
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), constrained_layout=True)
        fig.suptitle(f"{label} theo kích thước · {scope}")
        for axis, (mode, cost, title) in zip(axes, CATEGORIES[:2]):
            axis.set_title(title)
            _curve(axis, _select(cases, mode, cost), "size", metric, scale, label)
        fig.savefig(destination / f"{name}.png", dpi=160)
        plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.4), constrained_layout=True)
    fig.suptitle(f"Tỷ số chi phí trên cặp có nghiệm UCS (vạch là trung vị) · {scope}")
    for axis, (mode, cost, title) in zip(axes, CATEGORIES):
        axis.set_title(title)
        _ratio_chart(axis, _select(cases, mode, cost))
    fig.savefig(destination / "cost_ratio_vs_ucs.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), constrained_layout=True)
    fig.suptitle(f"Chi phí tính toán theo số điểm lấy hàng · {scope}")
    multi = _select(cases, "multi", "weighted")
    _curve(axes[0], multi, "pickup_count", "expanded_nodes", 1, "Nút mở rộng")
    _curve(axes[1], multi, "pickup_count", "elapsed_seconds", 1000, "Thời gian (ms)")
    fig.savefig(destination / "multi_by_pickups.png", dpi=160)
    plt.close(fig)


def plot(directory: Path) -> dict:
    manifest, tasks = load_run(directory)
    cases = collect(directory, manifest, tasks)
    (directory / "summary.md").write_text(summary(manifest, cases), encoding="utf-8")
    _charts(directory, manifest, cases)
    return manifest


def _latest(output_dir: Path, profile: str) -> Path:
    manifests = list((output_dir / profile).glob("*/manifest.json"))
    if not manifests:
        raise ValueError(f"Chưa có dữ liệu {profile}. Chạy benchmark trước hoặc chỉ định --run-dir.")
    return max(manifests, key=lambda path: (path.stat().st_mtime_ns, path.parent.name)).parent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Vẽ biểu đồ và tổng hợp một cấu hình benchmark robot kho.")
    parser.add_argument("--profile", choices=PROFILES, default="quick", help="Profile mới nhất nếu bỏ --run-dir")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--run-dir", type=Path, help="Thư mục chứa manifest.json và kết quả cần vẽ")
    args = parser.parse_args(argv)
    try:
        directory = args.run_dir or _latest(args.output_dir, args.profile)
        manifest = plot(directory)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    print(f"Profile {manifest['profile']} · cấu hình {manifest['config_id']}")
    print(f"Bảng {directory / 'summary.md'}")
    print(f"Biểu đồ {directory / 'figures'}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
