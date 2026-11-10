"""Chơi trên terminal: người vs máy hoặc máy vs máy.

Ví dụ:
    python play.py --game caro --size 9 --p1 human --p2 mcts-h --iters 3000
    python play.py --game ttt --p1 mcts --p2 minimax
    python play.py --game xiangqi --p1 human --p2 ab --depth 3
Nhập nước đi:  Caro/TTT: "hàng cột" (vd: 4 4)   |   Cờ tướng: ký hiệu tọa độ (vd: h2e2)
"""
import argparse
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from games.gomoku import GomokuState, DRAW                       # noqa: E402
from games.xiangqi import XiangqiState                           # noqa: E402
from agents.baselines import RandomAgent, GreedyAgent, make_mcts, make_alphabeta  # noqa: E402
from agents.minimax import PerfectTTTAgent                       # noqa: E402
from agents.xiangqi_agents import XQRandomAgent, make_xq_alphabeta, make_xq_mcts  # noqa: E402


class Human:
    name = "Người chơi"

    def select_move(self, state):
        legal = state.legal_moves()
        while True:
            try:
                if isinstance(state, GomokuState):
                    s = input(f"Nước đi của bạn ({'X' if state.player == 0 else 'O'}) [hàng cột]: ")
                else:
                    s = input("Nước đi của bạn (vd h2e2): ")
                if isinstance(state, GomokuState):
                    r, c = map(int, s.replace(",", " ").split())
                    m = state.rules.idx(r, c)
                else:
                    m = state.parse_move(s.strip())
                if m in legal:
                    return m
            except (ValueError, IndexError):
                pass
            print("  Nước không hợp lệ, nhập lại.")


def build(kind, args, game):
    if kind == "human":
        return Human()
    if game == "xiangqi":
        if kind == "random":
            return XQRandomAgent()
        if kind == "ab":
            return make_xq_alphabeta(args.depth, time_limit=args.time)
        if kind in ("mcts", "mcts-h"):
            return make_xq_mcts(args.c, args.iters, "eval" if kind == "mcts-h" else "random")
        raise SystemExit(f"Agent không hỗ trợ cho cờ tướng: {kind}")
    if kind == "random":
        return RandomAgent()
    if kind == "greedy":
        return GreedyAgent()
    if kind == "minimax":
        return PerfectTTTAgent(random.Random())
    if kind == "ab":
        return make_alphabeta(args.depth, time_limit=args.time)
    if kind == "mcts":
        return make_mcts(args.c, args.iters, "random")
    if kind == "mcts-h":
        return make_mcts(args.c, args.iters, "heuristic")
    raise SystemExit(kind)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", choices=["ttt", "caro", "xiangqi"], default="caro")
    ap.add_argument("--size", type=int, default=9, help="kích thước bàn caro (mặc định 9)")
    ap.add_argument("--k", type=int, default=5, help="số quân thẳng hàng để thắng (caro)")
    ap.add_argument("--p1", default="human", help="human|random|greedy|minimax|ab|mcts|mcts-h")
    ap.add_argument("--p2", default="mcts-h")
    ap.add_argument("--iters", type=int, default=2000)
    ap.add_argument("--c", type=float, default=1.4)
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--time", type=float, default=None, help="giới hạn thời gian/nước cho Alpha-Beta (giây)")
    args = ap.parse_args()

    if args.game == "ttt":
        state = GomokuState(3, 3)
    elif args.game == "caro":
        state = GomokuState(args.size, args.k)
    else:
        state = XiangqiState()
    agents = [build(args.p1, args, args.game), build(args.p2, args, args.game)]
    print(state, "\n")
    while not state.is_terminal():
        a = agents[state.player]
        m = a.select_move(state)
        if not isinstance(a, Human):
            print(f"{a.name} đi {state.move_str(m)}")
        state = state.play(m)
        print(state, "\n")
    w = state.winner()
    print("Kết quả:", "Hòa" if w == DRAW else f"Người chơi {w + 1} ({agents[w].name}) thắng")


if __name__ == "__main__":
    main()
