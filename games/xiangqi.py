"""
Cờ tướng (Xiangqi) — luật đầy đủ cho sinh nước đi hợp lệ.

Bàn 10 hàng × 9 cột, ô sq = r*9 + c, hàng 0 ở phía Đen (trên), hàng 9 ở phía Đỏ (dưới).
Đỏ (RED = 0) đi trước, Đen (BLACK = 1).
Ký hiệu quân: chữ HOA = Đỏ, chữ thường = Đen.
    K/k Tướng, A/a Sĩ, B/b Tượng, N/n Mã, R/r Xe, C/c Pháo, P/p Tốt.

Luật được cài đặt: phạm vi cung (Tướng, Sĩ), Tượng không qua sông + cản mắt Tượng,
Mã bị cản chân, Pháo ăn cách đúng một quân (ngòi), Tốt qua sông được đi ngang,
"lộ mặt tướng" (hai Tướng không được đối mặt trên cùng cột không có quân chắn),
không được để Tướng mình bị chiếu sau nước đi. Hết nước đi hợp lệ (bị chiếu bí hoặc
hết nước) => thua.  Đơn giản hóa: không cài luật cấm "chiếu dai/đuổi dai"; thay vào đó
ván được xử hòa khi một thế cờ lặp lại 3 lần hoặc vượt quá MAX_PLIES nước.
"""
from __future__ import annotations

import random

RED, BLACK = 0, 1
DRAW = 2
ROWS, COLS = 10, 9

START_FEN = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"

VALUES = {"K": 0, "A": 120, "B": 120, "N": 270, "R": 600, "C": 285, "P": 30}
PIECE_NAMES_VI = {"K": "Tướng", "A": "Sĩ", "B": "Tượng", "N": "Mã", "R": "Xe", "C": "Pháo", "P": "Tốt"}

ORTHO = ((-1, 0), (1, 0), (0, -1), (0, 1))
DIAG = ((-1, -1), (-1, 1), (1, -1), (1, 1))
# (bước Mã, chân Mã)
KNIGHT = (((-2, -1), (-1, 0)), ((-2, 1), (-1, 0)), ((2, -1), (1, 0)), ((2, 1), (1, 0)),
          ((-1, -2), (0, -1)), ((1, -2), (0, -1)), ((-1, 2), (0, 1)), ((1, 2), (0, 1)))


def side_of(p: str) -> int:
    return RED if p.isupper() else BLACK


def in_palace(r: int, c: int, side: int) -> bool:
    if not 3 <= c <= 5:
        return False
    return 7 <= r <= 9 if side == RED else 0 <= r <= 2


def own_half(r: int, side: int) -> bool:
    return r >= 5 if side == RED else r <= 4


# ---------------------------------------------------------------- PST
def _pst_bonus(p: str, r: int, c: int) -> int:
    """Điểm vị trí đơn giản (theo góc nhìn quân đó). r được chuẩn hóa về phía Đỏ."""
    t = p.upper()
    rr = r if p.isupper() else 9 - r     # khoảng cách từ đáy phía mình: 9 - rr
    adv = 9 - rr                          # số hàng đã tiến
    center = 4 - abs(c - 4)
    if t == "P":
        if adv >= 5:                      # đã qua sông
            return 40 + 10 * min(adv - 5, 3) + 6 * center - (25 if adv == 9 else 0)
        return 0
    if t == "N":
        return 6 * center + 4 * min(adv, 6)
    if t == "C":
        return 10 if c == 4 else 0
    if t == "R":
        return 2 * center + (8 if adv >= 5 else 0)
    return 0


PST = {}
for _p in "KABNRCPkabnrcp":
    for _r in range(ROWS):
        for _c in range(COLS):
            PST[(_p, _r * 9 + _c)] = VALUES[_p.upper()] + _pst_bonus(_p, _r, _c)


class XiangqiState:
    __slots__ = ("board", "player", "kings", "ply", "_legal", "_winner_cache")
    MAX_PLIES = 300

    def __init__(self, fen: str = START_FEN):
        self.board = ["."] * 90
        self.kings = [-1, -1]
        rows, side = fen.split()
        for r, row in enumerate(rows.split("/")):
            c = 0
            for ch in row:
                if ch.isdigit():
                    c += int(ch)
                else:
                    sq = r * 9 + c
                    self.board[sq] = ch
                    if ch == "K":
                        self.kings[RED] = sq
                    elif ch == "k":
                        self.kings[BLACK] = sq
                    c += 1
        self.player = RED if side == "w" else BLACK
        self.ply = 0
        self._legal = None
        self._winner_cache = -1

    # ---------------------------------------------------------- sao chép
    def copy(self) -> "XiangqiState":
        s = XiangqiState.__new__(XiangqiState)
        s.board = self.board[:]
        s.kings = self.kings[:]
        s.player = self.player
        s.ply = self.ply
        s._legal = None
        s._winner_cache = -1
        return s

    def fen(self) -> str:
        rows = []
        for r in range(ROWS):
            s, e = "", 0
            for c in range(COLS):
                p = self.board[r * 9 + c]
                if p == ".":
                    e += 1
                else:
                    if e:
                        s += str(e)
                        e = 0
                    s += p
            if e:
                s += str(e)
            rows.append(s)
        return "/".join(rows) + (" w" if self.player == RED else " b")

    def key(self):
        return ("".join(self.board), self.player)

    # ---------------------------------------------------------- sinh nước
    def pseudo_moves(self, side: int | None = None) -> list[int]:
        """Nước giả hợp lệ (chưa kiểm tra tự chiếu). Mã hóa nước = from*90 + to."""
        side = self.player if side is None else side
        b = self.board
        out = []
        app = out.append
        for sq in range(90):
            p = b[sq]
            if p == "." or side_of(p) != side:
                continue
            r, c = divmod(sq, 9)
            t = p.upper()
            base = sq * 90
            if t == "R" or t == "C":
                for dr, dc in ORTHO:
                    rr, cc = r + dr, c + dc
                    jumped = False
                    while 0 <= rr < ROWS and 0 <= cc < COLS:
                        q = b[rr * 9 + cc]
                        if not jumped:
                            if q == ".":
                                app(base + rr * 9 + cc)
                            else:
                                if t == "R":
                                    if side_of(q) != side:
                                        app(base + rr * 9 + cc)
                                    break
                                jumped = True          # Pháo: gặp ngòi
                        else:
                            if q != ".":
                                if side_of(q) != side:
                                    app(base + rr * 9 + cc)
                                break
                        rr += dr
                        cc += dc
            elif t == "N":
                for (dr, dc), (lr, lc) in KNIGHT:
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < ROWS and 0 <= cc < COLS and b[(r + lr) * 9 + c + lc] == ".":
                        q = b[rr * 9 + cc]
                        if q == "." or side_of(q) != side:
                            app(base + rr * 9 + cc)
            elif t == "P":
                fwd = -1 if side == RED else 1
                steps = [(fwd, 0)]
                if not own_half(r, side):
                    steps += [(0, -1), (0, 1)]
                for dr, dc in steps:
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < ROWS and 0 <= cc < COLS:
                        q = b[rr * 9 + cc]
                        if q == "." or side_of(q) != side:
                            app(base + rr * 9 + cc)
            elif t == "K":
                for dr, dc in ORTHO:
                    rr, cc = r + dr, c + dc
                    if in_palace(rr, cc, side):
                        q = b[rr * 9 + cc]
                        if q == "." or side_of(q) != side:
                            app(base + rr * 9 + cc)
            elif t == "A":
                for dr, dc in DIAG:
                    rr, cc = r + dr, c + dc
                    if in_palace(rr, cc, side):
                        q = b[rr * 9 + cc]
                        if q == "." or side_of(q) != side:
                            app(base + rr * 9 + cc)
            elif t == "B":
                for dr, dc in DIAG:
                    rr, cc = r + 2 * dr, c + 2 * dc
                    if 0 <= rr < ROWS and 0 <= cc < COLS and own_half(rr, side) \
                            and b[(r + dr) * 9 + c + dc] == ".":
                        q = b[rr * 9 + cc]
                        if q == "." or side_of(q) != side:
                            app(base + rr * 9 + cc)
        return out

    def attacked(self, sq: int, by: int) -> bool:
        """Ô sq có bị bên `by` tấn công không (dùng để kiểm tra chiếu tướng)."""
        b = self.board
        r, c = divmod(sq, 9)
        R_, C_, N_, P_, K_ = ("R", "C", "N", "P", "K") if by == RED else ("r", "c", "n", "p", "k")
        # Xe, Pháo, Tướng đối mặt (theo cột)
        for dr, dc in ORTHO:
            rr, cc = r + dr, c + dc
            screen = False
            while 0 <= rr < ROWS and 0 <= cc < COLS:
                q = b[rr * 9 + cc]
                if q != ".":
                    if not screen:
                        if q == R_ or (q == K_ and dc == 0):
                            return True
                        screen = True
                    else:
                        if q == C_:
                            return True
                        break
                rr += dr
                cc += dc
        # Mã: Mã ở (r+dr, c+dc) nhảy về (r, c); chân Mã nằm cạnh Mã, hướng về phía ô đích
        for dr, dc in ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (1, -2), (-1, 2), (1, 2)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and b[nr * 9 + nc] == N_:
                if abs(dr) == 2:
                    lr, lc = nr - (dr // 2), nc
                else:
                    lr, lc = nr, nc - (dc // 2)
                if b[lr * 9 + lc] == ".":
                    return True
        # Tốt
        fwd = -1 if by == RED else 1          # hướng tiến của Tốt bên tấn công
        pr = r - fwd
        if 0 <= pr < ROWS and b[pr * 9 + c] == P_:
            return True
        for dc in (-1, 1):
            cc = c + dc
            if 0 <= cc < COLS and b[r * 9 + cc] == P_ and not own_half(r, by):
                return True
        return False

    def in_check(self, side: int | None = None) -> bool:
        side = self.player if side is None else side
        return self.attacked(self.kings[side], 1 - side)

    def _make(self, m: int):
        """Thực hiện nước tại chỗ, trả về quân bị ăn (để hoàn tác)."""
        f, t = divmod(m, 90)
        b = self.board
        p, cap = b[f], b[t]
        b[t], b[f] = p, "."
        if p == "K":
            self.kings[RED] = t
        elif p == "k":
            self.kings[BLACK] = t
        return cap

    def _unmake(self, m: int, cap: str):
        f, t = divmod(m, 90)
        b = self.board
        p = b[t]
        b[f], b[t] = p, cap
        if p == "K":
            self.kings[RED] = f
        elif p == "k":
            self.kings[BLACK] = f

    def legal_moves(self) -> list[int]:
        if self._legal is None:
            side = self.player
            res = []
            for m in self.pseudo_moves(side):
                cap = self._make(m)
                if not self.attacked(self.kings[side], 1 - side):
                    res.append(m)
                self._unmake(m, cap)
            self._legal = res
        return self._legal

    def play_inplace(self, m: int) -> None:
        self._make(m)
        self.player ^= 1
        self.ply += 1
        self._legal = None
        self._winner_cache = -1

    def play(self, m: int) -> "XiangqiState":
        s = self.copy()
        s.play_inplace(m)
        return s

    # ---------------------------------------------------------- kết thúc
    def winner(self):
        """None nếu chưa kết thúc; RED/BLACK; DRAW (vượt MAX_PLIES)."""
        if self._winner_cache != -1:
            return self._winner_cache
        if not self.legal_moves():
            w = 1 - self.player             # hết nước (bị chiếu bí / hết nước) => thua
        elif self.ply >= self.MAX_PLIES:
            w = DRAW
        else:
            w = None
        self._winner_cache = w
        return w

    def is_terminal(self) -> bool:
        return self.winner() is not None

    def result_for(self, player: int) -> float:
        w = self.winner()
        return 0.5 if w == DRAW else (1.0 if w == player else 0.0)

    # ---------------------------------------------------------- hiển thị
    def move_str(self, m: int) -> str:
        f, t = divmod(m, 90)
        fr, fc = divmod(f, 9)
        tr, tc = divmod(t, 9)
        files = "abcdefghi"
        return f"{files[fc]}{9 - fr}{files[tc]}{9 - tr}"

    def parse_move(self, s: str) -> int:
        files = "abcdefghi"
        fc, fr, tc, tr = files.index(s[0]), 9 - int(s[1]), files.index(s[2]), 9 - int(s[3])
        return (fr * 9 + fc) * 90 + tr * 9 + tc

    def __str__(self) -> str:
        lines = []
        for r in range(ROWS):
            row = " ".join(self.board[r * 9 + c] for c in range(COLS))
            lines.append(f"{9 - r} {row}")
            if r == 4:
                lines.append("  ~~~~~ sông ~~~~~")
        lines.append("  a b c d e f g h i")
        return "\n".join(lines)


# ------------------------------------------------------------------ lượng giá
def material(state: XiangqiState) -> int:
    """Điểm vật chất + vị trí theo góc nhìn Đỏ."""
    s = 0
    for sq, p in enumerate(state.board):
        if p != ".":
            v = PST[(p, sq)]
            s += v if p.isupper() else -v
    return s


def evaluate(state: XiangqiState, player: int) -> float:
    """Hàm lượng giá theo góc nhìn `player` (dùng cho Alpha-Beta cắt độ sâu)."""
    v = material(state)
    if state.in_check(state.player):
        v += -30 if state.player == RED else 30   # bị chiếu: bất lợi nhẹ
    return v if player == RED else -v


def ordered_moves(state: XiangqiState) -> list[int]:
    """Sắp thứ tự MVV-LVA: ăn quân giá trị cao bằng quân giá trị thấp trước."""
    b = state.board

    def key(m):
        f, t = divmod(m, 90)
        cap = b[t]
        if cap == ".":
            return 0
        return 10 * VALUES[cap.upper()] - VALUES[b[f].upper()] + 10_000
    return sorted(state.legal_moves(), key=key, reverse=True)


# ------------------------------------------------------------------ rollout cho MCTS
def random_rollout(state: XiangqiState, rng: random.Random, max_depth: int = 40):
    """Rollout ngẫu nhiên thuần (nước giả hợp lệ, ăn Tướng = thắng).
    Hết max_depth nước mà chưa phân thắng bại => hòa (0.5): đánh giá thuần Monte Carlo."""
    s = state.copy()
    side = s.player
    b = s.board
    for _ in range(max_depth):
        moves = s.pseudo_moves(side)
        if not moves:
            return 1 - side
        m = rng.choice(moves)
        cap = b[m % 90]
        if cap in ("K", "k"):
            return side
        s._make(m)
        side ^= 1
    return DRAW


def eval_rollout(state: XiangqiState, rng: random.Random, max_depth: int = 6, scale: float = 400.0):
    """Rollout heuristic ngắn (ưu tiên ăn quân giá trị cao) rồi lượng giá bằng
    sigmoid(material / scale) => xác suất Đỏ thắng. Đây là "value function" thủ công."""
    import math
    s = state.copy()
    side = s.player
    b = s.board
    for _ in range(max_depth):
        moves = s.pseudo_moves(side)
        if not moves:
            return 1 - side
        best, best_v = [], -1
        for m in moves:
            cap = b[m % 90]
            if cap in ("K", "k"):
                return side
            v = VALUES[cap.upper()] if cap != "." else 0
            if v > best_v:
                best, best_v = [m], v
            elif v == best_v:
                best.append(m)
        m = rng.choice(best)
        s._make(m)
        side ^= 1
    return 1.0 / (1.0 + math.exp(-material(s) / scale))


def perft(state: XiangqiState, depth: int) -> int:
    if depth == 0:
        return 1
    n = 0
    for m in state.legal_moves():
        n += perft(state.play(m), depth - 1) if depth > 1 else 1
    return n
