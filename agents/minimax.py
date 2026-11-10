"""
Minimax và Minimax + cắt tỉa Alpha-Beta (dạng MAX-VALUE / MIN-VALUE như AIMA, ch.5-6).

Dùng chung cho mọi trò chơi hai người, tổng bằng không, thông tin đầy đủ có giao diện:
    state.player          : người đến lượt (0/1)
    state.play(m)         : trạng thái mới sau nước m
    state.is_terminal()   : ván kết thúc?
    state.winner()        : 0 / 1 / 2 (=hòa)
và hai hàm cấu hình:
    moves_fn(state)       -> danh sách nước đi (có thể đã sắp thứ tự)
    eval_fn(state, p)     -> giá trị heuristic theo góc nhìn người chơi p (khi cắt độ sâu)
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass, field

WIN = 1_000_000_000
DRAW_CODE = 2


@dataclass
class SearchStats:
    nodes: int = 0          # số nút được sinh/duyệt (kể cả gốc)
    leaves: int = 0         # số lần gọi hàm lượng giá / tiện ích
    cutoffs: int = 0        # số lần cắt tỉa (alpha-beta)
    time: float = 0.0
    depth_reached: int = 0
    extra: dict = field(default_factory=dict)


class SearchTimeout(Exception):
    pass


def utility(state, root_player: int, ply: int) -> float:
    """Giá trị trạng thái kết thúc. Thắng sớm tốt hơn thắng muộn (trừ ply)."""
    w = state.winner()
    if w == DRAW_CODE:
        return 0.0
    return (WIN - ply) if w == root_player else -(WIN - ply)


class MinimaxSearch:
    """Bộ tìm kiếm có thể chạy ở chế độ minimax thuần hoặc alpha-beta."""

    def __init__(self, moves_fn, eval_fn=None, alpha_beta: bool = True,
                 deadline: float | None = None):
        self.moves_fn = moves_fn
        self.eval_fn = eval_fn
        self.alpha_beta = alpha_beta
        self.deadline = deadline
        self.stats = SearchStats()
        self.root_player = 0

    # ------------------------------------------------------------ public API
    def search(self, state, depth: int | None = None):
        """Trả về (nước tốt nhất, giá trị) cho người đến lượt ở `state`.
        depth=None: tìm kiếm tới trạng thái kết thúc (chỉ dùng cho bàn nhỏ)."""
        t0 = time.perf_counter()
        self.root_player = state.player
        self.stats.nodes += 1
        best_move, best_val = None, -math.inf
        alpha, beta = -math.inf, math.inf
        d = math.inf if depth is None else depth
        for m in self.moves_fn(state):
            v = self._min_value(state.play(m), d - 1, 1, alpha, beta)
            if v > best_val:
                best_val, best_move = v, m
            if self.alpha_beta:
                alpha = max(alpha, best_val)
        self.stats.time += time.perf_counter() - t0
        return best_move, best_val

    def root_values(self, state, depth: int | None = None):
        """Giá trị minimax chính xác của từng nước ở gốc (không cắt tỉa ở gốc)."""
        self.root_player = state.player
        d = math.inf if depth is None else depth
        return {m: self._min_value(state.play(m), d - 1, 1, -math.inf, math.inf)
                for m in self.moves_fn(state)}

    # ------------------------------------------------------------ internals
    def _cutoff_value(self, state, depth, ply):
        if state.is_terminal():
            self.stats.leaves += 1
            return utility(state, self.root_player, ply)
        if depth <= 0:
            self.stats.leaves += 1
            return self.eval_fn(state, self.root_player)
        return None

    def _check_time(self):
        if self.deadline is not None and (self.stats.nodes & 255) == 0 \
                and time.perf_counter() > self.deadline:
            raise SearchTimeout

    def _max_value(self, state, depth, ply, alpha, beta):
        self.stats.nodes += 1
        self._check_time()
        v0 = self._cutoff_value(state, depth, ply)
        if v0 is not None:
            return v0
        v = -math.inf
        for m in self.moves_fn(state):
            v = max(v, self._min_value(state.play(m), depth - 1, ply + 1, alpha, beta))
            if self.alpha_beta:
                if v >= beta:
                    self.stats.cutoffs += 1
                    return v
                alpha = max(alpha, v)
        return v

    def _min_value(self, state, depth, ply, alpha, beta):
        self.stats.nodes += 1
        self._check_time()
        v0 = self._cutoff_value(state, depth, ply)
        if v0 is not None:
            return v0
        v = math.inf
        for m in self.moves_fn(state):
            v = min(v, self._max_value(state.play(m), depth - 1, ply + 1, alpha, beta))
            if self.alpha_beta:
                if v <= alpha:
                    self.stats.cutoffs += 1
                    return v
                beta = min(beta, v)
        return v


class AlphaBetaAgent:
    """Agent dùng Alpha-Beta + iterative deepening (giới hạn độ sâu và/hoặc thời gian)."""

    def __init__(self, moves_fn, eval_fn, depth: int = 3, time_limit: float | None = None,
                 name: str | None = None):
        self.moves_fn, self.eval_fn = moves_fn, eval_fn
        self.depth, self.time_limit = depth, time_limit
        self.name = name or f"AlphaBeta(d={depth})"
        self.last_stats = None

    def select_move(self, state):
        deadline = None if self.time_limit is None else time.perf_counter() + self.time_limit
        best = None
        total = SearchStats()
        for d in range(1, self.depth + 1):
            s = MinimaxSearch(self.moves_fn, self.eval_fn, alpha_beta=True, deadline=deadline)
            try:
                m, v = s.search(state, d)
            except SearchTimeout:
                total.nodes += s.stats.nodes
                break
            total.nodes += s.stats.nodes
            total.depth_reached = d
            best = m
            if abs(v) >= WIN - 1000:       # đã tìm thấy thắng/thua chắc chắn
                break
        if best is None:
            best = self.moves_fn(state)[0]
        self.last_stats = total
        return best


class PerfectTTTAgent:
    """Người chơi hoàn hảo cho bàn nhỏ: minimax đầy đủ + bảng ghi nhớ (memo).
    Chọn ngẫu nhiên giữa các nước tối ưu (nếu rng được cung cấp) để đa dạng ván đấu."""

    name = "Minimax-perfect"

    def __init__(self, rng=None):
        self.rng = rng
        self.memo = {}

    def value(self, state) -> int:
        """Giá trị lý thuyết theo góc nhìn người đến lượt: +1 thắng, 0 hòa, -1 thua."""
        key = (state.bb[0], state.bb[1])
        if key in self.memo:
            return self.memo[key]
        w = state.winner()
        if w is not None:
            v = 0 if w == DRAW_CODE else (1 if w == state.player else -1)
        else:
            v = max(-self.value(state.play(m)) for m in state.legal_moves())
        self.memo[key] = v
        return v

    def optimal_moves(self, state):
        vals = {m: -self.value(state.play(m)) for m in state.legal_moves()}
        best = max(vals.values())
        return [m for m, v in vals.items() if v == best], vals

    def select_move(self, state):
        best, _ = self.optimal_moves(state)
        return self.rng.choice(best) if self.rng else best[0]
