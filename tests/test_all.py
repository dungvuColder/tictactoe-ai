"""Kiểm thử đơn vị. Chạy:  python -m pytest -q tests   (hoặc  python tests/test_all.py)"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from games.gomoku import GomokuState, X, O, DRAW                       # noqa: E402
from games import gomoku_heuristics as H                                 # noqa: E402
from games import xiangqi as XQ                                          # noqa: E402
from agents.minimax import MinimaxSearch, PerfectTTTAgent                # noqa: E402
from agents.baselines import make_mcts, RandomAgent                      # noqa: E402


def play_rc(s, cells):
    for r, c in cells:
        s = s.play(s.rules.idx(r, c))
    return s


def test_win_detection_all_directions():
    for cells_x in ([(4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],      # ngang
                    [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8)],      # dọc, sát mép phải
                    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],      # chéo chính
                    [(0, 8), (1, 7), (2, 6), (3, 5), (4, 4)]):     # chéo phụ
        s = GomokuState(9, 5)
        o_cells = [(8, i) for i in range(4)] if cells_x[0] != (4, 0) else [(8, i + 4) for i in range(4)]
        for i in range(5):
            s = s.play(s.rules.idx(*cells_x[i]))
            if i < 4:
                assert not s.is_terminal()
                s = s.play(s.rules.idx(*o_cells[i]))
        assert s.winner() == X


def test_no_wraparound():
    # 3 quân cuối hàng 0 + 2 quân đầu hàng 1 KHÔNG được tính là 5 liên tiếp
    s = GomokuState(9, 5)
    xs = [(0, 6), (0, 7), (0, 8), (1, 0), (1, 1)]
    os_ = [(5, 0), (5, 2), (5, 4), (5, 6)]
    for i in range(5):
        s = s.play(s.rules.idx(*xs[i]))
        if i < 4:
            s = s.play(s.rules.idx(*os_[i]))
    assert not s.is_terminal()


def test_minimax_tree_size_and_value():
    s = GomokuState(3, 3)
    S = MinimaxSearch(lambda st: st.legal_moves(), None, alpha_beta=False)
    _, v = S.search(s, None)
    assert v == 0 and S.stats.nodes == 549946          # cây Tic-Tac-Toe đầy đủ
    A = MinimaxSearch(lambda st: st.legal_moves(), None, alpha_beta=True)
    _, v2 = A.search(s, None)
    assert v2 == 0 and A.stats.nodes < S.stats.nodes / 10
    P = PerfectTTTAgent()
    assert P.value(s) == 0 and len(P.memo) == 5478       # 5.478 trạng thái hợp lệ


def test_alphabeta_equals_minimax_depth_limited():
    rng = random.Random(1)
    for _ in range(3):
        s = GomokuState(9, 5)
        for _ in range(8):
            s = s.play(rng.choice(s.candidate_moves(1)))
        vals = []
        for ab in (False, True):
            S = MinimaxSearch(lambda st: st.candidate_moves(1), H.evaluate, alpha_beta=ab)
            vals.append(S.search(s, 2)[1])
        assert vals[0] == vals[1]


def test_heuristic_rollout_takes_win():
    s = play_rc(GomokuState(9, 5), [(4, 0), (0, 0), (4, 1), (0, 2), (4, 2), (0, 4), (4, 3), (8, 8)])
    rng = random.Random(0)
    assert all(H.heuristic_rollout(s, rng) == X for _ in range(50))   # X có ô thắng ngay


def test_mcts_never_loses_vs_perfect():
    P = PerfectTTTAgent(random.Random(0))
    for g in range(10):
        s = GomokuState(3, 3)
        mcts = make_mcts(c=1.4, iterations=2000, seed=g)
        agents = (mcts, P) if g % 2 == 0 else (P, mcts)
        while not s.is_terminal():
            s = s.play(agents[s.player].select_move(s))
        assert s.winner() == DRAW


def test_xiangqi_perft():
    s = XQ.XiangqiState()
    assert [XQ.perft(s, d) for d in (1, 2, 3)] == [44, 1920, 79666]


def test_xiangqi_special_rules():
    # Mã bị cản chân: Mã đỏ b0 có chân b1? -> thế đầu: Mã b0 đi được a2, c2 (chân b1 trống)
    s = XQ.XiangqiState()
    moves = {s.move_str(m) for m in s.legal_moves()}
    assert {"b0a2", "b0c2", "b2b9"} <= moves           # Pháo b2 ăn Mã b9 qua ngòi b7
    assert "b2b8" not in moves                        # Pháo không được nhảy qua ngòi b7 khi không ăn quân
    # Lộ mặt tướng: hai Tướng cùng cột không quân chắn -> nước làm lộ mặt là bất hợp lệ
    s2 = XQ.XiangqiState("4k4/9/9/9/9/9/9/9/4A4/4K4 w")
    mv2 = {s2.move_str(m) for m in s2.legal_moves()}
    assert "e1d0" not in mv2 and "e1d2" not in mv2   # Sĩ rời cột e => hai Tướng đối mặt
    s3 = XQ.XiangqiState("3k5/9/9/9/9/9/9/9/9/4K4 w")
    assert "e0d0" not in {s3.move_str(m) for m in s3.legal_moves()}   # đi sang cột d => đối mặt Tướng đen


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
