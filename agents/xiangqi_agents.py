"""Các agent cho Cờ tướng: Random, Alpha-Beta (lượng giá vật chất + vị trí), MCTS-UCT."""
from __future__ import annotations

import random

from games import xiangqi as XQ
from agents.mcts import MCTS
from agents.minimax import AlphaBetaAgent


class XQRandomAgent:
    name = "Random"

    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def select_move(self, state):
        return self.rng.choice(state.legal_moves())


def make_xq_alphabeta(depth=2, time_limit=None):
    return AlphaBetaAgent(XQ.ordered_moves, XQ.evaluate, depth=depth, time_limit=time_limit,
                          name=f"AlphaBeta(d={depth})")


def make_xq_mcts(c=1.4, iterations=300, rollout="eval", seed=None, time_limit=None,
                 depth=None):
    if rollout == "random":
        d = 40 if depth is None else depth
        rf = lambda s, rng: XQ.random_rollout(s, rng, d)
    elif rollout == "eval":
        d = 6 if depth is None else depth
        rf = lambda s, rng: XQ.eval_rollout(s, rng, d)
    else:
        raise ValueError(rollout)
    return MCTS(lambda s: list(s.legal_moves()), rf, c=c, iterations=iterations, seed=seed,
                time_limit=time_limit, name=f"MCTS-{rollout}(c={c},it={iterations})")
