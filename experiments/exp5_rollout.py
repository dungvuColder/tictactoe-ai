"""E5 — Rollout ngẫu nhiên vs rollout heuristic (thắng ngay > chặn ngay > ngẫu nhiên cục bộ).

(a) Chất lượng ước lượng giá trị lá: trên tập thế cờ 9×9 đã biết kết quả lý thuyết
    (Alpha-Beta độ sâu 4 chứng minh thắng/thua cưỡng bức), so sánh trung bình kết quả rollout
    với nhãn đúng: sai số MSE, độ lệch (bias), độ chính xác dấu. Đây đúng là cách người ta
    đánh giá một value network.
(b) Bàn 3×3: tỷ lệ không thua trước Minimax hoàn hảo khi ít iteration.
(c) Bàn 9×9: bảng thắng/hòa/thua của MCTS-random và MCTS-heuristic trước 4 đối thủ.
(d) Đối đầu trực tiếp heuristic vs random: cùng số iteration và cùng thời gian suy nghĩ.
"""
import random
import sys
import time

from common import run_matches, save
from games.gomoku import GomokuState
from games import gomoku_heuristics as H
from agents.baselines import EpsilonGreedyAgent
from agents.minimax import MinimaxSearch, WIN


def labelled_positions(n=80, seed=5):
    """Thế cờ 9×9 lấy từ tự đấu EpsGreedy, giữ lại các thế mà Alpha-Beta d=4 chứng minh được kết quả."""
    rng = random.Random(seed)
    res = []
    tries = 0
    while len(res) < n and tries < 5000:
        tries += 1
        s = GomokuState(9, 5)
        a, b = EpsilonGreedyAgent(0.6, rng.randrange(10 ** 9)), EpsilonGreedyAgent(0.6, rng.randrange(10 ** 9))
        stop = rng.randrange(8, 40)
        for ply in range(stop):
            if s.is_terminal():
                break
            s = s.play((a, b)[s.player].select_move(s))
        if s.is_terminal():
            continue
        S = MinimaxSearch(lambda st: H.ordered_moves(st, 1), H.evaluate, alpha_beta=True)
        m, v = S.search(s, 4)
        if abs(v) >= WIN - 100:
            res.append((s, 1.0 if v > 0 else 0.0))
    return res


def rollout_quality(positions, k=200, seed=9):
    rng = random.Random(seed)
    out = {}
    for name, fn in (("random", H.random_rollout), ("heuristic", H.heuristic_rollout)):
        se = bias = sign_ok = 0.0
        t0 = time.perf_counter()
        per = []
        for s, label in positions:
            p = s.player
            vals = []
            for _ in range(k):
                w = fn(s, rng)
                vals.append(0.5 if w == 2 else (1.0 if w == p else 0.0))
            est = sum(vals) / k
            per.append(est)
            se += (est - label) ** 2
            bias += est - label
            sign_ok += ((est > 0.5) == (label > 0.5))
        n = len(positions)
        out[name] = {"mse": se / n, "bias": bias / n, "sign_acc": sign_ok / n,
                     "us_per_rollout": 1e6 * (time.perf_counter() - t0) / (n * k),
                     "mean_est_win": sum(e for e, (_, l) in zip(per, positions) if l == 1) / max(1, sum(1 for _, l in positions if l == 1)),
                     "mean_est_loss": sum(e for e, (_, l) in zip(per, positions) if l == 0) / max(1, sum(1 for _, l in positions if l == 0))}
    return out


def main():
    games = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    out = {}
    pos = labelled_positions()
    out["n_positions"] = len(pos)
    out["n_win"] = sum(1 for _, l in pos if l == 1)
    out["quality"] = rollout_quality(pos)
    print(out["quality"], flush=True)
    save("e5_rollout.json", out)

    T3, T9 = ("gomoku", 3, 3), ("gomoku", 9, 5)
    m3 = []
    for ro in ("random", "heuristic"):
        for it in (10, 25, 50, 100, 200):
            m3.append((f"3x3|{ro}|{it}|perfect", T3, ("mcts", {"iterations": it, "rollout": ro}), ("perfect", {})))
    out["3x3"] = run_matches(m3, games=100, seed=51, log="E5-3x3")
    save("e5_rollout.json", out)

    m9 = []
    opps = {"Random": ("random", {}), "EpsGreedy(0.5)": ("epsgreedy", {"eps": 0.5}),
            "Greedy": ("greedy", {}), "AlphaBeta(d=2)": ("ab", {"depth": 2})}
    for ro in ("random", "heuristic"):
        for it in (500, 2000):
            for on, ospec in opps.items():
                m9.append((f"9x9|{ro}|{it}|{on}", T9, ("mcts", {"iterations": it, "rollout": ro}), ospec))
    # đối đầu trực tiếp
    m9.append(("9x9|h2h|iters1000", T9, ("mcts", {"iterations": 1000, "rollout": "heuristic"}),
               ("mcts", {"iterations": 1000, "rollout": "random"})))
    m9.append(("9x9|h2h|time0.2s", T9, ("mcts", {"iterations": 10 ** 9, "time_limit": 0.2, "rollout": "heuristic"}),
               ("mcts", {"iterations": 10 ** 9, "time_limit": 0.2, "rollout": "random"})))
    out["9x9"] = run_matches(m9, games=games, seed=52, log="E5-9x9")
    save("e5_rollout.json", out)


if __name__ == "__main__":
    main()
