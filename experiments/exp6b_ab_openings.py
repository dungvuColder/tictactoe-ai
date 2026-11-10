"""E6b — Alpha-Beta (tất định) đấu với nhau từ khai cuộc ngẫu nhiên 4 nửa nước (cặp ván đổi màu),
để 20 ván là 10 khai cuộc khác nhau thay vì lặp lại 1 ván."""
import sys
from common import run_matches, save

if __name__ == "__main__":
    games = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    G = ("xiangqi", 200, 4)
    AB1, AB2, AB3 = ("xq_ab", {"depth": 1}), ("xq_ab", {"depth": 2}), ("xq_ab", {"depth": 3})
    ME = ("xq_mcts", {"iterations": 500, "rollout": "eval"})
    m = [("AB2 vs AB1 (khai cuộc ngẫu nhiên)", G, AB2, AB1),
         ("AB3 vs AB2 (khai cuộc ngẫu nhiên)", G, AB3, AB2),
         ("MCTS-eval vs AB1 (khai cuộc ngẫu nhiên)", G, ME, AB1)]
    out = run_matches(m, games=games, seed=62, log="E6b")
    save("e6b_ab_openings.json", out)
    for k, v in out.items():
        print(k, v["win"], v["draw"], v["loss"], v["win_first"], v["draw_first"], v["loss_first"], round(v["avg_plies"]))
