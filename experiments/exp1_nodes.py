"""E1 — So sánh số nút duyệt: Minimax thuần vs Alpha-Beta (không sắp thứ tự) vs Alpha-Beta + move ordering.

(a) Tic-Tac-Toe 3×3: tìm kiếm toàn bộ cây (không giới hạn độ sâu) từ một số thế cờ gốc.
(b) Bàn 9×9, k=5: tìm kiếm giới hạn độ sâu d = 1..4 (hàm lượng giá theo cửa sổ) từ 5 thế cờ giữa ván.
Kiểm tra thêm: giá trị gốc của Minimax và Alpha-Beta phải trùng nhau (tính đúng đắn của cắt tỉa).
"""
import random
import time

from common import save
from games.gomoku import GomokuState
from games import gomoku_heuristics as H
from agents.baselines import GreedyAgent
from agents.minimax import MinimaxSearch


def run(state, depth, mode, radius=1):
    if mode == "minimax":
        mf, ab = (lambda s: s.candidate_moves(radius)), False
    elif mode == "ab":
        mf, ab = (lambda s: s.candidate_moves(radius)), True
    else:  # ab + ordering
        mf, ab = (lambda s: H.ordered_moves(s, radius)), True
    S = MinimaxSearch(mf, H.evaluate, alpha_beta=ab)
    t0 = time.perf_counter()
    m, v = S.search(state, depth)
    return {"nodes": S.stats.nodes, "leaves": S.stats.leaves, "cutoffs": S.stats.cutoffs,
            "time": time.perf_counter() - t0, "value": v, "move": m}


def positions_9x9(count=5, plies=10, seed=7):
    """Sinh thế cờ giữa ván bằng tự đấu của Greedy có nhiễu (đảm bảo chưa kết thúc)."""
    rng = random.Random(seed)
    res = []
    while len(res) < count:
        s = GomokuState(9, 5)
        g = GreedyAgent(rng.randrange(10 ** 9))
        for _ in range(plies):
            m = g.select_move(s) if rng.random() < 0.6 else rng.choice(s.candidate_moves(1))
            s = s.play(m)
            if s.is_terminal():
                break
        if not s.is_terminal():
            # bỏ các thế đã có đe dọa thắng ngay (quá dễ)
            R = s.rules
            if not (H.winning_cells(R, s.bb[0], s.bb[1]) or H.winning_cells(R, s.bb[1], s.bb[0])):
                res.append(s)
    return res


def main():
    out = {"3x3": [], "9x9": []}
    roots = {"Bàn trống": [], "X ở góc (0,0)": [0], "X ở tâm (1,1)": [5], "X tâm, O góc": [5, 0]}
    for name, moves in roots.items():
        s = GomokuState(3, 3)
        for m in moves:
            s = s.play(m)
        row = {"root": name}
        for mode in ("minimax", "ab", "ab_ord"):
            row[mode] = run(s, None, mode)
        out["3x3"].append(row)
        print(name, {k: (v["nodes"], round(v["time"], 3), v["value"]) for k, v in row.items() if k != "root"},
              flush=True)

    pos = positions_9x9()
    for d in (1, 2, 3, 4):
        for i, s in enumerate(pos):
            row = {"depth": d, "pos": i, "branching": len(s.candidate_moves(1))}
            for mode in ("minimax", "ab", "ab_ord"):
                if mode == "minimax" and d == 4 and i >= 3:
                    continue     # minimax d=4 rất chậm: chỉ đo trên 3 thế cờ
                row[mode] = run(s, d, mode)
            if "minimax" in row:
                row["same_value"] = (row["minimax"]["value"] == row["ab"]["value"] == row["ab_ord"]["value"])
            out["9x9"].append(row)
            print(d, i, {k: (v["nodes"], round(v["time"], 2)) for k, v in row.items() if isinstance(v, dict)},
                  flush=True)
            save("e1_nodes.json", out)
    save("e1_nodes.json", out)


if __name__ == "__main__":
    main()
