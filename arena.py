"""Tổ chức ván đấu / loạt ván giữa hai agent (đổi lượt đi trước giữa các ván)."""
from __future__ import annotations

import time

DRAW = 2


def play_game(agents, state, verbose=False, max_plies=None):
    """agents[0] cầm quân của người 0 (đi trước). Trả về (winner, số nước, thời gian từng agent)."""
    t = [0.0, 0.0]
    plies = 0
    while not state.is_terminal():
        if max_plies is not None and plies >= max_plies:
            return DRAW, plies, t
        p = state.player
        t0 = time.perf_counter()
        m = agents[p].select_move(state)
        t[p] += time.perf_counter() - t0
        state = state.play(m)
        plies += 1
        if verbose:
            print(f"{agents[p].name} -> {state.move_str(m)}\n{state}\n")
    return state.winner(), plies, t


def play_match(make_a, make_b, make_state, games=50, seed=0, max_plies=None):
    """Đấu `games` ván giữa A và B, A đi trước ở ván chẵn, B đi trước ở ván lẻ.
    make_a/make_b(seed) -> agent mới (để mỗi ván có seed riêng, tái lập được).
    Trả về dict thống kê theo góc nhìn A."""
    res = {"win": 0, "draw": 0, "loss": 0, "win_first": 0, "loss_first": 0,
           "win_second": 0, "loss_second": 0, "plies": 0, "time_a": 0.0, "time_b": 0.0,
           "games": games}
    for g in range(games):
        a, b = make_a(seed * 100003 + 2 * g), make_b(seed * 100003 + 2 * g + 1)
        a_first = (g % 2 == 0)
        agents = (a, b) if a_first else (b, a)
        w, plies, t = play_game(agents, make_state(), max_plies=max_plies)
        ia = 0 if a_first else 1
        res["plies"] += plies
        res["time_a"] += t[ia]
        res["time_b"] += t[1 - ia]
        tag = "first" if a_first else "second"
        if w == DRAW:
            res["draw"] += 1
        elif w == ia:
            res["win"] += 1
            res["win_" + tag] += 1
        else:
            res["loss"] += 1
            res["loss_" + tag] += 1
    return res
