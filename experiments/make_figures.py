"""Vẽ toàn bộ đồ thị từ các file results/*.json -> results/figures/*.png"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from common import RESULTS, load  # noqa: E402

FIG = os.path.join(RESULTS, "figures")
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.25, "figure.dpi": 150})
BLUES = ["#9ecae1", "#6baed6", "#2171b5", "#08306b"]       # c tăng dần -> đậm dần
GREY, ACCENT, ORANGE = "#8c8c8c", "#2171b5", "#d9822b"


def wilson(k, n, z=1.96):
    if n == 0:
        return 0, 0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p - (c - h), (c + h) - p


def fig_e3():
    d = load("e3_c_sweep.json")
    cs = d["cs"]
    # 3x3
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for ax, opp, key, title in ((axes[0], "random", "win_rate", "(a) 3×3 — tỷ lệ THẮNG trước Random"),
                                (axes[1], "perfect", "nonloss_rate", "(b) 3×3 — tỷ lệ KHÔNG THUA trước Minimax hoàn hảo")):
        for c, col in zip(cs, BLUES):
            ys = [d["3x3"][f"3x3|{opp}|{c}|{it}"][key] for it in d["it3"]]
            ax.plot(d["it3"], ys, marker="o", ms=4, color=col, label=f"c = {c}")
        ax.set_xscale("log")
        ax.set_xlabel("Số iteration MCTS mỗi nước (thang log)")
        ax.set_ylabel(key.replace("win_rate", "Tỷ lệ thắng").replace("nonloss_rate", "Tỷ lệ không thua"))
        ax.set_title(title, fontsize=10)
        ax.set_ylim((0.6, 1.01) if opp == "random" else (0, 1.03))
    axes[1].legend(loc="lower right", frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "e3_3x3_c_sweep.png"))
    plt.close(fig)
    # 9x9
    if "9x9" in d:
        fig, ax = plt.subplots(figsize=(6.5, 4))
        for j, (c, col) in enumerate(zip(cs, BLUES)):
            xs, ys, lo, hi = [], [], [], []
            for it in d["it9"]:
                r = d["9x9"][f"9x9|epsgreedy|{c}|{it}"]
                xs.append(it * (1 + 0.04 * (j - 1.5)))
                ys.append(r["win_rate"])
                a, b = wilson(r["win"], r["games"])
                lo.append(a)
                hi.append(b)
            ax.errorbar(xs, ys, yerr=[lo, hi], marker="o", ms=4, color=col, capsize=2, lw=1.6,
                        elinewidth=0.8, label=f"c = {c}")
        ax.set_xscale("log")
        ax.set_xlabel("Số iteration MCTS mỗi nước (thang log)")
        ax.set_ylabel("Tỷ lệ thắng")
        ax.set_ylim(0, 1.03)
        ax.set_title(f"Bàn 9×9, 5 quân — MCTS vs EpsGreedy(0.5), {d['games9']} ván/điểm\n(thanh lỗi: khoảng tin cậy Wilson 95%)",
                     fontsize=10)
        ax.legend(frameon=False, loc="upper left")
        fig.tight_layout()
        fig.savefig(os.path.join(FIG, "e3_9x9_c_sweep.png"))
        plt.close(fig)


def fig_e1():
    d = load("e1_nodes.json")
    rows = d["9x9"]
    depths = sorted({r["depth"] for r in rows})
    modes = [("minimax", "Minimax", GREY), ("ab", "Alpha-Beta", "#6baed6"), ("ab_ord", "Alpha-Beta + sắp thứ tự", ACCENT)]
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    w = 0.26
    for j, (m, lab, col) in enumerate(modes):
        xs, ys = [], []
        for di, dd in enumerate(depths):
            vals = [r[m]["nodes"] for r in rows if r["depth"] == dd and m in r]
            if vals:
                xs.append(di + (j - 1) * w)
                ys.append(sum(vals) / len(vals))
        bars = ax.bar(xs, ys, width=w, color=col, label=lab)
        for x, y in zip(xs, ys):
            ax.text(x, y * 1.15, f"{y:,.0f}".replace(",", "."), ha="center", fontsize=6.5, rotation=90)
    ax.set_yscale("log")
    ax.set_xticks(range(len(depths)))
    ax.set_xticklabels([f"d = {x}" for x in depths])
    ax.set_ylabel("Số nút trung bình (thang log)")
    ax.set_title("Bàn 9×9, 5 quân: số nút duyệt theo độ sâu", fontsize=10)
    ax.set_ylim(1, 1e7)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "e1_nodes_9x9.png"))
    plt.close(fig)


def fig_e2():
    d = load("e2_never_lose.json")
    ex = d["exhaustive"]
    its = sorted({r["it"] for r in ex})
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    for ro, col, lab in (("random", ACCENT, "Rollout ngẫu nhiên"), ("heuristic", ORANGE, "Rollout heuristic")):
        lossf, opt = [], []
        for it in its:
            rs = [r for r in ex if r["it"] == it and r["rollout"] == ro]
            lossf.append(sum(r["loss"] for r in rs) / sum(r["lines"] for r in rs))
            opt.append(sum(r["optimal"] for r in rs) / sum(r["decisions"] for r in rs))
        axes[0].plot(its, lossf, marker="o", ms=4, color=col, label=lab)
        axes[1].plot(its, opt, marker="o", ms=4, color=col, label=lab)
    axes[0].set_title("(a) Tỷ lệ ván THUA trên toàn bộ cây chiến lược đối thủ", fontsize=10)
    axes[0].set_ylabel("Ván thua / tổng số ván có thể")
    axes[1].set_title("(b) Tỷ lệ nước MCTS chọn trùng nước tối ưu (minimax)", fontsize=10)
    axes[1].set_ylabel("Tỷ lệ quyết định tối ưu")
    axes[1].set_ylim(0.85, 1.005)
    for ax in axes:
        ax.set_xscale("log")
        ax.set_xlabel("Số iteration MCTS mỗi nước (thang log)")
    axes[1].legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "e2_verify_3x3.png"))
    plt.close(fig)


def fig_e4():
    d = load("e4_root_stats.json")
    fr = d["disagreement"]
    its = [r["it"] for r in fr]
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    n = fr[0]["positions"]
    ax.plot(its, [r["robust_optimal"] / n for r in fr], marker="o", ms=4, color=ACCENT, label="Chọn theo N lớn nhất")
    ax.plot(its, [r["ratio_optimal"] / n for r in fr], marker="s", ms=4, color=ORANGE, label="Chọn theo W/N lớn nhất")
    ax.bar(its, [r["disagree"] / n for r in fr], width=[x * 0.3 for x in its], color=GREY, alpha=0.35,
           label="Tỷ lệ hai tiêu chí chọn khác nhau")
    ax.set_xscale("log")
    ax.set_ylim(0, 1.03)
    ax.set_xlabel("Số iteration MCTS (thang log)")
    ax.set_ylabel("Tỷ lệ trên 400 thế cờ 3×3")
    ax.set_title("Chọn nước theo N hay theo W/N: tỷ lệ chọn đúng nước tối ưu", fontsize=10)
    ax.legend(frameon=False, loc="center right", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "e4_robust_vs_ratio.png"))
    plt.close(fig)


def fig_e5():
    d = load("e5_rollout.json")
    q = d["quality"]
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    labels = ["Thế THẮNG cưỡng bức\n(nhãn đúng = 1)", "Thế THUA cưỡng bức\n(nhãn đúng = 0)"]
    w = 0.35
    for j, (k, col, lab) in enumerate((("random", GREY, "Rollout ngẫu nhiên"), ("heuristic", ACCENT, "Rollout heuristic"))):
        ys = [q[k]["mean_est_win"], q[k]["mean_est_loss"]]
        xs = [i + (j - 0.5) * w for i in range(2)]
        ax.bar(xs, ys, width=w, color=col, label=lab)
        for x, y in zip(xs, ys):
            ax.text(x, y + 0.02, f"{y:.2f}", ha="center", fontsize=8)
    ax.axhline(1, color="#444", lw=0.8, ls="--")
    ax.axhline(0, color="#444", lw=0.8)
    ax.set_xticks(range(2))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("Giá trị ước lượng trung bình\n(200 rollout / thế cờ)")
    ax.set_title(f"Độ chính xác ước lượng giá trị lá trên {d['n_positions']} thế cờ 9×9 đã biết kết quả", fontsize=10)
    ax.legend(frameon=False, loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "e5_rollout_quality.png"))
    plt.close(fig)


if __name__ == "__main__":
    for f in (fig_e3, fig_e1, fig_e2, fig_e4, fig_e5):
        try:
            f()
            print("OK", f.__name__)
        except FileNotFoundError as e:
            print("Bỏ qua", f.__name__, "(chưa có dữ liệu)", e)
