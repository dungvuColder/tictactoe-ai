#!/bin/bash
# Chạy lại toàn bộ thực nghiệm trong báo cáo (~1,5–2 giờ trên 2 nhân CPU). Log và JSON ghi vào results/.
cd "$(dirname "$0")"
export NPROC=${NPROC:-2}
python3 exp1_nodes.py               > ../results/log_exp1.txt 2>&1
python3 exp2_never_lose.py 100      > ../results/log_exp2.txt 2>&1
python3 exp2b_never_lose_more.py    > ../results/log_exp2b.txt 2>&1
python3 exp3_c_sweep.py 100 50      > ../results/log_e3.txt 2>&1
python3 exp4_root_stats.py 100      > ../results/log_exp4.txt 2>&1
python3 exp4b_low_budget.py         > ../results/log_exp4b.txt 2>&1
python3 exp5_rollout.py 50          > ../results/log_exp5.txt 2>&1
python3 exp6_xiangqi.py 20          > ../results/log_exp6.txt 2>&1
python3 exp6b_ab_openings.py 20     > ../results/log_exp6b.txt 2>&1
python3 make_figures.py
python3 report_tables.py            > ../results/tables.md
