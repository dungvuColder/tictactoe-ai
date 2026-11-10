"""
Tic-Tac-Toe tổng quát (m×m, k quân thẳng hàng thì thắng) dùng bitboard.

- Bàn 3×3, k = 3  : Tic-Tac-Toe cổ điển.
- Bàn N×N, k = 5  : "Tic-Tac-Toe 5 quân" (Caro / Gomoku tự do).

Biểu diễn: mỗi người chơi là một số nguyên Python (bitboard). Ô (r, c) ứng
với bit r*W + c, trong đó W = N + 1 (thêm 1 cột đệm luôn rỗng để các phép
dịch bit theo hàng/chéo không bị "tràn" sang hàng kế tiếp).

Bốn hướng thẳng hàng tương ứng với bốn độ dịch: 1 (ngang), W (dọc),
W+1 (chéo chính), W-1 (chéo phụ). Kiểm tra thắng toàn bàn chỉ cần
4*(k-1) phép AND + dịch bit.
"""
from __future__ import annotations

import random

X, O = 0, 1          # người chơi: X đi trước
DRAW = 2             # mã kết quả hòa
SYMBOLS = {X: "X", O: "O"}


class GomokuRules:
    """Thông tin tĩnh của một biến thể (kích thước, k, các mặt nạ bit)."""

    _cache: dict = {}

    def __new__(cls, n: int, k: int):
        key = (n, k)
        if key not in cls._cache:
            obj = super().__new__(cls)
            obj._init(n, k)
            cls._cache[key] = obj
        return cls._cache[key]

    def _init(self, n: int, k: int):
        assert 3 <= k <= n
        self.n, self.k = n, k
        self.W = W = n + 1
        self.dirs = (1, W, W + 1, W - 1)
        self.cells = [r * W + c for r in range(n) for c in range(n)]
        self.full = 0
        for i in self.cells:
            self.full |= 1 << i
        self.num_cells = n * n
        # Tất cả cửa sổ k ô thẳng hàng (dùng cho hàm lượng giá)
        self.windows = []          # list[int] mặt nạ của cửa sổ
        self.windows_of_cell = {i: [] for i in self.cells}
        for r in range(n):
            for c in range(n):
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    rr, cc = r + (k - 1) * dr, c + (k - 1) * dc
                    if 0 <= rr < n and 0 <= cc < n:
                        mask, idx = 0, []
                        for t in range(k):
                            p = (r + t * dr) * W + (c + t * dc)
                            mask |= 1 << p
                            idx.append(p)
                        wid = len(self.windows)
                        self.windows.append(mask)
                        for p in idx:
                            self.windows_of_cell[p].append(mask)
        self.center = (n // 2) * W + n // 2

    # ---- tiện ích ----
    def rc(self, idx: int):
        return divmod(idx, self.W)

    def idx(self, r: int, c: int) -> int:
        return r * self.W + c

    def has_k(self, b: int) -> bool:
        """True nếu bitboard b chứa k quân liên tiếp theo một hướng nào đó."""
        k = self.k
        for d in self.dirs:
            # x có bit i <=> b có L quân liên tiếp bắt đầu từ i (theo hướng d).
            # Nhân đôi L mỗi bước: chỉ cần ~log2(k) phép AND.
            x, L = b, 1
            while L < k and x:
                s = L if 2 * L <= k else k - L
                x &= x >> (s * d)
                L += s
            if x:
                return True
        return False

    def neighbors(self, occ: int, radius: int = 1) -> int:
        """Mặt nạ các ô nằm trong bán kính `radius` (Chebyshev) quanh quân đã đặt."""
        W, full = self.W, self.full
        x = occ
        for _ in range(radius):
            y = x
            for d in (1, W, W + 1, W - 1):
                y |= (x << d) | (x >> d)
            x = y & full
        return x


def iter_bits(x: int):
    """Liệt kê chỉ số các bit 1 của x."""
    while x:
        low = x & -x
        yield low.bit_length() - 1
        x ^= low


class GomokuState:
    """Trạng thái trò chơi. Bất biến về mặt ngữ nghĩa: play() trả về trạng thái mới."""

    __slots__ = ("rules", "bb", "player", "last", "nmoves", "_winner")

    def __init__(self, n: int = 3, k: int = 3, rules: GomokuRules | None = None):
        self.rules = rules or GomokuRules(n, k)
        self.bb = [0, 0]
        self.player = X
        self.last = -1
        self.nmoves = 0
        self._winner = None  # None: chưa kết thúc; X/O/DRAW

    # ------------------------------------------------------------------ cơ bản
    def copy(self) -> "GomokuState":
        s = GomokuState.__new__(GomokuState)
        s.rules = self.rules
        s.bb = self.bb[:]
        s.player = self.player
        s.last = self.last
        s.nmoves = self.nmoves
        s._winner = self._winner
        return s

    def play_inplace(self, m: int) -> None:
        p = self.player
        b = self.bb[p] | (1 << m)
        self.bb[p] = b
        self.last = m
        self.nmoves += 1
        if self.nmoves >= 2 * self.rules.k - 1 and self.rules.has_k(b):
            self._winner = p
        elif self.nmoves == self.rules.num_cells:
            self._winner = DRAW
        self.player = 1 - p

    def play(self, m: int) -> "GomokuState":
        s = self.copy()
        s.play_inplace(m)
        return s

    def occupied(self) -> int:
        return self.bb[0] | self.bb[1]

    def empty_mask(self) -> int:
        return self.rules.full & ~(self.bb[0] | self.bb[1])

    def is_terminal(self) -> bool:
        return self._winner is not None

    def winner(self):
        return self._winner

    def legal_moves(self) -> list[int]:
        if self._winner is not None:
            return []
        return list(iter_bits(self.empty_mask()))

    def candidate_moves(self, radius: int = 2) -> list[int]:
        """Nước đi "hợp lý" cho bàn lớn: các ô trống gần quân đã đặt.
        Với bàn 3×3 (hoặc bàn trống) trả về toàn bộ / ô trung tâm."""
        if self._winner is not None:
            return []
        R = self.rules
        if R.n <= 4:
            return self.legal_moves()
        occ = self.occupied()
        if occ == 0:
            return [R.center]
        return list(iter_bits(R.neighbors(occ, radius) & ~occ))

    def result_for(self, player: int) -> float:
        """Kết quả cuối ván theo góc nhìn `player`: 1 thắng, 0.5 hòa, 0 thua."""
        w = self._winner
        if w == DRAW:
            return 0.5
        return 1.0 if w == player else 0.0

    # --------------------------------------------------------------- tiện ích
    def key(self):
        return (self.bb[0], self.bb[1])

    def __str__(self) -> str:
        R = self.rules
        lines = []
        header = "   " + " ".join(f"{c:>2}" for c in range(R.n))
        lines.append(header)
        for r in range(R.n):
            row = []
            for c in range(R.n):
                i = R.idx(r, c)
                if self.bb[X] >> i & 1:
                    ch = "X"
                elif self.bb[O] >> i & 1:
                    ch = "O"
                else:
                    ch = "."
                row.append(f"{ch:>2}")
            lines.append(f"{r:>2} " + " ".join(row))
        return "\n".join(lines)

    def move_str(self, m: int) -> str:
        r, c = self.rules.rc(m)
        return f"({r},{c})"

    # ------------------------------------------------------- rollout nhanh
    def random_rollout(self, rng: random.Random) -> int:
        """Rollout ngẫu nhiên đều: hoán vị ngẫu nhiên các ô trống rồi đi lần lượt.
        Trả về người thắng (X/O) hoặc DRAW. Không thay đổi self."""
        if self._winner is not None:
            return self._winner
        R = self.rules
        empties = list(iter_bits(self.empty_mask()))
        rng.shuffle(empties)
        bb = self.bb[:]
        p = self.player
        n = self.nmoves
        thr = 2 * R.k - 1
        has_k = R.has_k
        for m in empties:
            b = bb[p] | (1 << m)
            bb[p] = b
            n += 1
            if n >= thr and has_k(b):
                return p
            p ^= 1
        return DRAW
