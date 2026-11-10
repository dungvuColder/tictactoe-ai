"""E6 (*) — Mở rộng cho Cờ tướng.

(a) Kiểm thử bộ sinh nước bằng perft từ thế cờ ban đầu (so với giá trị chuẩn đã công bố).
(b) Số nút Minimax vs Alpha-Beta vs Alpha-Beta + MVV-LVA ở độ sâu 1..3 (3 thế cờ).
(c) Đấu loạt: Alpha-Beta các độ sâu, MCTS rollout ngẫu nhiên, MCTS rollout ngắn + lượng giá
    (tương tự value network), với Random và với nhau. Giới hạn 200 nửa nước, lặp 3 lần => hòa.
"""
import random
import sys
import time

from common import run_matches, save
from games import xiangqi as XQ
from agents.minimax import MinimaxSearch

PERFT_REF = {1: 44, 2: 1920, 3: 79666, 4: 3290240}


def positions():
    rng = random.Random(3)
    res = [("Khai cuộc", XQ.XiangqiState())]
    for name, plies in (("Trung cuộc A (sau 16 nửa nước)", 16), ("Trung cuộc B (sau 30 nửa nước)", 30)):
        while True:
            s = XQ.XiangqiState()
            ok = True
            for _ in range(plies):
                mv = XQ.ordered_moves(s)
                if not mv:
                    ok = False
                    break
                # chọn ngẫu nhiên có thiên hướng ăn quân để ra thế cờ "thật"
                s = s.play(mv[0] if rng.random() < 0.3 else rng.choice(mv))
            if ok and not s.is_terminal():
                res.append((name, s))
                break
    return res


def nodes_table():
    out = []
    for name, s in positions():
        for d in (1, 2, 3):
            row = {"pos": name, "fen": s.fen(), "depth": d}
            for mode in ("minimax", "ab", "ab_mvvlva"):
                mf = XQ.ordered_moves if mode == "ab_mvvlva" else (lambda st: st.legal_moves())
                S = MinimaxSearch(mf, XQ.evaluate, alpha_beta=(mode != "minimax"))
                t0 = time.perf_counter()
                m, v = S.search(s, d)
                row[mode] = {"nodes": S.stats.nodes, "time": time.perf_counter() - t0, "value": v}
            row["same_value"] = row["minimax"]["value"] == row["ab"]["value"] == row["ab_mvvlva"]["value"]
            out.append(row)
            print(name, d, {k: row[k]["nodes"] for k in ("minimax", "ab", "ab_mvvlva")}, row["same_value"], flush=True)
    return out


def main():
    games = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    out = {"perft": []}
    s = XQ.XiangqiState()
    for d in (1, 2, 3, 4):
        t0 = time.perf_counter()
        n = XQ.perft(s, d)
        out["perft"].append({"depth": d, "nodes": n, "reference": PERFT_REF[d], "ok": n == PERFT_REF[d],
                             "time": time.perf_counter() - t0})
        print(out["perft"][-1], flush=True)
    out["nodes"] = nodes_table()
    save("e6_xiangqi.json", out)

    G = ("xiangqi", 200)
    R = ("xq_random", {})
    AB1, AB2, AB3 = ("xq_ab", {"depth": 1}), ("xq_ab", {"depth": 2}), ("xq_ab", {"depth": 3})
    MR = ("xq_mcts", {"iterations": 500, "rollout": "random"})
    ME = ("xq_mcts", {"iterations": 500, "rollout": "eval"})
    matches = [
        ("AB1 vs Random", G, AB1, R),
        ("AB2 vs Random", G, AB2, R),
        ("AB2 vs AB1", G, AB2, AB1),
        ("AB3 vs AB2", G, AB3, AB2),
        ("MCTS-random vs Random", G, MR, R),
        ("MCTS-eval vs Random", G, ME, R),
        ("MCTS-eval vs MCTS-random", G, ME, MR),
        ("MCTS-eval vs AB1", G, ME, AB1),
        ("MCTS-eval vs AB2", G, ME, AB2),
    ]
    out["matches"] = run_matches(matches, games=games, seed=61, log="E6")
    save("e6_xiangqi.json", out)


if __name__ == "__main__":
    main()
