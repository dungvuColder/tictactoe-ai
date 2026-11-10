# BTL Trí tuệ nhân tạo — Bài 1: Tic-Tac-Toe 5 quân với Minimax, Alpha-Beta và MCTS-UCT (+ Cờ tướng)

Mã nguồn Python thuần (chỉ cần `matplotlib` để vẽ đồ thị, `pygame` cho giao diện đồ họa).

## Cài đặt

```bash
pip install -r requirements.txt      # matplotlib, pygame (pygame chỉ cần cho gui.py)
python tests/test_all.py             # 8 bài kiểm thử, ~10 giây
```

## Chơi thử

```bash
# Giao diện đồ họa (click chuột để đi; R = ván mới; Esc = thoát)
python gui.py --game caro --size 9 --ai mcts-h --iters 3000      # bạn (X) vs MCTS rollout heuristic
python gui.py --game caro --size 15 --ai ab --depth 3 --ai-first  # Alpha-Beta đi trước
python gui.py --game ttt --ai mcts --iters 2000                   # Tic-Tac-Toe 3×3
python gui.py --game xiangqi --ai ab --depth 3                    # Cờ tướng, bạn cầm Đỏ
python gui.py --game caro --p1 ab --ai mcts-h                     # máy vs máy

# Terminal
python play.py --game caro --p1 human --p2 ab --depth 3           # nhập "hàng cột", vd: 4 4
python play.py --game xiangqi --p1 human --p2 mcts-h --iters 800  # nhập vd: h2e2
```

Các loại agent: `random`, `greedy`, `minimax` (hoàn hảo, chỉ 3×3), `ab` (Alpha-Beta + iterative deepening),
`mcts` (UCT, rollout ngẫu nhiên), `mcts-h` (UCT, rollout heuristic; với Cờ tướng là rollout ngắn + lượng giá).
Tham số: `--iters`, `--c`, `--depth`, `--time`.

## Cấu trúc

```
games/
  gomoku.py             Tic-Tac-Toe m×m, k quân (bitboard), rollout ngẫu nhiên nhanh
  gomoku_heuristics.py  hàm lượng giá theo cửa sổ, move ordering, ô thắng ngay, rollout heuristic
  xiangqi.py            Cờ tướng: luật đầy đủ, kiểm tra chiếu, perft, lượng giá, rollout
agents/
  minimax.py            Minimax / Alpha-Beta (MAX-VALUE, MIN-VALUE), AlphaBetaAgent, PerfectTTTAgent
  mcts.py               MCTS-UCT độc lập trò chơi; chọn nước theo N (robust) hoặc W/N
  baselines.py          Random, Greedy, EpsilonGreedy, hàm tạo agent
  xiangqi_agents.py     agent cho Cờ tướng
experiments/
  exp1_nodes.py         E1: số nút Minimax vs Alpha-Beta (3×3 toàn cây; 9×9 độ sâu 1–4)
  exp2_never_lose.py    E2: kiểm chứng VÉT CẠN MCTS không thua ở 3×3 + đấu loạt
  exp3_c_sweep.py       E3: c ∈ {0.5,1,1.4,2} × iteration (3×3 và 9×9)
  exp4_root_stats.py    E4: bảng W, N, W/N tại gốc; N vs W/N
  exp5_rollout.py       E5: rollout ngẫu nhiên vs heuristic
  exp6_xiangqi.py       E6: Cờ tướng (perft, số nút, đấu loạt); exp2b, exp4b, exp6b: thực nghiệm bổ sung
  report_tables.py      in các bảng kết quả (results/tables.md)
  make_figures.py       vẽ đồ thị vào results/figures/
  run_all.sh            chạy lại toàn bộ (~2 giờ trên 2 nhân CPU)
results/                kết quả JSON, log và hình (đã chạy sẵn)
gui.py, play.py         giao diện đồ họa / terminal
```

## Tái lập thực nghiệm

```bash
cd experiments
NPROC=4 python exp3_c_sweep.py 100 50    # tham số: số ván 3×3, số ván 9×9
python make_figures.py
```
Mọi thực nghiệm dùng seed cố định; mỗi cấu hình ≥ 50 ván, đổi lượt đi trước giữa các ván
(ván chẵn agent A đi trước, ván lẻ agent B đi trước).
