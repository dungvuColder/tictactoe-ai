"""
Tri thức heuristic cho Tic-Tac-Toe k quân:
  * hàm lượng giá theo "cửa sổ" k ô (window-based evaluation),
  * điểm nước đi (dùng để sắp thứ tự nước cho alpha-beta và cho người chơi tham lam),
  * tập ô "thắng ngay" (threat cells),
  * rollout heuristic cho MCTS: Thắng ngay > Chặn ngay > Ngẫu nhiên cục bộ.
"""
from __future__ import annotations

import random

from .gomoku import DRAW, GomokuRules, GomokuState, iter_bits

WIN_SCORE = 10_000_000


def window_weights(k: int):
    """Trọng số cho một cửa sổ chứa a quân của một bên (và 0 quân đối phương).
    Tăng theo cấp số nhân: W[a] = 10^(a-1)."""
    return [0] + [10 ** (a - 1) for a in range(1, k + 1)]


def winning_cells(rules: GomokuRules, own: int, opp: int) -> int:
    """Mặt nạ các ô trống mà `own` đặt vào là thắng ngay (đủ k quân)."""
    k1 = rules.k - 1
    res = 0
    for w in rules.windows:
        if not (w & opp) and (w & own).bit_count() == k1:
            res |= w & ~own
    return res


def local_winning_cells(rules: GomokuRules, own: int, opp: int, m: int) -> int:
    """Như winning_cells nhưng chỉ xét các cửa sổ đi qua ô m (dùng cập nhật tăng dần)."""
    k1 = rules.k - 1
    res = 0
    for w in rules.windows_of_cell[m]:
        if not (w & opp) and (w & own).bit_count() == k1:
            res |= w & ~own
    return res


def evaluate(state: GomokuState, player: int) -> float:
    """Hàm lượng giá tĩnh theo góc nhìn `player`.

    E(s) = Σ_{cửa sổ chỉ có quân của player} W[a]  -  Σ_{cửa sổ chỉ có quân đối thủ} W[b]
    kèm điều chỉnh "đến lượt": bên đang đến lượt mà có ô thắng ngay thì coi như thắng;
    bên kia có >= 2 ô thắng ngay (không thể chặn cả hai) thì coi như thua.
    """
    w = state.winner()
    if w is not None:
        if w == DRAW:
            return 0.0
        return WIN_SCORE if w == player else -WIN_SCORE
    R = state.rules
    k = R.k
    W = window_weights(k)
    own, opp = state.bb[player], state.bb[1 - player]
    score = 0
    own_threat = opp_threat = 0
    k1 = k - 1
    for win in R.windows:
        a = (win & own).bit_count()
        b = (win & opp).bit_count()
        if a and not b:
            score += W[a]
            if a == k1:
                own_threat |= win & ~own
        elif b and not a:
            score -= W[b]
            if b == k1:
                opp_threat |= win & ~opp
    to_move = state.player
    mover_threat, other_threat = (own_threat, opp_threat) if to_move == player else (opp_threat, own_threat)
    sign = 1 if to_move == player else -1
    if mover_threat:                       # bên đến lượt thắng ở nước kế tiếp
        return sign * (WIN_SCORE // 2)
    if other_threat.bit_count() >= 2:      # bên kia có 2 đường thắng, không chặn nổi
        return -sign * (WIN_SCORE // 4)
    return float(score)


def move_score(state: GomokuState, m: int) -> float:
    """Điểm cục bộ của nước m cho người đang đến lượt = tấn công + phòng thủ."""
    R = state.rules
    W = window_weights(R.k)
    p = state.player
    own, opp = state.bb[p], state.bb[1 - p]
    att = dfn = 0
    for win in R.windows_of_cell[m]:
        a = (win & own).bit_count()
        b = (win & opp).bit_count()
        if not b:
            att += W[a + 1]
        if not a:
            dfn += W[b + 1]
    return att + 0.9 * dfn


def ordered_moves(state: GomokuState, radius: int = 2) -> list[int]:
    """Sắp xếp nước đi giảm dần theo move_score (move ordering cho alpha-beta)."""
    moves = state.candidate_moves(radius)
    return sorted(moves, key=lambda m: move_score(state, m), reverse=True)


# ---------------------------------------------------------------- rollout
def heuristic_rollout(state: GomokuState, rng: random.Random, radius: int = 1) -> int:
    """Rollout heuristic đơn giản (3 luật):
        1) Nếu có ô thắng ngay  -> đi ô đó (kết thúc).
        2) Nếu đối thủ có ô thắng ngay -> chặn.
        3) Ngược lại: chọn ngẫu nhiên một ô trống trong bán kính `radius` quanh các quân đã đặt.
    Tập ô thắng ngay được cập nhật tăng dần nên mỗi bước chỉ tốn O(số cửa sổ qua 1 ô).
    """
    if state.is_terminal():
        return state.winner()
    R = state.rules
    bb = state.bb[:]
    p = state.player
    occ = bb[0] | bb[1]
    empty = R.full & ~occ
    threats = [winning_cells(R, bb[0], bb[1]), winning_cells(R, bb[1], bb[0])]
    neighbors = R.neighbors
    choice = rng.choice
    while empty:
        t_own = threats[p] & empty
        if t_own:
            return p                                  # luật 1: thắng ngay
        t_opp = threats[1 - p] & empty
        if t_opp:
            m = choice(list(iter_bits(t_opp)))        # luật 2: chặn
        else:
            near = neighbors(occ, radius) & empty if occ else empty
            if not near:
                near = empty
            m = choice(list(iter_bits(near)))         # luật 3: ngẫu nhiên cục bộ
        bit = 1 << m
        bb[p] |= bit
        occ |= bit
        empty &= ~bit
        threats[0] &= ~bit
        threats[1] &= ~bit
        threats[p] |= local_winning_cells(R, bb[p], bb[1 - p], m) & empty
        p ^= 1
    return DRAW


def random_rollout(state: GomokuState, rng: random.Random) -> int:
    return state.random_rollout(rng)
