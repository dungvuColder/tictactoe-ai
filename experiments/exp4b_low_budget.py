"""E4b — N vs W/N khi ngân sách thấp so với hệ số nhánh (bàn 9×9: ~25 nước ứng viên ở gốc).

(a) Đối đầu trực tiếp MCTS-robust (max N) vs MCTS-max_ratio (max W/N), cùng c=1.4, cùng iteration.
(b) Trên các thế cờ 9×9 giữa ván: tỷ lệ nước được chọn theo W/N có N <= 2, và chất lượng nước
    (điểm Alpha-Beta d=2 của nước được chọn so với nước tốt nhất).
"""
import random
from common import run_matches, save
from games.gomoku import GomokuState
from games import gomoku_heuristics as H
from agents.baselines import make_mcts, EpsilonGreedyAgent
from agents.minimax import MinimaxSearch


def positions(n=150, seed=11):
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        s = GomokuState(9, 5)
        a = EpsilonGreedyAgent(0.6, rng.randrange(10 ** 9))
        for _ in range(rng.randrange(6, 20)):
            if s.is_terminal():
                break
            s = s.play(a.select_move(s))
        R = s.rules
        if not s.is_terminal() and not H.winning_cells(R, s.bb[0], s.bb[1]) and not H.winning_cells(R, s.bb[1], s.bb[0]):
            out.append(s)
    return out


def main():
    out = {}
    pos = positions()
    rows = []
    for it in (30, 60, 100, 300, 1000):
        lowN = same = 0
        reg_r = reg_q = 0.0
        for i, s in enumerate(pos):
            a = make_mcts(c=1.4, iterations=it, seed=500 + i)
            root = a.search(s)
            cr, cq = a.best_child(root, "robust"), a.best_child(root, "max_ratio")
            lowN += cq.N <= 2
            same += cr.move == cq.move
            S = MinimaxSearch(lambda st: H.ordered_moves(st, 1), H.evaluate, alpha_beta=True)
            vals = S.root_values(s, 2)
            best = max(vals.values())
            # "nước tốt" = nước có giá trị Alpha-Beta d=2 bằng giá trị tốt nhất
            reg_r += vals.get(cr.move, -1e18) >= best
            reg_q += vals.get(cq.move, -1e18) >= best
        n = len(pos)
        rows.append({"it": it, "positions": n, "ratio_pick_lowN": lowN / n, "same": same / n,
                     "robust_best": reg_r / n, "ratio_best": reg_q / n})
        print(rows[-1], flush=True)
    out["positions"] = rows
    save("e4b_low_budget.json", out)
    T9 = ("gomoku", 9, 5)
    m = [(f"robust_vs_ratio|{it}", T9, ("mcts", {"iterations": it, "final": "robust"}),
          ("mcts", {"iterations": it, "final": "max_ratio"})) for it in (30, 60, 100)]
    out["matches"] = run_matches(m, games=100, seed=45)
    for k, v in out["matches"].items():
        print(k, v["win"], v["draw"], v["loss"])
    save("e4b_low_budget.json", out)


if __name__ == "__main__":
    main()
