"""Hạ tầng chung cho thực nghiệm: mô tả agent bằng dict (pickle được), chạy song song nhiều ván."""
from __future__ import annotations

import json
import os
import random
import sys
import time
from multiprocessing import Pool

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from games.gomoku import GomokuState                      # noqa: E402
from games.xiangqi import XiangqiState                    # noqa: E402
from agents.baselines import (RandomAgent, GreedyAgent, EpsilonGreedyAgent,  # noqa: E402
                              make_mcts, make_alphabeta)
from agents.minimax import PerfectTTTAgent                # noqa: E402
from agents.xiangqi_agents import XQRandomAgent, make_xq_alphabeta, make_xq_mcts  # noqa: E402

RESULTS = os.path.join(ROOT, "results")
os.makedirs(RESULTS, exist_ok=True)
DRAW = 2
NPROC = int(os.environ.get("NPROC", os.cpu_count() or 1))

_perfect = None


def make_agent(spec, seed):
    kind, kw = spec
    if kind == "random":
        return RandomAgent(seed)
    if kind == "greedy":
        return GreedyAgent(seed)
    if kind == "epsgreedy":
        return EpsilonGreedyAgent(kw.get("eps", 0.5), seed)
    if kind == "ab":
        return make_alphabeta(**kw)
    if kind == "perfect":
        global _perfect
        if _perfect is None:
            _perfect = PerfectTTTAgent()
        _perfect.rng = random.Random(seed)
        return _perfect
    if kind == "mcts":
        return make_mcts(seed=seed, **kw)
    if kind == "xq_random":
        return XQRandomAgent(seed)
    if kind == "xq_ab":
        return make_xq_alphabeta(**kw)
    if kind == "xq_mcts":
        return make_xq_mcts(seed=seed, **kw)
    raise ValueError(kind)


def make_state(game):
    if game[0] == "gomoku":
        return GomokuState(game[1], game[2])
    if game[0] == "xiangqi":
        s = XiangqiState()
        if len(game) > 1:
            XiangqiState.MAX_PLIES = game[1]
        return s
    raise ValueError(game)


def _play_one(job):
    """job = (tag, game, specA, specB, g, seed). A đi trước nếu g chẵn."""
    tag, game, spec_a, spec_b, g, seed = job
    a = make_agent(spec_a, seed * 1_000_003 + 2 * g)
    b = make_agent(spec_b, seed * 1_000_003 + 2 * g + 1)
    a_first = (g % 2 == 0)
    agents = (a, b) if a_first else (b, a)
    state = make_state(game)
    if game[0] == "xiangqi" and len(game) > 2 and game[2] > 0:
        # Khai cuộc ngẫu nhiên game[2] nửa nước, dùng chung cho cặp ván (2g, 2g+1) đổi màu
        # => tránh việc hai agent tất định lặp lại đúng một ván.
        orng = random.Random(seed * 7919 + g // 2)
        for _ in range(game[2]):
            state = state.play(orng.choice(state.legal_moves()))
    times = [0.0, 0.0]
    moves_cnt = [0, 0]
    seen = {}
    plies = 0
    w = None
    while not state.is_terminal():
        p = state.player
        t0 = time.perf_counter()
        m = agents[p].select_move(state)
        times[p] += time.perf_counter() - t0
        moves_cnt[p] += 1
        state = state.play(m)
        plies += 1
        if game[0] == "xiangqi":                  # hòa khi lặp thế cờ 3 lần
            k = state.key()
            seen[k] = seen.get(k, 0) + 1
            if seen[k] >= 3:
                w = DRAW
                break
    if w is None:
        w = state.winner()
    ia = 0 if a_first else 1
    if w == DRAW:
        r = "draw"
    elif w == ia:
        r = "win"
    else:
        r = "loss"
    return {"tag": tag, "g": g, "a_first": a_first, "result": r, "plies": plies,
            "time_a": times[ia], "time_b": times[1 - ia],
            "moves_a": moves_cnt[ia], "moves_b": moves_cnt[1 - ia]}


def run_matches(matches, games=50, seed=0, procs=NPROC, log=None):
    """matches: list[(tag, game, specA, specB)] -> dict tag -> thống kê (góc nhìn A)."""
    jobs = [(tag, game, sa, sb, g, seed) for (tag, game, sa, sb) in matches for g in range(games)]
    # xen kẽ để cân bằng tải
    random.Random(seed).shuffle(jobs)
    out = {tag: [] for (tag, *_rest) in matches}
    t0 = time.time()
    with Pool(procs) as pool:
        for i, r in enumerate(pool.imap_unordered(_play_one, jobs, chunksize=1)):
            out[r["tag"]].append(r)
            if log and (i + 1) % max(1, len(jobs) // 20) == 0:
                print(f"  [{log}] {i + 1}/{len(jobs)} ván, {time.time() - t0:.0f}s", flush=True)
    return {tag: summarize(rs) for tag, rs in out.items()}


def summarize(rs):
    n = len(rs)
    s = {"games": n}
    for k in ("win", "draw", "loss"):
        s[k] = sum(1 for r in rs if r["result"] == k)
    s["win_rate"] = s["win"] / n
    s["nonloss_rate"] = (s["win"] + s["draw"]) / n
    s["score"] = (s["win"] + 0.5 * s["draw"]) / n
    for side, flag in (("first", True), ("second", False)):
        sub = [r for r in rs if r["a_first"] == flag]
        s[f"win_{side}"] = sum(1 for r in sub if r["result"] == "win")
        s[f"draw_{side}"] = sum(1 for r in sub if r["result"] == "draw")
        s[f"loss_{side}"] = sum(1 for r in sub if r["result"] == "loss")
    s["avg_plies"] = sum(r["plies"] for r in rs) / n
    ma = sum(r["moves_a"] for r in rs)
    s["ms_per_move_a"] = 1000 * sum(r["time_a"] for r in rs) / max(1, ma)
    mb = sum(r["moves_b"] for r in rs)
    s["ms_per_move_b"] = 1000 * sum(r["time_b"] for r in rs) / max(1, mb)
    return s


def save(name, obj):
    path = os.path.join(RESULTS, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    print("Đã lưu", path)


def load(name):
    with open(os.path.join(RESULTS, name), encoding="utf-8") as f:
        return json.load(f)
