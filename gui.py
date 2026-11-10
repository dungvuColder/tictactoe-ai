"""Giao diện đồ họa (pygame) cho Tic-Tac-Toe 3×3, Caro k quân và Cờ tướng.

    pip install pygame
    python gui.py --game caro --size 9 --ai mcts-h --iters 3000      # người (X) vs máy
    python gui.py --game caro --size 15 --ai ab --depth 3 --ai-first  # máy đi trước
    python gui.py --game ttt --ai mcts --iters 1000
    python gui.py --game xiangqi --ai ab --depth 3                    # người cầm Đỏ
    python gui.py --game caro --ai mcts-h --p1 ab                     # máy vs máy

Phím: R = ván mới, Esc = thoát. Máy suy nghĩ trong luồng riêng nên cửa sổ không bị treo.
"""
import argparse
import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame  # noqa: E402

from games.gomoku import GomokuState, DRAW, X, O, iter_bits  # noqa: E402
from games.xiangqi import XiangqiState, PIECE_NAMES_VI, RED  # noqa: E402
from play import build  # noqa: E402

BG = (240, 217, 167)
LINE = (90, 60, 30)
X_COL = (200, 40, 40)
O_COL = (30, 70, 160)
HL = (60, 170, 80)


def font(size, bold=False):
    return pygame.font.SysFont("arial,segoeui,dejavusans,liberationsans", size, bold=bold)


class App:
    def __init__(self, args):
        self.args = args
        pygame.init()
        self.game = args.game
        if self.game == "xiangqi":
            self.cell = 64
            self.margin = 50
            self.W = self.margin * 2 + self.cell * 8
            self.H = self.margin * 2 + self.cell * 9 + 40
        else:
            n = 3 if self.game == "ttt" else args.size
            self.n = n
            self.cell = 120 if n == 3 else max(32, min(56, 720 // n))
            self.margin = 30
            self.W = self.margin * 2 + self.cell * n
            self.H = self.W + 40
        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("BTL Trí tuệ nhân tạo — " + {"ttt": "Tic-Tac-Toe", "caro": "Caro 5 quân",
                                                                 "xiangqi": "Cờ tướng"}[self.game])
        self.reset()

    def reset(self):
        a = self.args
        if self.game == "ttt":
            self.state = GomokuState(3, 3)
        elif self.game == "caro":
            self.state = GomokuState(a.size, a.k)
        else:
            self.state = XiangqiState()
        ai = build(a.ai, a, self.game)
        other = build(a.p1, a, self.game) if a.p1 != "human" else None
        # người chơi = None
        self.players = [ai, other] if a.ai_first else [other, ai]
        self.last = None
        self.selected = None
        self.thinking = False
        self.result = None
        self.status = ""

    # ------------------------------------------------------------- vẽ
    def draw(self):
        self.screen.fill(BG)
        if self.game == "xiangqi":
            self.draw_xiangqi()
        else:
            self.draw_gomoku()
        msg = self.status
        if self.result is not None:
            msg = self.result + "   (R: ván mới)"
        elif self.thinking:
            msg = f"{self.players[self.state.player].name} đang suy nghĩ..."
        txt = font(18).render(msg, True, (20, 20, 20))
        self.screen.blit(txt, (12, self.H - 32))
        pygame.display.flip()

    def draw_gomoku(self):
        n, cs, mg = self.n, self.cell, self.margin
        for i in range(n + 1):
            pygame.draw.line(self.screen, LINE, (mg, mg + i * cs), (mg + n * cs, mg + i * cs), 1)
            pygame.draw.line(self.screen, LINE, (mg + i * cs, mg), (mg + i * cs, mg + n * cs), 1)
        R = self.state.rules
        for p, col in ((X, X_COL), (O, O_COL)):
            for idx in iter_bits(self.state.bb[p]):
                r, c = R.rc(idx)
                cx, cy = mg + c * cs + cs // 2, mg + r * cs + cs // 2
                rad = cs // 2 - max(4, cs // 8)
                if idx == self.last:
                    pygame.draw.rect(self.screen, (255, 245, 200), (mg + c * cs + 1, mg + r * cs + 1, cs - 1, cs - 1))
                w = max(2, cs // 14)
                if p == X:
                    pygame.draw.line(self.screen, col, (cx - rad, cy - rad), (cx + rad, cy + rad), w + 1)
                    pygame.draw.line(self.screen, col, (cx - rad, cy + rad), (cx + rad, cy - rad), w + 1)
                else:
                    pygame.draw.circle(self.screen, col, (cx, cy), rad, w)

    def sq_xy(self, sq):
        r, c = divmod(sq, 9)
        return self.margin + c * self.cell, self.margin + r * self.cell

    def draw_xiangqi(self):
        cs, mg = self.cell, self.margin
        for r in range(10):
            pygame.draw.line(self.screen, LINE, (mg, mg + r * cs), (mg + 8 * cs, mg + r * cs), 2)
        for c in range(9):
            if c in (0, 8):
                pygame.draw.line(self.screen, LINE, (mg + c * cs, mg), (mg + c * cs, mg + 9 * cs), 2)
            else:
                pygame.draw.line(self.screen, LINE, (mg + c * cs, mg), (mg + c * cs, mg + 4 * cs), 2)
                pygame.draw.line(self.screen, LINE, (mg + c * cs, mg + 5 * cs), (mg + c * cs, mg + 9 * cs), 2)
        for r0 in (0, 7):
            pygame.draw.line(self.screen, LINE, (mg + 3 * cs, mg + r0 * cs), (mg + 5 * cs, mg + (r0 + 2) * cs), 2)
            pygame.draw.line(self.screen, LINE, (mg + 5 * cs, mg + r0 * cs), (mg + 3 * cs, mg + (r0 + 2) * cs), 2)
        f2 = font(20, True)
        for txt, cx in (("Sở hà", mg + 2 * cs), ("Hán giới", mg + 6 * cs)):
            t = f2.render(txt, True, LINE)
            self.screen.blit(t, (cx - t.get_width() // 2, mg + 4 * cs + cs // 2 - t.get_height() // 2))
        if self.last is not None:
            for sq in divmod(self.last, 90):
                x, y = self.sq_xy(sq)
                pygame.draw.circle(self.screen, (230, 200, 90), (x, y), cs // 2 - 2, 3)
        targets = []
        if self.selected is not None:
            targets = [m % 90 for m in self.state.legal_moves() if m // 90 == self.selected]
        f = font(13, True)
        for sq, p in enumerate(self.state.board):
            if p == ".":
                continue
            x, y = self.sq_xy(sq)
            col = X_COL if p.isupper() else (20, 20, 20)
            pygame.draw.circle(self.screen, (250, 235, 200), (x, y), cs // 2 - 5)
            pygame.draw.circle(self.screen, HL if sq == self.selected else col, (x, y), cs // 2 - 5, 3)
            t = f.render(PIECE_NAMES_VI[p.upper()], True, col)
            self.screen.blit(t, (x - t.get_width() // 2, y - t.get_height() // 2))
        for sq in targets:
            x, y = self.sq_xy(sq)
            pygame.draw.circle(self.screen, HL, (x, y), 8)

    # ------------------------------------------------------------- logic
    def human_turn(self):
        return self.result is None and self.players[self.state.player] is None and not self.thinking

    def apply(self, m):
        self.state = self.state.play(m)
        self.last = m
        self.selected = None
        if self.state.is_terminal():
            w = self.state.winner()
            if w == DRAW:
                self.result = "Hòa!"
            else:
                who = self.players[w].name if self.players[w] else "Bạn"
                side = ("Đỏ" if w == RED else "Đen") if self.game == "xiangqi" else ("X" if w == X else "O")
                self.result = f"{who} ({side}) thắng!"

    def ai_move(self):
        agent = self.players[self.state.player]
        st = self.state
        m = agent.select_move(st)
        if st is self.state:            # chưa bị reset trong lúc suy nghĩ
            self.apply(m)
        self.thinking = False

    def click(self, pos):
        if not self.human_turn():
            return
        x, y = pos
        if self.game == "xiangqi":
            c = round((x - self.margin) / self.cell)
            r = round((y - self.margin) / self.cell)
            if not (0 <= r < 10 and 0 <= c < 9):
                return
            sq = r * 9 + c
            p = self.state.board[sq]
            if self.selected is not None:
                m = self.selected * 90 + sq
                if m in self.state.legal_moves():
                    self.apply(m)
                    return
            if p != "." and (p.isupper() == (self.state.player == RED)):
                self.selected = sq
        else:
            c = (x - self.margin) // self.cell
            r = (y - self.margin) // self.cell
            if 0 <= r < self.n and 0 <= c < self.n:
                m = self.state.rules.idx(r, c)
                if m in self.state.legal_moves():
                    self.apply(m)

    def run(self, max_frames=None, screenshot=None):
        clock = pygame.time.Clock()
        frames = 0
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_r:
                    self.reset()
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.click(ev.pos)
            if self.result is None and not self.thinking and self.players[self.state.player] is not None:
                self.thinking = True
                threading.Thread(target=self.ai_move, daemon=True).start()
            self.draw()
            clock.tick(30)
            frames += 1
            if max_frames and frames >= max_frames:
                if screenshot:
                    pygame.image.save(self.screen, screenshot)
                pygame.quit()
                return


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game", choices=["ttt", "caro", "xiangqi"], default="caro")
    ap.add_argument("--size", type=int, default=9)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--ai", default="mcts-h", help="random|greedy|minimax|ab|mcts|mcts-h")
    ap.add_argument("--p1", default="human", help="đối thủ còn lại: human hoặc một loại agent")
    ap.add_argument("--ai-first", action="store_true", help="máy đi trước")
    ap.add_argument("--iters", type=int, default=2000)
    ap.add_argument("--c", type=float, default=1.4)
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--time", type=float, default=None)
    ap.add_argument("--frames", type=int, default=None, help=argparse.SUPPRESS)
    ap.add_argument("--screenshot", default=None, help=argparse.SUPPRESS)
    args = ap.parse_args()
    App(args).run(args.frames, args.screenshot)


if __name__ == "__main__":
    main()
