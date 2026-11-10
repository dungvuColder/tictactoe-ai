"""E4 — Thống kê tại nút gốc (W, N, W/N, UCT) và vì sao chọn nước theo N lớn nhất.

(a) Bảng W, N, W/N tại gốc cho bàn 3×3 trống và một thế cờ 3×3 có đe dọa (MCTS c=1.4).
(b) Tần suất argmax(N) != argmax(W/N) theo số iteration, và khi khác nhau thì
    nước nào là nước tối ưu lý thuyết (so với minimax).
(c) Đấu: MCTS-robust (max N) vs MCTS-max_ratio (max W/N) — cùng c, cùng iteration —
    trước Minimax hoàn hảo trên 3×3 (tỷ lệ không thua) và đối đầu trực tiếp trên 9×9.
"""
import random
import sys

from common import run_matches, save
from games.gomoku import GomokuState
from agents.baselines import make_mcts
from agents.minimax import PerfectTTTAgent

P = PerfectTTTAgent()


def table(state, it, c=1.4, seed=1):
    a = make_mcts(c=c, iterations=it, seed=seed)
    a.search(state)
    best_vals = P.optimal_moves(state)[1]
    rows = []
    for (m, W, N, q, u) in a.root_table():
        rows.append({"move": state.move_str(m), "W": W, "N": N, "W/N": q, "UCT": u,
                     "minimax": best_vals[m]})
    return rows


def all_positions():
    """Mọi thế cờ 3×3 hợp lệ, chưa kết thúc, có >= 2 nước đi."""
    seen, out, stack = set(), [], [GomokuState(3, 3)]
    while stack:
        s = stack.pop()
        k = s.key()
        if k in seen or s.is_terminal():
            continue
        seen.add(k)
        if len(s.legal_moves()) >= 2:
            out.append(s)
        for m in s.legal_moves():
            stack.append(s.play(m))
    return out


def main():
    games = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    out = {}
    s0 = GomokuState(3, 3)
    out["table_empty_1000"] = table(s0, 1000)
    out["table_empty_100"] = table(s0, 100)
    # Thế cờ: X(0,0) O(1,1) X(2,2) -> O phải đi cạnh, đi góc là thua
    s1 = GomokuState(3, 3)
    for m in (0, 5, 10):          # chỉ số bitboard với W=4: (0,0)=0, (1,1)=5, (2,2)=10
        s1 = s1.play(m)
    out["pos_tricky"] = str(s1)
    out["table_tricky_200"] = table(s1, 200)
    out["table_tricky_1000"] = table(s1, 1000)

    # (b) tần suất bất đồng giữa hai tiêu chí
    rng = random.Random(4)
    pos = all_positions()
    sample = rng.sample(pos, 400)
    freq = []
    for it in (25, 50, 100, 200, 500, 1000):
        dis = robust_ok = ratio_ok = 0
        for i, s in enumerate(sample):
            a = make_mcts(c=1.4, iterations=it, seed=1000 + i)
            root = a.search(s)
            mr, mq = a.best_child(root, "robust").move, a.best_child(root, "max_ratio").move
            best, _ = P.optimal_moves(s)
            robust_ok += mr in best
            ratio_ok += mq in best
            if mr != mq:
                dis += 1
        freq.append({"it": it, "positions": len(sample), "disagree": dis,
                     "robust_optimal": robust_ok, "ratio_optimal": ratio_ok})
        print(freq[-1], flush=True)
    out["disagreement"] = freq
    save("e4_root_stats.json", out)

    T3, T9 = ("gomoku", 3, 3), ("gomoku", 9, 5)
    matches = []
    for it in (25, 50, 100, 200):
        for fin in ("robust", "max_ratio"):
            matches.append((f"3x3|{fin}|{it}", T3, ("mcts", {"c": 1.4, "iterations": it, "final": fin}),
                            ("perfect", {})))
    for it in (200, 1000):
        matches.append((f"9x9|robust_vs_ratio|{it}", T9,
                        ("mcts", {"c": 1.4, "iterations": it, "final": "robust"}),
                        ("mcts", {"c": 1.4, "iterations": it, "final": "max_ratio"})))
    out["matches"] = run_matches(matches, games=games, seed=41, log="E4")
    save("e4_root_stats.json", out)


if __name__ == "__main__":
    main()
