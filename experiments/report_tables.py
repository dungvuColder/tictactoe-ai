"""In các bảng kết quả (Markdown) từ results/*.json — dùng để đưa vào báo cáo."""
from common import load


def pct(x):
    return f"{100 * x:.0f}%"


def f_int(x):
    return f"{x:,.0f}".replace(",", ".")


def e1():
    d = load("e1_nodes.json")
    print("### E1a 3x3 toàn cây")
    print("| Gốc | Minimax: nút | Alpha-Beta: nút | AB + sắp thứ tự: nút | Giảm (AB+ord / Minimax) | Thời gian Minimax → AB+ord | Giá trị |")
    print("|---|---|---|---|---|---|---|")
    for r in d["3x3"]:
        m, a, o = r["minimax"], r["ab"], r["ab_ord"]
        print(f"| {r['root']} | {f_int(m['nodes'])} | {f_int(a['nodes'])} | {f_int(o['nodes'])} | "
              f"{m['nodes'] / o['nodes']:.0f}× | {m['time']:.2f} s → {o['time']:.3f} s | {int(m['value'] > 0) - int(m['value'] < 0)} |")
    print("\n### E1b 9x9 theo độ sâu (trung bình các thế cờ)")
    print("| d | Số thế | b TB | Minimax | Alpha-Beta | AB + sắp thứ tự | Minimax/AB+ord | thời gian Minimax | thời gian AB+ord | Cùng giá trị |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    rows = d["9x9"]
    for dd in sorted({r["depth"] for r in rows}):
        rs = [r for r in rows if r["depth"] == dd]
        mm = [r for r in rs if "minimax" in r]
        avg = lambda key, sub, k="nodes": sum(r[key][k] for r in sub) / len(sub)
        print(f"| {dd} | {len(rs)} | {sum(r['branching'] for r in rs) / len(rs):.1f} | {f_int(avg('minimax', mm))} | "
              f"{f_int(avg('ab', rs))} | {f_int(avg('ab_ord', rs))} | "
              f"{sum(r['minimax']['nodes'] for r in mm) / sum(r['ab_ord']['nodes'] for r in mm):.0f}× | "
              f"{avg('minimax', mm, 'time'):.2f} s | {avg('ab_ord', rs, 'time'):.3f} s | "
              f"{sum(r['same_value'] for r in mm)}/{len(mm)} |")


def e2():
    d = load("e2_never_lose.json")
    print("\n### E2a vét cạn")
    print("| Rollout | it | Số ván có thể (MCTS là X / O) | Thua | Thắng | Hòa | Quyết định tối ưu |")
    print("|---|---|---|---|---|---|---|")
    for ro in ("random", "heuristic"):
        its = sorted({r["it"] for r in d["exhaustive"]})
        for it in its:
            rs = [r for r in d["exhaustive"] if r["it"] == it and r["rollout"] == ro]
            lx = sum(r["lines"] for r in rs if r["side"] == 0)
            lo = sum(r["lines"] for r in rs if r["side"] == 1)
            L = sum(r["loss"] for r in rs)
            print(f"| {ro} | {it} | {lx} / {lo} | {L} | {sum(r['win'] for r in rs)} | {sum(r['draw'] for r in rs)} | "
                  f"{pct(sum(r['optimal'] for r in rs) / sum(r['decisions'] for r in rs))} |")
    print("\n### E2b đấu loạt 3x3")
    print_matches(d["matches"])


def print_matches(ms):
    print("| Cấu hình | Ván | Thắng | Hòa | Thua | Thắng/Hòa/Thua khi đi trước | ... khi đi sau | ms/nước |")
    print("|---|---|---|---|---|---|---|---|")
    for tag, s in ms.items():
        print(f"| {tag} | {s['games']} | {s['win']} | {s['draw']} | {s['loss']} | "
              f"{s['win_first']}/{s['draw_first']}/{s['loss_first']} | {s['win_second']}/{s['draw_second']}/{s['loss_second']} | "
              f"{s['ms_per_move_a']:.1f} |")


def e3():
    d = load("e3_c_sweep.json")
    for key, opp, fld, its in (("3x3", "random", "win_rate", d["it3"]), ("3x3", "perfect", "nonloss_rate", d["it3"]),
                               ("9x9", "epsgreedy", "win_rate", d["it9"])):
        if key not in d:
            continue
        print(f"\n### E3 {key} vs {opp} ({fld})")
        print("| c | " + " | ".join(str(i) for i in its) + " |")
        print("|---|" + "---|" * len(its))
        for c in d["cs"]:
            print(f"| {c} | " + " | ".join(pct(d[key][f"{key}|{opp}|{c}|{it}"][fld]) for it in its) + " |")
    if "9x9" in d:
        print("\nms/nước 9x9:", {it: round(d["9x9"][f"9x9|epsgreedy|1.4|{it}"]["ms_per_move_a"]) for it in d["it9"]})


def e4():
    d = load("e4_root_stats.json")
    for k in ("table_empty_100", "table_empty_1000", "table_tricky_200", "table_tricky_1000"):
        print(f"\n### {k}")
        print("| Nước | W | N | W/N | UCT | Giá trị minimax |")
        print("|---|---|---|---|---|---|")
        for r in d[k]:
            print(f"| {r['move']} | {r['W']:.1f} | {r['N']} | {r['W/N']:.3f} | {r['UCT']:.3f} | {r['minimax']} |")
    print("\n", d["pos_tricky"])
    print("\n### disagreement")
    for r in d["disagreement"]:
        n = r["positions"]
        print(r["it"], pct(r["disagree"] / n), pct(r["robust_optimal"] / n), pct(r["ratio_optimal"] / n))
    if "matches" in d:
        print_matches(d["matches"])


def e5():
    d = load("e5_rollout.json")
    print("\n### E5 quality", d["n_positions"], d["n_win"])
    for k, v in d["quality"].items():
        print(k, {a: round(b, 3) for a, b in v.items()})
    for key in ("3x3", "9x9"):
        if key in d:
            print(f"\n### E5 {key}")
            print_matches(d[key])


def e6():
    d = load("e6_xiangqi.json")
    print("\n### E6 perft")
    for r in d["perft"]:
        print(r)
    print("| Thế cờ | d | Minimax | Alpha-Beta | AB + MVV-LVA | Cùng giá trị |")
    print("|---|---|---|---|---|---|")
    for r in d["nodes"]:
        print(f"| {r['pos']} | {r['depth']} | {f_int(r['minimax']['nodes'])} ({r['minimax']['time']:.2f} s) | "
              f"{f_int(r['ab']['nodes'])} | {f_int(r['ab_mvvlva']['nodes'])} ({r['ab_mvvlva']['time']:.2f} s) | {r['same_value']} |")
    if "matches" in d:
        print_matches(d["matches"])
        for t, s in d["matches"].items():
            print(t, "avg plies", round(s["avg_plies"]))


if __name__ == "__main__":
    for f in (e1, e2, e3, e4, e5, e6):
        try:
            f()
        except FileNotFoundError:
            print("(chưa có)", f.__name__)
