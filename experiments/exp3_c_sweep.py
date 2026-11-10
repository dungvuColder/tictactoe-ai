"""E3 — Ảnh hưởng của hằng số c (UCT) và số iteration lên tỷ lệ thắng.

(a) Bàn 3×3 (k=3): MCTS(c, it) vs Random  (tỷ lệ thắng) và vs Minimax hoàn hảo (tỷ lệ không thua).
(b) Bàn 9×9 (k=5): MCTS(c, it) vs EpsGreedy(0.5) (tỷ lệ thắng).
Mỗi điểm: GAMES ván, đổi lượt đi trước giữa các ván.
"""
import sys
from common import run_matches, save

CS = [0.5, 1.0, 1.4, 2.0]
GAMES = int(sys.argv[1]) if len(sys.argv) > 1 else 100
GAMES9 = int(sys.argv[2]) if len(sys.argv) > 2 else 50

IT3 = [10, 25, 50, 100, 200, 500, 1000, 2000, 5000]
IT9 = [100, 200, 500, 1000, 2000, 5000]


def main():
    out = {"cs": CS, "it3": IT3, "it9": IT9, "games3": GAMES, "games9": GAMES9}
    matches = []
    for c in CS:
        for it in IT3:
            mc = ("mcts", {"c": c, "iterations": it})
            matches.append((f"3x3|random|{c}|{it}", ("gomoku", 3, 3), mc, ("random", {})))
            matches.append((f"3x3|perfect|{c}|{it}", ("gomoku", 3, 3), mc, ("perfect", {})))
    out["3x3"] = run_matches(matches, games=GAMES, seed=31, log="E3-3x3")
    save("e3_c_sweep.json", out)
    matches = []
    for c in CS:
        for it in IT9:
            mc = ("mcts", {"c": c, "iterations": it})
            matches.append((f"9x9|epsgreedy|{c}|{it}", ("gomoku", 9, 5), mc, ("epsgreedy", {"eps": 0.5})))
    out["9x9"] = run_matches(matches, games=GAMES9, seed=32, log="E3-9x9")
    save("e3_c_sweep.json", out)


if __name__ == "__main__":
    main()
