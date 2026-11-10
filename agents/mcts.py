r"""
Monte Carlo Tree Search với chính sách chọn UCT (UCB1 applied to Trees).

    UCT(i) = W_i / N_i  +  c * sqrt( ln N_parent / N_i )
             \_______/      \___________________________/
             khai thác                khám phá

Mỗi vòng lặp (iteration) gồm 4 bước: Selection -> Expansion -> Simulation (rollout)
-> Backpropagation.  W_i được tính theo góc nhìn của người chơi VỪA ĐI vào nút i
(thắng = 1, hòa = 0.5, thua = 0), nên ở mọi tầng ta đều chọn max UCT.

Nước đi cuối cùng ở gốc được chọn theo:
    * "robust"  : N lớn nhất (mặc định, khuyến nghị)
    * "max_ratio": W/N lớn nhất (để so sánh trong thực nghiệm)

Thuật toán độc lập với trò chơi. Trạng thái cần có:
    copy(), play_inplace(m), is_terminal(), winner(), player
và hàm `moves_fn(state)` sinh các nước được phép mở rộng trong cây,
hàm `rollout_fn(state, rng)` trả về:  0 / 1 (người thắng), 2 (hòa)
hoặc một số thực trong [0, 1] = xác suất người chơi 0 thắng (rollout cắt cụt + lượng giá).
"""
from __future__ import annotations

import math
import random
import time

DRAW_CODE = 2


class Node:
    __slots__ = ("move", "parent", "children", "untried", "N", "W", "pjm")

    def __init__(self, move, parent, untried, player_just_moved):
        self.move = move
        self.parent = parent
        self.children = []
        self.untried = untried          # nước chưa mở rộng
        self.N = 0                      # số lần thăm
        self.W = 0.0                    # tổng phần thưởng (góc nhìn pjm)
        self.pjm = player_just_moved    # người vừa đi để tới nút này


def outcome_to_p0(outcome) -> float:
    """Chuẩn hóa kết quả rollout thành 'xác suất người chơi 0 thắng'."""
    if isinstance(outcome, float):
        return outcome
    if outcome == DRAW_CODE:
        return 0.5
    return 1.0 if outcome == 0 else 0.0


class MCTS:
    def __init__(self, moves_fn, rollout_fn, c: float = 1.4, iterations: int = 1000,
                 time_limit: float | None = None, final: str = "robust",
                 seed: int | None = None, name: str | None = None):
        self.moves_fn = moves_fn
        self.rollout_fn = rollout_fn
        self.c = c
        self.iterations = iterations
        self.time_limit = time_limit
        self.final = final
        self.rng = random.Random(seed)
        self.name = name or f"MCTS(c={c},it={iterations})"
        self.root = None
        self.last_info = {}

    # ----------------------------------------------------------- 4 bước
    def _select(self, node, state):
        c = self.c
        while not node.untried and node.children:
            logN = math.log(node.N)
            best, best_u = None, -1.0
            for ch in node.children:
                u = ch.W / ch.N + c * math.sqrt(logN / ch.N)
                if u > best_u:
                    best, best_u = ch, u
            node = best
            state.play_inplace(node.move)
        return node

    def _expand(self, node, state):
        if node.untried:
            i = self.rng.randrange(len(node.untried))
            m = node.untried[i]
            node.untried[i] = node.untried[-1]
            node.untried.pop()
            pjm = state.player
            state.play_inplace(m)
            child = Node(m, node, self.moves_fn(state) if not state.is_terminal() else [], pjm)
            node.children.append(child)
            return child
        return node

    @staticmethod
    def _backprop(node, value_p0: float):
        while node is not None:
            node.N += 1
            node.W += value_p0 if node.pjm == 0 else 1.0 - value_p0
            node = node.parent

    # ----------------------------------------------------------- tìm kiếm
    def search(self, state):
        root = Node(None, None, self.moves_fn(state), 1 - state.player)
        self.root = root
        t0 = time.perf_counter()
        deadline = None if self.time_limit is None else t0 + self.time_limit
        it = 0
        while True:
            if deadline is None:
                if it >= self.iterations:
                    break
            elif time.perf_counter() >= deadline and it > 0:
                break
            s = state.copy()
            leaf = self._select(root, s)                 # 1. Selection
            leaf = self._expand(leaf, s)                 # 2. Expansion
            if s.is_terminal():                          # 3. Simulation
                value = outcome_to_p0(s.winner())
            else:
                value = outcome_to_p0(self.rollout_fn(s, self.rng))
            self._backprop(leaf, value)                  # 4. Backpropagation
            it += 1
        self.last_info = {"iterations": it, "time": time.perf_counter() - t0,
                          "tree_size": self._count(root)}
        return root

    @staticmethod
    def _count(node):
        n, stack = 0, [node]
        while stack:
            x = stack.pop()
            n += 1
            stack.extend(x.children)
        return n

    def best_child(self, root, final: str | None = None):
        final = final or self.final
        if final == "robust":
            return max(root.children, key=lambda ch: (ch.N, ch.W))
        if final == "max_ratio":
            return max(root.children, key=lambda ch: (ch.W / ch.N, ch.N))
        raise ValueError(final)

    def select_move(self, state):
        root = self.search(state)
        if not root.children:          # (không xảy ra nếu iterations >= 1)
            return self.moves_fn(state)[0]
        return self.best_child(root).move

    def root_table(self, state=None):
        """Bảng thống kê tại nút gốc: [(move, W, N, W/N, UCT)] sắp theo N giảm dần."""
        root = self.root
        rows = []
        for ch in root.children:
            uct = ch.W / ch.N + self.c * math.sqrt(math.log(root.N) / ch.N)
            rows.append((ch.move, ch.W, ch.N, ch.W / ch.N, uct))
        rows.sort(key=lambda r: -r[2])
        return rows
