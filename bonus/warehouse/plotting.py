"""Tổng hợp một lần benchmark và vẽ biểu đồ bằng Matplotlib."""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import median, quantiles

from .benchmark import OUTPUT_DIR, PROFILES, STATUSES, load_run, read_attempt, repeat_count

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
DETERMINISTIC_FIELDS = (
    "total_cost", "steps", "expanded_nodes", "generated_nodes", "peak_frontier_entries", "pickup_order",
)


@dataclass(frozen=True)
class TaskStats:
    expected: int
    counts: Counter
    median_seconds: float | None
    quartiles: tuple[float, float] | None
    inconsistent: tuple[str, ...]
    representative: dict | None
    sessions: frozenset[str]

    @property
    def recorded(self) -> int:
        return sum(self.counts.values())

    @property
    def mixed_timeout(self) -> bool:
        return bool(self.counts["timeout"] and len(self.counts) > 1)

    @property
    def comparable(self) -> bool:
        return self.counts["success"] == self.expected and self.representative is not None


def _quartiles(times: list) -> tuple[float, float] | None:
    if len(times) < 3:
        return None
    q1, _, q3 = quantiles(times, n=4, method="inclusive")
    return q1, q3


def _task_stats(attempts: list, expected: int) -> TaskStats:
    successes = [row for row in attempts if row["status"] == "success"]
    times = [row["elapsed_seconds"] for row in successes]
    inconsistent = tuple(
        key for key in DETERMINISTIC_FIELDS
        if successes and any(row[key] != successes[0][key] for row in successes[1:])
    )
    middle = median(times) if times else None
    representative = {**successes[0], "elapsed_seconds": middle} if successes and not inconsistent else None
    return TaskStats(
        expected, Counter(row["status"] for row in attempts), middle, _quartiles(times), inconsistent,
        representative, frozenset(row["session_id"] for row in attempts if "session_id" in row),
    )


def _variants(cases: list) -> tuple:
    return tuple(dict.fromkeys(variant for task, _ in cases for variant in task["variants"]))


def _paired(cases: list, variants: tuple) -> list:
    return [
        {variant: rows[variant].representative for variant in variants}
        for _, rows in cases
        if all(variant in rows and rows[variant].comparable for variant in variants)
    ] if variants else []


def _ratios(cases: list, variant: str) -> list[float]:
    values = []
    for _, rows in cases:
        reference, row = rows.get("ucs"), rows.get(variant)
        if not reference or not reference.comparable or reference.representative["total_cost"] <= 0:
            continue
        if row and row.comparable:
            values.append(row.representative["total_cost"] / reference.representative["total_cost"])
    return values


def collect(directory: Path, manifest: dict, tasks: list) -> list:
    cases = []
    expected = repeat_count(manifest)
    for task in tasks:
        rows = {}
        for variant in task["variants"]:
            attempts = []
            for index in range(1, expected + 1):
                row = read_attempt(directory, manifest, task, variant, index)
                if row is not None:
                    attempts.append(row)
            rows[variant] = _task_stats(attempts, expected)
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
    return f"{median(values) * scale:.4g}" if values else "—"


def _format_interval(bounds: tuple | None, scale: int = 1) -> str:
    return f"{bounds[0] * scale:.4g}–{bounds[1] * scale:.4g}" if bounds is not None else "không có"


def _time_ratios(paired: list, variant: str) -> list[float]:
    return [
        rows[variant]["elapsed_seconds"] / rows["ucs"]["elapsed_seconds"]
        for rows in paired if "ucs" in rows and rows["ucs"]["elapsed_seconds"] > 0
    ]


def summary(manifest: dict, cases: list) -> str:
    repeats = repeat_count(manifest)
    expected = repeats * sum(len(task["variants"]) for task, _ in cases)
    all_stats = [stats for _, rows in cases for stats in rows.values()]
    observed = sum(stats.recorded for stats in all_stats)
    sessions = {session for stats in all_stats for session in stats.sessions}
    env = manifest["environment"]
    lines = [
        f"# Benchmark robot kho · {_scope(manifest)}",
        "",
        f"- Mã cấu hình `{manifest['config_id']}`.",
        f"- Python {env['python_version']} ({env['python_implementation']}) trên "
        f"{env['system']} {env['system_release']} · {env['machine']}.",
        f"- **{len(cases)} nhiệm vụ**, {repeats} lượt đo chính thức mỗi biến thể, schema {manifest['schema_version']}.",
        f"- Có dữ liệu **{observed}/{expected}** lần chạy. Còn thiếu **{expected - observed}**.",
        f"- Số phiên có bản ghi {len(sessions) if manifest['schema_version'] != 1 else 'không có thông tin'}.",
        f"- Cặp nhiệm vụ–thuật toán có kết quả success lệch {sum(bool(s.inconsistent) for s in all_stats)}. "
        f"Có timeout xen trạng thái khác {sum(s.mixed_timeout for s in all_stats)}.",
        "",
        "Tỷ lệ thành công tính trên số lượt đã ghi. Tập chung chỉ gồm nhiệm vụ mà mọi thuật toán trong nhóm "
        "có đủ lượt success và kết quả xác định nhất quán. Mỗi nhiệm vụ đóng góp một trung vị thời gian "
        "và một giá trị chi phí, số nút. Q1–Q3 trong bảng nhóm đo phân tán **giữa các nhiệm vụ**, "
        "không phải khoảng tin cậy. Xem [chi tiết đo lặp](repeat_details.md) để biết biến thiên "
        "trong cùng nhiệm vụ và các trạng thái hỗn hợp.",
        "",
        "Tỷ số thời gian dùng trung vị thời gian của từng cặp trong tập chung. "
        "Tỷ số chi phí dùng mỗi cặp có đủ nghiệm nhất quán và UCS với chi phí dương.",
    ]
    groups = _groups(cases)
    for mode, cost, title in CATEGORIES:
        lines.extend([
            "", f"## {title}", "",
            "| Cỡ | Cản danh nghĩa | Điểm | Thuật toán | Ghi/kỳ vọng | Thiếu | Thành công | Vô nghiệm | "
            "Timeout | Giới hạn nút | Hủy | n chung | n loại | Chi phí | Thời gian (ms) | Q1–Q3 (ms) | "
            "Thời gian/UCS | Nút mở rộng | n tỷ số chi phí | Chi phí/UCS |",
            "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ])
        for (group_mode, group_cost, size, density, count), group in sorted(groups.items()):
            if (mode, cost) != (group_mode, group_cost):
                continue
            variants = _variants(group)
            paired = _paired(group, variants)
            for variant in variants:
                wanted = repeats * sum(variant in task["variants"] for task, _ in group)
                status = Counter()
                for _, rows in group:
                    if variant in rows:
                        status.update(rows[variant].counts)
                recorded = sum(status.values())
                rate = f"{status['success']}/{recorded} ({status['success'] / recorded:.0%})" if recorded else "—"
                ratios = _ratios(group, variant)
                data = [rows[variant] for rows in paired]
                times = [row["elapsed_seconds"] for row in data]
                lines.append(
                    f"| {size}×{size} | {density}% | {count} | {LABELS.get(variant, variant)} | "
                    f"{recorded}/{wanted} | {wanted - recorded} | {rate} | {status['no_path']} | "
                    f"{status['timeout']} | {status['node_limit']} | {status['cancelled']} | "
                    f"{len(paired)} | {len(group) - len(paired)} | "
                    f"{_format_median([row['total_cost'] for row in data])} | "
                    f"{_format_median(times, 1000)} | {_format_interval(_quartiles(times), 1000)} | "
                    f"{_format_median(_time_ratios(paired, variant))} | "
                    f"{_format_median([row['expanded_nodes'] for row in data])} | "
                    f"{len(ratios)} | {_format_median(ratios)} |"
                )
    return "\n".join(lines) + "\n"


def repeat_details(cases: list) -> str:
    lines = [
        "# Độ dao động trong cùng nhiệm vụ",
        "",
        "Thống kê thời gian chỉ dùng các lượt success của từng biến thể. Q1, Q3 và IQR được tính bằng "
        "nội suy phân vị khi có ít nhất ba lượt success. Schema cũ có một lượt nên độ phân tán không có.",
        "",
        "| Nhiệm vụ | Thuật toán | Ghi/kỳ vọng | Success | No path | Timeout | Giới hạn nút | Hủy | "
        "Trung vị (ms) | Q1 (ms) | Q3 (ms) | IQR (ms) | Ghi chú |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for task, rows in cases:
        for variant, stats in rows.items():
            timings = (stats.median_seconds, None, None, None)
            if stats.quartiles is not None:
                q1, q3 = stats.quartiles
                timings = (stats.median_seconds, q1, q3, q3 - q1)
            notes = []
            if stats.inconsistent:
                notes.append("Success lệch " + ", ".join(stats.inconsistent))
            if stats.mixed_timeout:
                notes.append("Timeout xen trạng thái khác")
            elif len(stats.counts) > 1:
                notes.append("Trạng thái hỗn hợp")
            fields = [
                task["task_id"], LABELS.get(variant, variant), f"{stats.recorded}/{stats.expected}",
                *(str(stats.counts[status]) for status in STATUSES),
                *(f"{seconds * 1000:.4g}" if seconds is not None else "không có" for seconds in timings),
                ". ".join(notes) or "—",
            ]
            lines.append("| " + " | ".join(fields) + " |")
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
    axis.set_xticklabels([
        f"{value}\n(n={len(rows)}/{len(buckets[value])})" for value, rows in zip(groups, paired)
    ])
    if not any(paired):
        _empty(axis, "Không có mẫu thành công chung")
        return
    for variant in variants:
        # NaN giữ khoảng trống ở cỡ thiếu dữ liệu, tránh nối hai điểm qua cỡ đó.
        samples = [[row[variant][metric] * scale for row in rows] for rows in paired]
        values = [median(sample) if sample else float("nan") for sample in samples]
        color = COLORS.get(variant)
        axis.plot(
            groups, values, marker="o", linewidth=2, color=color,
            linestyle="--" if variant == "ucs" else "-", label=LABELS.get(variant, variant),
        )
        if metric == "elapsed_seconds":
            for x, middle, sample in zip(groups, values, samples):
                interval = _quartiles(sample)
                if interval is not None:
                    q1, q3 = interval
                    axis.errorbar(x, middle, yerr=[[middle - q1], [q3 - middle]],
                                  color=color, capsize=3, fmt="none", alpha=0.45)
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
        title = f"{label} theo kích thước · {scope}"
        if metric == "elapsed_seconds":
            title += (
                "\nĐường trung vị của các trung vị nhiệm vụ · Thanh Q1–Q3 giữa nhiệm vụ"
                "\nThanh phân tán không phải khoảng tin cậy"
            )
        fig.suptitle(title)
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
    axes[1].set_title("Đường trung vị của các trung vị nhiệm vụ\n"
                      "Thanh Q1–Q3 giữa nhiệm vụ, không phải khoảng tin cậy", fontsize=9)
    fig.savefig(destination / "multi_by_pickups.png", dpi=160)
    plt.close(fig)


def _report_directory(directory: Path, manifest: dict) -> Path:
    if manifest["schema_version"] == 1:
        directory = directory.resolve()
        return directory.with_name(f"{directory.name}-analysis-v2")
    return directory


def plot(directory: Path) -> dict:
    manifest, tasks = load_run(directory)
    cases = collect(directory, manifest, tasks)
    destination = _report_directory(directory, manifest)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "summary.md").write_text(summary(manifest, cases), encoding="utf-8")
    (destination / "repeat_details.md").write_text(repeat_details(cases), encoding="utf-8")
    _charts(destination, manifest, cases)
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
    destination = _report_directory(directory, manifest)
    print(f"Bảng {destination / 'summary.md'}")
    print(f"Chi tiết {destination / 'repeat_details.md'}")
    print(f"Biểu đồ {destination / 'figures'}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
