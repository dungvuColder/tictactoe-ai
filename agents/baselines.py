"""Các đối thủ cơ sở và hàm tạo agent tiện dụng cho Tic-Tac-Toe k quân."""
from __future__ import annotations

import random

from games.gomoku import iter_bits
from games import gomoku_heuristics as H
from agents.mcts import MCTS
from agents.minimax import AlphaBetaAgent


class RandomAgent:
    name = "Random"

    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def select_move(self, state):
        return self.rng.choice(state.legal_moves())


class GreedyAgent:
    """Tham lam 1 lớp: thắng ngay > chặn ngay > nước có move_score cao nhất (phá hòa ngẫu nhiên)."""
    name = "Greedy"

    def __init__(self, seed=None, radius: int = 2):
        self.rng = random.Random(seed)
        self.radius = radius

    def select_move(self, state):
        R = state.rules
        p = state.player
        own, opp = state.bb[p], state.bb[1 - p]
        empty = state.empty_mask()
        win = H.winning_cells(R, own, opp) & empty
        if win:
            return self.rng.choice(list(iter_bits(win)))
        block = H.winning_cells(R, opp, own) & empty
        if block:
            return self.rng.choice(list(iter_bits(block)))
        moves = state.candidate_moves(self.radius)
        scores = [H.move_score(state, m) for m in moves]
        best = max(scores)
        return self.rng.choice([m for m, s in zip(moves, scores) if s >= best - 1e-9])


# ---------------------------------------------------------------- factories
def tree_moves(radius: int):
    def f(state):
        return state.candidate_moves(radius)
    return f


def make_mcts(c=1.4, iterations=1000, rollout="random", seed=None, radius=1,
              final="robust", time_limit=None):
    if rollout == "random":
        rf = H.random_rollout
    elif rollout == "heuristic":
        rf = H.heuristic_rollout
    else:
        raise ValueError(rollout)
    return MCTS(tree_moves(radius), rf, c=c, iterations=iterations, seed=seed,
                final=final, time_limit=time_limit,
                name=f"MCTS-{rollout}(c={c},it={iterations})")


def make_alphabeta(depth=3, radius=2, time_limit=None):
    def moves(state):
        return H.ordered_moves(state, radius)
    return AlphaBetaAgent(moves, H.evaluate, depth=depth, time_limit=time_limit,
                          name=f"AlphaBeta(d={depth})")


class EpsilonGreedyAgent(GreedyAgent):
    """Greedy có nhiễu: luôn thắng ngay/chặn ngay, nhưng với xác suất eps đi một nước
    ngẫu nhiên gần quân đã đặt. Là đối thủ "trung bình" cố định, không phụ thuộc c."""

    def __init__(self, eps=0.5, seed=None, radius: int = 2):
        super().__init__(seed, radius)
        self.eps = eps
        self.name = f"EpsGreedy({eps})"

    def select_move(self, state):
        R = state.rules
        p = state.player
        own, opp = state.bb[p], state.bb[1 - p]
        empty = state.empty_mask()
        win = H.winning_cells(R, own, opp) & empty
        if win:
            return self.rng.choice(list(iter_bits(win)))
        block = H.winning_cells(R, opp, own) & empty
        if block:
            return self.rng.choice(list(iter_bits(block)))
        if self.rng.random() < self.eps:
            return self.rng.choice(state.candidate_moves(1))
        return super().select_move(state)
