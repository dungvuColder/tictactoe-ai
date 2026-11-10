"""E2 — Kiểm chứng: với Tic-Tac-Toe 3×3, MCTS-UCT (đủ iteration) KHÔNG BAO GIỜ THUA.

Hai cách kiểm chứng:
(a) VÉT CẠN chiến lược đối thủ: tại lượt đối thủ, rẽ nhánh theo MỌI nước hợp lệ; tại lượt MCTS,
    gọi MCTS (seed cố định theo thế cờ => chính sách xác định). Duyệt hết mọi ván có thể xảy ra
    => nếu số ván thua = 0 thì MCTS không thua trước BẤT KỲ đối thủ nào (kể cả đối thủ hoàn hảo).
    Đồng thời đo tỷ lệ quyết định của MCTS trùng với nước tối ưu lý thuyết (minimax).
(b) Đấu loạt >= 100 ván (đổi lượt đi trước) với Random, Minimax hoàn hảo và chính nó.
"""
import sys
import zlib
from multiprocessing import Pool

from common import run_matches, save, NPROC
from games.gomoku import GomokuState, DRAW
from agents.baselines import make_mcts
from agents.minimax import PerfectTTTAgent

ITS = [10, 25, 50, 100, 200, 500, 1000, 2000]
SEEDS = [0, 1, 2, 3, 4]
_P = PerfectTTTAgent()


def verify(args):
    it, c, seed, side, rollout = args
    decided = {}
    st = {"lines": 0, "win": 0, "draw": 0, "loss": 0, "decisions": 0, "optimal": 0,
          "loss_example": None}

    def rec(s, hist):
        if s.is_terminal():
            st["lines"] += 1
            w = s.winner()
            if w == DRAW:
                st["draw"] += 1
            elif w == side:
                st["win"] += 1
            else:
                st["loss"] += 1
                if st["loss_example"] is None:
                    st["loss_example"] = hist
            return
        if s.player == side:
            key = (s.bb[0], s.bb[1])
            if key not in decided:
                sd = zlib.crc32(f"{seed}|{key}".encode())
                m = make_mcts(c=c, iterations=it, rollout=rollout, seed=sd).select_move(s)
                decided[key] = m
                st["decisions"] += 1
                best, _ = _P.optimal_moves(s)
                st["optimal"] += (m in best)
            m = decided[key]
            rec(s.play(m), hist + [m])
        else:
            for m in s.legal_moves():
                rec(s.play(m), hist + [m])

    rec(GomokuState(3, 3), [])
    return {"it": it, "c": c, "seed": seed, "side": side, "rollout": rollout, **st}


def main():
    games = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    out = {}
    jobs = [(it, 1.4, sd, side, ro) for ro in ("random", "heuristic") for it in ITS
            for sd in SEEDS for side in (0, 1)]
    jobs.sort(key=lambda j: -j[0])
    with Pool(NPROC) as pool:
        out["exhaustive"] = pool.map(verify, jobs, chunksize=1)
    save("e2_never_lose.json", out)
    for ro in ("random", "heuristic"):
        for it in ITS:
            rs = [r for r in out["exhaustive"] if r["it"] == it and r["rollout"] == ro]
            print(ro, it, "loss lines:", sum(r["loss"] for r in rs), "/", sum(r["lines"] for r in rs),
                  "opt:", sum(r["optimal"] for r in rs), "/", sum(r["decisions"] for r in rs), flush=True)

    T = ("gomoku", 3, 3)
    matches = []
    for it in (100, 1000):
        mc = ("mcts", {"c": 1.4, "iterations": it})
        matches += [(f"mcts{it}|random", T, mc, ("random", {})),
                    (f"mcts{it}|perfect", T, mc, ("perfect", {})),
                    (f"mcts{it}|ab", T, mc, ("ab", {"depth": 9})),
                    (f"mcts{it}|self", T, mc, mc)]
    out["matches"] = run_matches(matches, games=games, seed=21, log="E2")
    save("e2_never_lose.json", out)


if __name__ == "__main__":
    main()
