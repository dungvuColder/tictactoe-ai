# Độ dao động trong cùng nhiệm vụ

Thống kê thời gian chỉ dùng các lượt success của từng biến thể. Q1, Q3 và IQR được tính bằng nội suy phân vị khi có ít nhất ba lượt success. Schema cũ có một lượt nên độ phân tán không có.

| Nhiệm vụ | Thuật toán | Ghi/kỳ vọng | Success | No path | Timeout | Giới hạn nút | Hủy | Trung vị (ms) | Q1 (ms) | Q3 (ms) | IQR (ms) | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| single-uniform-12-d10-s11-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8067 | 0.7245 | 0.8082 | 0.0837 | — |
| single-uniform-12-d10-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.03 | 0.7501 | 1.069 | 0.3186 | — |
| single-uniform-12-d10-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.4649 | 0.4128 | 0.4922 | 0.0794 | — |
| single-uniform-12-d10-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8314 | 0.8007 | 0.8396 | 0.0389 | — |
| single-uniform-12-d10-s29-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7549 | 0.7413 | 0.7628 | 0.0215 | — |
| single-uniform-12-d10-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.825 | 0.7856 | 0.8495 | 0.0639 | — |
| single-uniform-12-d10-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.2755 | 0.261 | 0.3048 | 0.0438 | — |
| single-uniform-12-d10-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.075 | 0.8804 | 1.227 | 0.3466 | — |
| single-uniform-12-d10-s47-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.206 | 1.132 | 1.428 | 0.2961 | — |
| single-uniform-12-d10-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8588 | 0.857 | 0.9608 | 0.1038 | — |
| single-uniform-12-d10-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.303 | 0.2755 | 0.4854 | 0.2099 | — |
| single-uniform-12-d10-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.9914 | 0.9697 | 1.001 | 0.0309 | — |
| single-uniform-12-d10-s71-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.175 | 1.142 | 1.24 | 0.098 | — |
| single-uniform-12-d10-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.153 | 0.8131 | 1.165 | 0.3515 | — |
| single-uniform-12-d10-s71-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.2697 | 0.2693 | 0.2749 | 0.0056 | — |
| single-uniform-12-d10-s71-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8593 | 0.8399 | 0.8921 | 0.0522 | — |
| single-uniform-12-d10-s101-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7246 | 0.7069 | 0.8375 | 0.1306 | — |
| single-uniform-12-d10-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7553 | 0.7532 | 0.7727 | 0.0195 | — |
| single-uniform-12-d10-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.2755 | 0.2638 | 0.3183 | 0.0545 | — |
| single-uniform-12-d10-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8526 | 0.8493 | 0.9743 | 0.125 | — |
| single-uniform-12-d10-s137-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8955 | 0.8497 | 1.057 | 0.207 | — |
| single-uniform-12-d10-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8435 | 0.8357 | 0.9429 | 0.1072 | — |
| single-uniform-12-d10-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.2715 | 0.2653 | 0.3019 | 0.0366 | — |
| single-uniform-12-d10-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.9794 | 0.9583 | 1.709 | 0.7511 | — |
| single-uniform-12-d25-s11-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.6584 | 0.6371 | 0.6726 | 0.0355 | — |
| single-uniform-12-d25-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.5991 | 0.5823 | 0.6637 | 0.0814 | — |
| single-uniform-12-d25-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.3392 | 0.293 | 0.3484 | 0.0554 | — |
| single-uniform-12-d25-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.4736 | 0.4725 | 0.4902 | 0.0177 | — |
| single-uniform-12-d25-s29-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7256 | 0.7158 | 0.8957 | 0.1799 | — |
| single-uniform-12-d25-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7129 | 0.7112 | 0.8783 | 0.1671 | — |
| single-uniform-12-d25-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.3095 | 0.2934 | 0.3205 | 0.0271 | — |
| single-uniform-12-d25-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7042 | 0.6988 | 1.076 | 0.3773 | — |
| single-uniform-12-d25-s47-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7039 | 0.6786 | 0.8628 | 0.1842 | — |
| single-uniform-12-d25-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7278 | 0.7226 | 0.7691 | 0.0465 | — |
| single-uniform-12-d25-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.3509 | 0.3501 | 0.4344 | 0.0843 | — |
| single-uniform-12-d25-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7405 | 0.731 | 0.744 | 0.013 | — |
| single-uniform-12-d25-s71-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d25-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d25-s71-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d25-s71-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d25-s101-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.6991 | 0.5648 | 0.7017 | 0.1369 | — |
| single-uniform-12-d25-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.6452 | 0.6301 | 1.003 | 0.3727 | — |
| single-uniform-12-d25-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.3605 | 0.3601 | 0.4292 | 0.0691 | — |
| single-uniform-12-d25-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.6312 | 0.6169 | 0.812 | 0.1951 | — |
| single-uniform-12-d25-s137-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7918 | 0.6918 | 0.9975 | 0.3057 | — |
| single-uniform-12-d25-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.704 | 0.6976 | 0.7228 | 0.0252 | — |
| single-uniform-12-d25-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.3525 | 0.2731 | 0.3814 | 0.1083 | — |
| single-uniform-12-d25-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.6102 | 0.5755 | 0.7032 | 0.1277 | — |
| single-uniform-12-d40-s11-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s11-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s11-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s11-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s29-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s29-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s29-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s29-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s47-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s47-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s47-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s47-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s71-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s71-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s71-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s101-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s101-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s101-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s101-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s137-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s137-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s137-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-12-d40-s137-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d10-s11-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.101 | 2.918 | 3.217 | 0.2989 | — |
| single-uniform-24-d10-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.331 | 3.112 | 3.53 | 0.4182 | — |
| single-uniform-24-d10-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.5024 | 0.499 | 0.6832 | 0.1842 | — |
| single-uniform-24-d10-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.343 | 3.28 | 3.36 | 0.0807 | — |
| single-uniform-24-d10-s29-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.836 | 2.788 | 2.936 | 0.1478 | — |
| single-uniform-24-d10-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.553 | 3.16 | 3.943 | 0.7835 | — |
| single-uniform-24-d10-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.5429 | 0.5303 | 0.5432 | 0.0129 | — |
| single-uniform-24-d10-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.995 | 2.992 | 3.224 | 0.2322 | — |
| single-uniform-24-d10-s47-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.035 | 4.266 | 6.199 | 1.933 | — |
| single-uniform-24-d10-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.31 | 5.873 | 7.97 | 2.097 | — |
| single-uniform-24-d10-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.122 | 1.08 | 1.268 | 0.1882 | — |
| single-uniform-24-d10-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.439 | 4.933 | 6.566 | 1.633 | — |
| single-uniform-24-d10-s71-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.519 | 5.081 | 6.596 | 1.515 | — |
| single-uniform-24-d10-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.7 | 4.259 | 4.935 | 0.6758 | — |
| single-uniform-24-d10-s71-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.251 | 0.8588 | 1.308 | 0.4487 | — |
| single-uniform-24-d10-s71-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.361 | 5.275 | 5.691 | 0.4159 | — |
| single-uniform-24-d10-s101-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.064 | 4.456 | 6.139 | 1.683 | — |
| single-uniform-24-d10-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.555 | 6.243 | 7.125 | 0.8822 | — |
| single-uniform-24-d10-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.168 | 0.7391 | 1.249 | 0.5102 | — |
| single-uniform-24-d10-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.317 | 5.199 | 6.073 | 0.8738 | — |
| single-uniform-24-d10-s137-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.417 | 4.733 | 5.44 | 0.707 | — |
| single-uniform-24-d10-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.897 | 4.685 | 5.78 | 1.094 | — |
| single-uniform-24-d10-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.057 | 0.9571 | 1.193 | 0.2364 | — |
| single-uniform-24-d10-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.417 | 5.356 | 5.992 | 0.6363 | — |
| single-uniform-24-d25-s11-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.535 | 3.528 | 5.13 | 1.602 | — |
| single-uniform-24-d25-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.078 | 4.077 | 4.809 | 0.732 | — |
| single-uniform-24-d25-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.9162 | 0.7411 | 1.201 | 0.4598 | — |
| single-uniform-24-d25-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.316 | 2.097 | 4.427 | 2.33 | — |
| single-uniform-24-d25-s29-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d25-s29-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d25-s29-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d25-s29-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d25-s47-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.864 | 3.593 | 4.303 | 0.7098 | — |
| single-uniform-24-d25-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.42 | 3.723 | 4.858 | 1.134 | — |
| single-uniform-24-d25-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.9916 | 0.836 | 1.07 | 0.2339 | — |
| single-uniform-24-d25-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.465 | 3.447 | 4.464 | 1.017 | — |
| single-uniform-24-d25-s71-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d25-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d25-s71-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d25-s71-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d25-s101-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.305 | 3.548 | 4.399 | 0.851 | — |
| single-uniform-24-d25-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.79 | 3.626 | 4.231 | 0.6045 | — |
| single-uniform-24-d25-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.027 | 0.8553 | 1.109 | 0.2534 | — |
| single-uniform-24-d25-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.08 | 3.04 | 3.366 | 0.3255 | — |
| single-uniform-24-d25-s137-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.503 | 3.256 | 3.861 | 0.6049 | — |
| single-uniform-24-d25-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.965 | 3.728 | 4.791 | 1.063 | — |
| single-uniform-24-d25-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.136 | 1.071 | 1.296 | 0.2249 | — |
| single-uniform-24-d25-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.335 | 2.421 | 3.371 | 0.9494 | — |
| single-uniform-24-d40-s11-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s11-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s11-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s11-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s29-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s29-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s29-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s29-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s47-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s47-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s47-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s47-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s71-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s71-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s71-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s101-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s101-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s101-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s101-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s137-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s137-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s137-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-24-d40-s137-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d10-s11-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.49 | 11.28 | 12.7 | 1.424 | — |
| single-uniform-40-d10-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 12.98 | 12.1 | 13.92 | 1.825 | — |
| single-uniform-40-d10-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.527 | 1.303 | 2.002 | 0.6986 | — |
| single-uniform-40-d10-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 20.08 | 19.28 | 20.18 | 0.8957 | — |
| single-uniform-40-d10-s29-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.85 | 11.05 | 13.2 | 2.144 | — |
| single-uniform-40-d10-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 12.62 | 12.59 | 12.65 | 0.0509 | — |
| single-uniform-40-d10-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.458 | 1.411 | 2.113 | 0.7014 | — |
| single-uniform-40-d10-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 15.97 | 14.37 | 16.02 | 1.648 | — |
| single-uniform-40-d10-s47-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.22 | 11.18 | 13.63 | 2.444 | — |
| single-uniform-40-d10-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 13.9 | 13.8 | 13.96 | 0.1586 | — |
| single-uniform-40-d10-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.495 | 1.293 | 1.511 | 0.218 | — |
| single-uniform-40-d10-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 12.63 | 11.42 | 12.71 | 1.293 | — |
| single-uniform-40-d10-s71-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.92 | 10.59 | 10.95 | 0.3663 | — |
| single-uniform-40-d10-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 12.11 | 11.58 | 12.53 | 0.9538 | — |
| single-uniform-40-d10-s71-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.325 | 1.294 | 1.595 | 0.3011 | — |
| single-uniform-40-d10-s71-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 12.58 | 12.4 | 12.79 | 0.3898 | — |
| single-uniform-40-d10-s101-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.07 | 10.96 | 11.13 | 0.1694 | — |
| single-uniform-40-d10-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 15.04 | 12.56 | 16.34 | 3.776 | — |
| single-uniform-40-d10-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.543 | 1.319 | 2.026 | 0.7068 | — |
| single-uniform-40-d10-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 13.76 | 12.56 | 18.37 | 5.81 | — |
| single-uniform-40-d10-s137-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 13.33 | 12.09 | 13.55 | 1.459 | — |
| single-uniform-40-d10-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 13.06 | 13.03 | 13.13 | 0.1049 | — |
| single-uniform-40-d10-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.067 | 1.03 | 1.071 | 0.0408 | — |
| single-uniform-40-d10-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 14.16 | 13.41 | 14.64 | 1.234 | — |
| single-uniform-40-d25-s11-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 12.29 | 10.97 | 12.93 | 1.956 | — |
| single-uniform-40-d25-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 13.41 | 12.11 | 14.09 | 1.982 | — |
| single-uniform-40-d25-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.936 | 1.629 | 1.987 | 0.3574 | — |
| single-uniform-40-d25-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.872 | 6.402 | 7.939 | 1.537 | — |
| single-uniform-40-d25-s29-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.78 | 10.04 | 13.74 | 3.7 | — |
| single-uniform-40-d25-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.35 | 10.28 | 11.5 | 1.219 | — |
| single-uniform-40-d25-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.673 | 1.475 | 2.156 | 0.6808 | — |
| single-uniform-40-d25-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.265 | 7.911 | 8.754 | 0.8427 | — |
| single-uniform-40-d25-s47-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 9.585 | 9.267 | 9.798 | 0.5316 | — |
| single-uniform-40-d25-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 14.63 | 13.75 | 16.36 | 2.613 | — |
| single-uniform-40-d25-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.336 | 1.193 | 1.958 | 0.7646 | — |
| single-uniform-40-d25-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.907 | 5.589 | 6.4 | 0.8112 | — |
| single-uniform-40-d25-s71-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 9.891 | 8.722 | 10.3 | 1.579 | — |
| single-uniform-40-d25-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.64 | 9.998 | 11.28 | 1.279 | — |
| single-uniform-40-d25-s71-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.401 | 1.181 | 1.528 | 0.347 | — |
| single-uniform-40-d25-s71-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.764 | 6.744 | 6.9 | 0.1555 | — |
| single-uniform-40-d25-s101-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.42 | 9.824 | 11.64 | 1.817 | — |
| single-uniform-40-d25-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.24 | 10.24 | 12.6 | 2.355 | — |
| single-uniform-40-d25-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.546 | 1.473 | 2.069 | 0.5956 | — |
| single-uniform-40-d25-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.846 | 8.647 | 8.908 | 0.261 | — |
| single-uniform-40-d25-s137-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.478 | 8.281 | 8.789 | 0.508 | — |
| single-uniform-40-d25-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 9.723 | 9.119 | 9.951 | 0.8316 | — |
| single-uniform-40-d25-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.857 | 1.606 | 1.956 | 0.3498 | — |
| single-uniform-40-d25-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 7.184 | 6.971 | 7.464 | 0.493 | — |
| single-uniform-40-d40-s11-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s11-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s11-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s11-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s29-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s29-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s29-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s29-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s47-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s47-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s47-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s47-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s71-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s71-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s71-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s101-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s101-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s101-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s101-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s137-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s137-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s137-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-40-d40-s137-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d10-s11-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 31.41 | 31.04 | 32.56 | 1.519 | — |
| single-uniform-64-d10-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 40.49 | 34.68 | 44.89 | 10.21 | — |
| single-uniform-64-d10-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.217 | 1.844 | 2.826 | 0.9815 | — |
| single-uniform-64-d10-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 34.4 | 32.5 | 34.91 | 2.416 | — |
| single-uniform-64-d10-s29-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 32.26 | 30.63 | 32.74 | 2.106 | — |
| single-uniform-64-d10-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 33.05 | 31.69 | 34.55 | 2.857 | — |
| single-uniform-64-d10-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.277 | 2.093 | 2.964 | 0.8711 | — |
| single-uniform-64-d10-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 33.54 | 33.36 | 33.6 | 0.2351 | — |
| single-uniform-64-d10-s47-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 30.56 | 30.27 | 32.48 | 2.205 | — |
| single-uniform-64-d10-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 41.95 | 32.32 | 43.17 | 10.85 | — |
| single-uniform-64-d10-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.511 | 2.119 | 3.487 | 1.368 | — |
| single-uniform-64-d10-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 35.74 | 35.32 | 50.28 | 14.96 | — |
| single-uniform-64-d10-s71-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 31.33 | 30.94 | 35.06 | 4.126 | — |
| single-uniform-64-d10-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 35.31 | 32.9 | 37.1 | 4.197 | — |
| single-uniform-64-d10-s71-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.328 | 2.29 | 2.337 | 0.0467 | — |
| single-uniform-64-d10-s71-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 36.18 | 35.23 | 40.77 | 5.544 | — |
| single-uniform-64-d10-s101-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 30.81 | 28.44 | 30.84 | 2.407 | — |
| single-uniform-64-d10-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 33.99 | 32.19 | 39.6 | 7.412 | — |
| single-uniform-64-d10-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.482 | 2.036 | 2.914 | 0.8782 | — |
| single-uniform-64-d10-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 31.83 | 31.6 | 32.24 | 0.6321 | — |
| single-uniform-64-d10-s137-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 29.59 | 29.48 | 29.84 | 0.3554 | — |
| single-uniform-64-d10-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 33.03 | 32.46 | 33.56 | 1.107 | — |
| single-uniform-64-d10-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.904 | 2.456 | 2.913 | 0.4573 | — |
| single-uniform-64-d10-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 37.82 | 34.58 | 40.87 | 6.286 | — |
| single-uniform-64-d25-s11-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 23.87 | 23.69 | 29.97 | 6.279 | — |
| single-uniform-64-d25-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 27.28 | 26.23 | 27.62 | 1.384 | — |
| single-uniform-64-d25-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.955 | 2.573 | 3.234 | 0.6611 | — |
| single-uniform-64-d25-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 17.02 | 16.78 | 17.14 | 0.3649 | — |
| single-uniform-64-d25-s29-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 24.08 | 23.65 | 24.91 | 1.259 | — |
| single-uniform-64-d25-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 25.29 | 23.87 | 27 | 3.134 | — |
| single-uniform-64-d25-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.49 | 2.257 | 2.509 | 0.2516 | — |
| single-uniform-64-d25-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 19.5 | 19.37 | 20.33 | 0.9651 | — |
| single-uniform-64-d25-s47-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 32.04 | 30.94 | 32.31 | 1.368 | — |
| single-uniform-64-d25-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 35.25 | 28.51 | 36.59 | 8.084 | — |
| single-uniform-64-d25-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.646 | 3.447 | 4.614 | 1.167 | — |
| single-uniform-64-d25-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 22.74 | 15.58 | 23.09 | 7.501 | — |
| single-uniform-64-d25-s71-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 24.89 | 23.01 | 28.1 | 5.09 | — |
| single-uniform-64-d25-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 26.87 | 26.67 | 27.11 | 0.4478 | — |
| single-uniform-64-d25-s71-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.249 | 2.131 | 2.32 | 0.1887 | — |
| single-uniform-64-d25-s71-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 18.25 | 17.73 | 18.47 | 0.7418 | — |
| single-uniform-64-d25-s101-p1 | BFS | 5/5 | 5 | 0 | 0 | 0 | 0 | 23.74 | 22.55 | 23.89 | 1.341 | — |
| single-uniform-64-d25-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 25.67 | 24.9 | 25.78 | 0.8799 | — |
| single-uniform-64-d25-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.273 | 3.187 | 3.607 | 0.4195 | — |
| single-uniform-64-d25-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 16.13 | 13.88 | 16.91 | 3.032 | — |
| single-uniform-64-d25-s137-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d25-s137-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d25-s137-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d25-s137-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s11-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s11-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s11-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s11-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s29-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s29-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s29-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s29-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s47-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s47-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s47-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s47-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s71-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s71-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s71-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s101-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s101-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s101-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s101-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s137-p1 | BFS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s137-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s137-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-64-d40-s137-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d10-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.48 | 1.173 | 1.937 | 0.7645 | — |
| single-weighted-12-d10-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.5689 | 0.5339 | 0.9426 | 0.4087 | — |
| single-weighted-12-d10-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.114 | 2.006 | 2.379 | 0.373 | — |
| single-weighted-12-d10-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.2 | 1.157 | 1.21 | 0.0529 | — |
| single-weighted-12-d10-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.3802 | 0.2951 | 0.3888 | 0.0937 | — |
| single-weighted-12-d10-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.801 | 1.361 | 2.323 | 0.9612 | — |
| single-weighted-12-d10-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.387 | 1.212 | 1.517 | 0.3048 | — |
| single-weighted-12-d10-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.411 | 0.399 | 0.5985 | 0.1995 | — |
| single-weighted-12-d10-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.392 | 1.205 | 1.394 | 0.1892 | — |
| single-weighted-12-d10-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.088 | 1.048 | 1.16 | 0.1122 | — |
| single-weighted-12-d10-s71-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.387 | 0.3859 | 0.4472 | 0.0613 | — |
| single-weighted-12-d10-s71-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.494 | 1.355 | 1.496 | 0.1415 | — |
| single-weighted-12-d10-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.241 | 1.181 | 1.525 | 0.3436 | — |
| single-weighted-12-d10-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.3662 | 0.3551 | 0.3856 | 0.0305 | — |
| single-weighted-12-d10-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.418 | 1.148 | 1.89 | 0.7427 | — |
| single-weighted-12-d10-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.492 | 1.046 | 1.828 | 0.7818 | — |
| single-weighted-12-d10-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.338 | 0.3158 | 0.4363 | 0.1205 | — |
| single-weighted-12-d10-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.659 | 1.6 | 1.79 | 0.1906 | — |
| single-weighted-12-d25-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7984 | 0.7714 | 0.8413 | 0.0699 | — |
| single-weighted-12-d25-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.491 | 0.431 | 0.7469 | 0.3159 | — |
| single-weighted-12-d25-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.636 | 1.405 | 1.705 | 0.3002 | — |
| single-weighted-12-d25-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.9332 | 0.8365 | 1.067 | 0.2302 | — |
| single-weighted-12-d25-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.5633 | 0.4182 | 0.5939 | 0.1757 | — |
| single-weighted-12-d25-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.296 | 1.254 | 1.595 | 0.3409 | — |
| single-weighted-12-d25-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.112 | 1.073 | 1.336 | 0.2627 | — |
| single-weighted-12-d25-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.6155 | 0.5376 | 0.7399 | 0.2023 | — |
| single-weighted-12-d25-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.162 | 1.12 | 1.305 | 0.1852 | — |
| single-weighted-12-d25-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d25-s71-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d25-s71-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d25-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.052 | 0.9077 | 1.106 | 0.1987 | — |
| single-weighted-12-d25-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.4786 | 0.4208 | 0.6852 | 0.2644 | — |
| single-weighted-12-d25-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.409 | 1.153 | 1.713 | 0.5594 | — |
| single-weighted-12-d25-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.625 | 1.552 | 1.694 | 0.1423 | — |
| single-weighted-12-d25-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.5578 | 0.4232 | 0.6074 | 0.1842 | — |
| single-weighted-12-d25-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.519 | 1.395 | 1.975 | 0.5799 | — |
| single-weighted-12-d40-s11-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s11-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s11-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s29-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s29-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s29-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s47-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s47-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s47-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s71-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s71-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s101-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s101-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s101-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s137-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s137-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-12-d40-s137-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d10-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 7.209 | 6.858 | 7.57 | 0.7126 | — |
| single-weighted-24-d10-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8599 | 0.8468 | 0.9002 | 0.0534 | — |
| single-weighted-24-d10-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.597 | 7.8 | 8.799 | 0.9992 | — |
| single-weighted-24-d10-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.077 | 4.785 | 6.611 | 1.826 | — |
| single-weighted-24-d10-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.084 | 0.7922 | 1.108 | 0.3157 | — |
| single-weighted-24-d10-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.141 | 6.022 | 8.247 | 2.225 | — |
| single-weighted-24-d10-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.114 | 5.097 | 5.302 | 0.2048 | — |
| single-weighted-24-d10-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.789 | 0.7317 | 1.15 | 0.4185 | — |
| single-weighted-24-d10-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.902 | 5.696 | 6.018 | 0.322 | — |
| single-weighted-24-d10-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.412 | 4.341 | 4.575 | 0.234 | — |
| single-weighted-24-d10-s71-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8081 | 0.7645 | 0.8716 | 0.1071 | — |
| single-weighted-24-d10-s71-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.146 | 5.478 | 7.74 | 2.261 | — |
| single-weighted-24-d10-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.169 | 5.011 | 5.522 | 0.5117 | — |
| single-weighted-24-d10-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.697 | 0.6854 | 0.7725 | 0.0871 | — |
| single-weighted-24-d10-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.302 | 5.087 | 6.345 | 1.257 | — |
| single-weighted-24-d10-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.103 | 4.365 | 5.363 | 0.9985 | — |
| single-weighted-24-d10-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.027 | 0.9093 | 1.178 | 0.2685 | — |
| single-weighted-24-d10-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.075 | 5.629 | 6.19 | 0.5605 | — |
| single-weighted-24-d25-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.309 | 4.275 | 4.882 | 0.6071 | — |
| single-weighted-24-d25-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.145 | 0.8118 | 1.183 | 0.3709 | — |
| single-weighted-24-d25-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.396 | 4.261 | 4.58 | 0.3191 | — |
| single-weighted-24-d25-s29-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d25-s29-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d25-s29-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d25-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.634 | 5.552 | 6.136 | 0.5842 | — |
| single-weighted-24-d25-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.224 | 1.181 | 1.405 | 0.2242 | — |
| single-weighted-24-d25-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.735 | 4.169 | 7.311 | 3.142 | — |
| single-weighted-24-d25-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d25-s71-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d25-s71-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d25-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.464 | 3.04 | 3.548 | 0.5077 | — |
| single-weighted-24-d25-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8203 | 0.7507 | 0.8802 | 0.1295 | — |
| single-weighted-24-d25-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.577 | 4.337 | 5.092 | 0.7554 | — |
| single-weighted-24-d25-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.792 | 3.194 | 4.004 | 0.8094 | — |
| single-weighted-24-d25-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.9666 | 0.9631 | 1.393 | 0.4303 | — |
| single-weighted-24-d25-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.851 | 3.837 | 4.42 | 0.5837 | — |
| single-weighted-24-d40-s11-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s11-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s11-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s29-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s29-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s29-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s47-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s47-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s47-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s71-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s71-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s101-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s101-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s101-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s137-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s137-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-24-d40-s137-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d10-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 12.97 | 12.72 | 13.27 | 0.5454 | — |
| single-weighted-40-d10-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.32 | 1.243 | 1.646 | 0.4037 | — |
| single-weighted-40-d10-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 14.65 | 14.55 | 16.47 | 1.915 | — |
| single-weighted-40-d10-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 12.88 | 12.35 | 15.71 | 3.36 | — |
| single-weighted-40-d10-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.192 | 1.154 | 2.183 | 1.028 | — |
| single-weighted-40-d10-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 14.02 | 14 | 20.87 | 6.877 | — |
| single-weighted-40-d10-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 12.16 | 12.14 | 13.3 | 1.16 | — |
| single-weighted-40-d10-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.21 | 1.097 | 1.6 | 0.5031 | — |
| single-weighted-40-d10-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 15.53 | 14.84 | 21.29 | 6.452 | — |
| single-weighted-40-d10-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 17.06 | 13.28 | 18.75 | 5.464 | — |
| single-weighted-40-d10-s71-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.146 | 0.954 | 1.329 | 0.3746 | — |
| single-weighted-40-d10-s71-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 15.41 | 15 | 17.28 | 2.274 | — |
| single-weighted-40-d10-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 13.84 | 13.73 | 14.72 | 0.9908 | — |
| single-weighted-40-d10-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.293 | 1.238 | 1.316 | 0.0776 | — |
| single-weighted-40-d10-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 15.38 | 14.72 | 15.59 | 0.8735 | — |
| single-weighted-40-d10-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 12.72 | 12.56 | 12.87 | 0.3123 | — |
| single-weighted-40-d10-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.417 | 1.087 | 1.544 | 0.4564 | — |
| single-weighted-40-d10-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 16.66 | 15.6 | 19.87 | 4.272 | — |
| single-weighted-40-d25-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 9.915 | 9.906 | 10.01 | 0.1023 | — |
| single-weighted-40-d25-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.483 | 1.378 | 2.082 | 0.7049 | — |
| single-weighted-40-d25-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.99 | 11.82 | 12.45 | 0.6344 | — |
| single-weighted-40-d25-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.21 | 9.276 | 12.15 | 2.879 | — |
| single-weighted-40-d25-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.579 | 1.477 | 1.783 | 0.3065 | — |
| single-weighted-40-d25-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 12.09 | 10.88 | 12.54 | 1.658 | — |
| single-weighted-40-d25-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 13.69 | 13.68 | 14.02 | 0.3395 | — |
| single-weighted-40-d25-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.304 | 1.153 | 2.027 | 0.8738 | — |
| single-weighted-40-d25-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 14 | 12.72 | 15.16 | 2.442 | — |
| single-weighted-40-d25-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.26 | 10.21 | 10.3 | 0.0863 | — |
| single-weighted-40-d25-s71-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.309 | 1.3 | 1.704 | 0.4039 | — |
| single-weighted-40-d25-s71-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 13.93 | 13.46 | 14.3 | 0.8378 | — |
| single-weighted-40-d25-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.25 | 9.782 | 11.3 | 1.522 | — |
| single-weighted-40-d25-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.38 | 1.352 | 1.723 | 0.3705 | — |
| single-weighted-40-d25-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.51 | 11.43 | 12.47 | 1.036 | — |
| single-weighted-40-d25-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 9.499 | 9.334 | 10.36 | 1.03 | — |
| single-weighted-40-d25-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.775 | 2.702 | 2.839 | 0.1371 | — |
| single-weighted-40-d25-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.36 | 11.11 | 12.33 | 1.218 | — |
| single-weighted-40-d40-s11-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s11-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s11-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s29-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s29-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s29-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s47-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s47-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s47-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s71-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s71-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s101-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s101-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s101-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s137-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s137-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-40-d40-s137-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d10-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 45.92 | 32.76 | 50.01 | 17.25 | — |
| single-weighted-64-d10-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.588 | 2.218 | 2.696 | 0.4779 | — |
| single-weighted-64-d10-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 43.52 | 40.48 | 53.39 | 12.91 | — |
| single-weighted-64-d10-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 35.3 | 34.63 | 40.56 | 5.927 | — |
| single-weighted-64-d10-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.241 | 2.147 | 2.661 | 0.5146 | — |
| single-weighted-64-d10-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 43.27 | 42.07 | 43.76 | 1.683 | — |
| single-weighted-64-d10-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 42.57 | 39.39 | 45.95 | 6.563 | — |
| single-weighted-64-d10-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.841 | 2.391 | 2.893 | 0.5012 | — |
| single-weighted-64-d10-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 43.67 | 42.41 | 54.98 | 12.57 | — |
| single-weighted-64-d10-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 34.73 | 34.3 | 36.61 | 2.31 | — |
| single-weighted-64-d10-s71-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.028 | 1.897 | 2.088 | 0.1907 | — |
| single-weighted-64-d10-s71-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 51.3 | 47.35 | 51.61 | 4.255 | — |
| single-weighted-64-d10-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 37.31 | 33.63 | 39.22 | 5.586 | — |
| single-weighted-64-d10-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.766 | 2.696 | 3.428 | 0.7318 | — |
| single-weighted-64-d10-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 48.12 | 41.99 | 51.58 | 9.588 | — |
| single-weighted-64-d10-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 33.67 | 31.68 | 37 | 5.327 | — |
| single-weighted-64-d10-s137-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.868 | 1.693 | 2.033 | 0.3405 | — |
| single-weighted-64-d10-s137-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 40.37 | 39.98 | 41.55 | 1.573 | — |
| single-weighted-64-d25-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 27.35 | 26.16 | 28.65 | 2.49 | — |
| single-weighted-64-d25-s11-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.745 | 2.458 | 2.937 | 0.4798 | — |
| single-weighted-64-d25-s11-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 32.09 | 31.22 | 32.51 | 1.293 | — |
| single-weighted-64-d25-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 26.97 | 26 | 27.22 | 1.229 | — |
| single-weighted-64-d25-s29-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.581 | 2.17 | 2.992 | 0.8222 | — |
| single-weighted-64-d25-s29-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 31.57 | 31.56 | 31.63 | 0.0718 | — |
| single-weighted-64-d25-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 27.22 | 26.04 | 37.27 | 11.23 | — |
| single-weighted-64-d25-s47-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.936 | 2.905 | 4.015 | 1.11 | — |
| single-weighted-64-d25-s47-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 39.38 | 32.24 | 39.59 | 7.343 | — |
| single-weighted-64-d25-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 35.99 | 35.12 | 37.41 | 2.292 | — |
| single-weighted-64-d25-s71-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.908 | 2.395 | 3.566 | 1.171 | — |
| single-weighted-64-d25-s71-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 44.36 | 44.01 | 46.52 | 2.514 | — |
| single-weighted-64-d25-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 37.92 | 33.4 | 39.01 | 5.611 | — |
| single-weighted-64-d25-s101-p1 | Greedy | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.012 | 3.76 | 5.95 | 2.189 | — |
| single-weighted-64-d25-s101-p1 | A* | 5/5 | 5 | 0 | 0 | 0 | 0 | 45.17 | 44.86 | 47.04 | 2.183 | — |
| single-weighted-64-d25-s137-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d25-s137-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d25-s137-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s11-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s11-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s11-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s29-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s29-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s29-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s47-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s47-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s47-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s71-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s71-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s101-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s101-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s101-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s137-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s137-p1 | Greedy | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-64-d40-s137-p1 | A* | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d10-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.516 | 1.178 | 1.523 | 0.3451 | — |
| multi-weighted-8-d10-s11-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.078 | 1.799 | 2.493 | 0.6936 | — |
| multi-weighted-8-d10-s11-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.224 | 2.153 | 2.362 | 0.2081 | — |
| multi-weighted-8-d10-s11-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8423 | 0.8027 | 1.241 | 0.4383 | — |
| multi-weighted-8-d10-s11-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.486 | 5.933 | 6.704 | 0.7712 | — |
| multi-weighted-8-d10-s11-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.454 | 8.269 | 9.095 | 0.8264 | — |
| multi-weighted-8-d10-s11-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.49 | 10.35 | 11.6 | 1.249 | — |
| multi-weighted-8-d10-s11-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.577 | 1.495 | 1.718 | 0.2238 | — |
| multi-weighted-8-d10-s11-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 31.7 | 24.05 | 32.11 | 8.065 | — |
| multi-weighted-8-d10-s11-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 37.03 | 33.27 | 38.34 | 5.067 | — |
| multi-weighted-8-d10-s11-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 54.41 | 47.65 | 55.5 | 7.851 | — |
| multi-weighted-8-d10-s11-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.088 | 2.069 | 2.244 | 0.1744 | — |
| multi-weighted-8-d10-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.992 | 1.925 | 2.114 | 0.1888 | — |
| multi-weighted-8-d10-s29-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.589 | 2.194 | 2.826 | 0.6317 | — |
| multi-weighted-8-d10-s29-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.45 | 2.354 | 2.939 | 0.5847 | — |
| multi-weighted-8-d10-s29-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8879 | 0.8642 | 0.8887 | 0.0245 | — |
| multi-weighted-8-d10-s29-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.741 | 6.658 | 6.994 | 0.3362 | — |
| multi-weighted-8-d10-s29-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.269 | 8.098 | 8.838 | 0.7402 | — |
| multi-weighted-8-d10-s29-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.77 | 10.25 | 11.34 | 1.086 | — |
| multi-weighted-8-d10-s29-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.82 | 1.199 | 1.965 | 0.7663 | — |
| multi-weighted-8-d10-s29-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 23.04 | 22.43 | 31.39 | 8.96 | — |
| multi-weighted-8-d10-s29-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 33.5 | 31.9 | 34.06 | 2.16 | — |
| multi-weighted-8-d10-s29-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 45.81 | 45.8 | 46.62 | 0.8141 | — |
| multi-weighted-8-d10-s29-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.427 | 1.617 | 2.872 | 1.255 | — |
| multi-weighted-8-d10-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.796 | 1.682 | 1.993 | 0.3116 | — |
| multi-weighted-8-d10-s47-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.577 | 2.141 | 2.687 | 0.5458 | — |
| multi-weighted-8-d10-s47-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.46 | 2.287 | 2.735 | 0.4483 | — |
| multi-weighted-8-d10-s47-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.14 | 0.9345 | 1.36 | 0.4257 | — |
| multi-weighted-8-d10-s47-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 7.253 | 7.102 | 9.392 | 2.29 | — |
| multi-weighted-8-d10-s47-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.907 | 8.651 | 9.54 | 0.8883 | — |
| multi-weighted-8-d10-s47-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.61 | 10.92 | 11.65 | 0.725 | — |
| multi-weighted-8-d10-s47-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.376 | 1.321 | 1.687 | 0.366 | — |
| multi-weighted-8-d10-s47-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 30.55 | 30.07 | 31.55 | 1.483 | — |
| multi-weighted-8-d10-s47-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 39.32 | 38.41 | 41.17 | 2.758 | — |
| multi-weighted-8-d10-s47-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 66.69 | 58.32 | 68.93 | 10.62 | — |
| multi-weighted-8-d10-s47-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.563 | 1.474 | 1.943 | 0.4697 | — |
| multi-weighted-8-d10-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.588 | 1.521 | 1.764 | 0.2435 | — |
| multi-weighted-8-d10-s71-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.129 | 2.054 | 2.546 | 0.4917 | — |
| multi-weighted-8-d10-s71-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.704 | 2.51 | 2.76 | 0.2497 | — |
| multi-weighted-8-d10-s71-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7733 | 0.6697 | 1.085 | 0.415 | — |
| multi-weighted-8-d10-s71-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.948 | 6.484 | 6.967 | 0.4826 | — |
| multi-weighted-8-d10-s71-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 9.381 | 8.467 | 9.529 | 1.062 | — |
| multi-weighted-8-d10-s71-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.42 | 10.98 | 12.43 | 1.45 | — |
| multi-weighted-8-d10-s71-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.633 | 1.627 | 1.765 | 0.1381 | — |
| multi-weighted-8-d10-s71-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 29.95 | 27.74 | 32.46 | 4.721 | — |
| multi-weighted-8-d10-s71-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 34.7 | 34.19 | 35.06 | 0.8648 | — |
| multi-weighted-8-d10-s71-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 49.51 | 49.37 | 50.41 | 1.04 | — |
| multi-weighted-8-d10-s71-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.616 | 1.471 | 1.858 | 0.3872 | — |
| multi-weighted-8-d10-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.414 | 1.169 | 1.454 | 0.2856 | — |
| multi-weighted-8-d10-s101-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.893 | 1.857 | 2.359 | 0.5016 | — |
| multi-weighted-8-d10-s101-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.201 | 2.13 | 2.65 | 0.5199 | — |
| multi-weighted-8-d10-s101-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.005 | 0.9716 | 1.043 | 0.0714 | — |
| multi-weighted-8-d10-s101-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.224 | 4.842 | 5.753 | 0.911 | — |
| multi-weighted-8-d10-s101-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.188 | 7.916 | 8.259 | 0.3431 | — |
| multi-weighted-8-d10-s101-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.55 | 9.904 | 12.23 | 2.324 | — |
| multi-weighted-8-d10-s101-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.527 | 1.43 | 1.985 | 0.5546 | — |
| multi-weighted-8-d10-s101-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 22.91 | 20.86 | 23.03 | 2.169 | — |
| multi-weighted-8-d10-s101-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 29.78 | 29.53 | 30.7 | 1.168 | — |
| multi-weighted-8-d10-s101-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 46.69 | 42.88 | 52.5 | 9.622 | — |
| multi-weighted-8-d10-s101-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.914 | 1.702 | 2.48 | 0.7777 | — |
| multi-weighted-8-d10-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.595 | 1.503 | 1.606 | 0.104 | — |
| multi-weighted-8-d10-s137-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.991 | 1.879 | 2.289 | 0.4092 | — |
| multi-weighted-8-d10-s137-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.935 | 1.757 | 2.184 | 0.4269 | — |
| multi-weighted-8-d10-s137-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.908 | 0.8722 | 1.043 | 0.1706 | — |
| multi-weighted-8-d10-s137-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 7.374 | 6.391 | 8.09 | 1.699 | — |
| multi-weighted-8-d10-s137-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.684 | 8.486 | 9.42 | 0.9348 | — |
| multi-weighted-8-d10-s137-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.31 | 9.901 | 11.52 | 1.615 | — |
| multi-weighted-8-d10-s137-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.256 | 1.168 | 1.603 | 0.4356 | — |
| multi-weighted-8-d10-s137-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 24.24 | 24.04 | 25.54 | 1.502 | — |
| multi-weighted-8-d10-s137-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 29.34 | 28.64 | 31.03 | 2.386 | — |
| multi-weighted-8-d10-s137-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 43.55 | 37.96 | 48.68 | 10.73 | — |
| multi-weighted-8-d10-s137-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.71 | 1.47 | 1.804 | 0.3339 | — |
| multi-weighted-8-d30-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.313 | 1.206 | 1.339 | 0.1335 | — |
| multi-weighted-8-d30-s11-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.613 | 1.044 | 1.744 | 0.7006 | — |
| multi-weighted-8-d30-s11-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.163 | 0.972 | 1.383 | 0.4111 | — |
| multi-weighted-8-d30-s11-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.6698 | 0.6675 | 0.8189 | 0.1514 | — |
| multi-weighted-8-d30-s11-p3 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s11-p3 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s11-p3 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s11-p3 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s11-p5 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s11-p5 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s11-p5 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s11-p5 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.364 | 1.093 | 1.552 | 0.4589 | — |
| multi-weighted-8-d30-s29-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.894 | 1.844 | 1.942 | 0.0986 | — |
| multi-weighted-8-d30-s29-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.926 | 1.545 | 1.945 | 0.4002 | — |
| multi-weighted-8-d30-s29-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.8015 | 0.7774 | 2.041 | 1.264 | — |
| multi-weighted-8-d30-s29-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.219 | 3.211 | 4.104 | 0.8929 | — |
| multi-weighted-8-d30-s29-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.404 | 4.324 | 5.427 | 1.103 | — |
| multi-weighted-8-d30-s29-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.012 | 5.853 | 8.855 | 3.003 | — |
| multi-weighted-8-d30-s29-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.124 | 0.7976 | 1.471 | 0.6734 | — |
| multi-weighted-8-d30-s29-p5 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s29-p5 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s29-p5 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s29-p5 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.196 | 0.9978 | 1.378 | 0.3805 | — |
| multi-weighted-8-d30-s47-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.866 | 1.76 | 2.021 | 0.2606 | — |
| multi-weighted-8-d30-s47-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.048 | 1.675 | 2.36 | 0.6856 | — |
| multi-weighted-8-d30-s47-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.6522 | 0.6244 | 0.9512 | 0.3268 | — |
| multi-weighted-8-d30-s47-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.015 | 5.606 | 6.456 | 0.8492 | — |
| multi-weighted-8-d30-s47-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.782 | 6.627 | 9.639 | 3.011 | — |
| multi-weighted-8-d30-s47-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.07 | 8.48 | 12.23 | 3.75 | — |
| multi-weighted-8-d30-s47-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.7435 | 0.7224 | 0.9796 | 0.2572 | — |
| multi-weighted-8-d30-s47-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 20.26 | 18.81 | 20.86 | 2.047 | — |
| multi-weighted-8-d30-s47-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 23.7 | 23.18 | 23.88 | 0.7075 | — |
| multi-weighted-8-d30-s47-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 32.68 | 32.38 | 40.27 | 7.89 | — |
| multi-weighted-8-d30-s47-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.086 | 1.059 | 1.34 | 0.2808 | — |
| multi-weighted-8-d30-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s71-p1 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s71-p1 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s71-p1 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s71-p3 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s71-p3 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s71-p3 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s71-p3 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s71-p5 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s71-p5 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s71-p5 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s71-p5 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s101-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s101-p1 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s101-p1 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s101-p1 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s101-p3 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s101-p3 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s101-p3 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s101-p3 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s101-p5 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s101-p5 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s101-p5 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s101-p5 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-8-d30-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.531 | 1.401 | 1.655 | 0.2541 | — |
| multi-weighted-8-d30-s137-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.403 | 1.245 | 1.912 | 0.6662 | — |
| multi-weighted-8-d30-s137-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.124 | 1.605 | 2.212 | 0.6067 | — |
| multi-weighted-8-d30-s137-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.5898 | 0.5645 | 0.7171 | 0.1526 | — |
| multi-weighted-8-d30-s137-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.991 | 4.766 | 5.711 | 0.9449 | — |
| multi-weighted-8-d30-s137-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.906 | 6.474 | 9.606 | 3.132 | — |
| multi-weighted-8-d30-s137-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 9.338 | 8.906 | 9.772 | 0.8661 | — |
| multi-weighted-8-d30-s137-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.205 | 1.111 | 1.548 | 0.4373 | — |
| multi-weighted-8-d30-s137-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 23.22 | 17.87 | 25.1 | 7.231 | — |
| multi-weighted-8-d30-s137-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 29.3 | 21.42 | 30.4 | 8.983 | — |
| multi-weighted-8-d30-s137-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 37.5 | 32.84 | 42.94 | 10.1 | — |
| multi-weighted-8-d30-s137-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.483 | 1.13 | 1.68 | 0.55 | — |
| multi-weighted-12-d10-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.627 | 3.914 | 5.427 | 1.512 | — |
| multi-weighted-12-d10-s11-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.282 | 5.264 | 5.491 | 0.2268 | — |
| multi-weighted-12-d10-s11-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.18 | 5.518 | 6.718 | 1.201 | — |
| multi-weighted-12-d10-s11-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.554 | 2.47 | 2.71 | 0.2399 | — |
| multi-weighted-12-d10-s11-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 14.18 | 13.54 | 16.26 | 2.714 | — |
| multi-weighted-12-d10-s11-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 18.48 | 18.34 | 19.61 | 1.272 | — |
| multi-weighted-12-d10-s11-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 24.36 | 24.05 | 25.22 | 1.17 | — |
| multi-weighted-12-d10-s11-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.591 | 2.276 | 2.598 | 0.3213 | — |
| multi-weighted-12-d10-s11-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 66.3 | 55.96 | 73.59 | 17.63 | — |
| multi-weighted-12-d10-s11-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 76.21 | 75.28 | 79.76 | 4.477 | — |
| multi-weighted-12-d10-s11-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 114 | 112.1 | 117 | 4.937 | — |
| multi-weighted-12-d10-s11-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.054 | 2.974 | 3.193 | 0.2192 | — |
| multi-weighted-12-d10-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.02 | 3.914 | 5.599 | 1.685 | — |
| multi-weighted-12-d10-s29-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.112 | 5.437 | 8.01 | 2.573 | — |
| multi-weighted-12-d10-s29-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.897 | 6.397 | 8.612 | 2.215 | — |
| multi-weighted-12-d10-s29-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.246 | 2.1 | 3.383 | 1.282 | — |
| multi-weighted-12-d10-s29-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 14.67 | 14.07 | 16.24 | 2.17 | — |
| multi-weighted-12-d10-s29-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 21.25 | 20.98 | 21.52 | 0.5407 | — |
| multi-weighted-12-d10-s29-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 26.39 | 25.73 | 33.57 | 7.839 | — |
| multi-weighted-12-d10-s29-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.656 | 3.081 | 3.916 | 0.8354 | — |
| multi-weighted-12-d10-s29-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 60.14 | 58.08 | 60.29 | 2.22 | — |
| multi-weighted-12-d10-s29-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 85.35 | 78.76 | 85.93 | 7.166 | — |
| multi-weighted-12-d10-s29-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 123.2 | 122.5 | 130.4 | 7.89 | — |
| multi-weighted-12-d10-s29-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.25 | 4.07 | 4.587 | 0.5164 | — |
| multi-weighted-12-d10-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.186 | 3.914 | 4.364 | 0.4503 | — |
| multi-weighted-12-d10-s47-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.835 | 4.173 | 5.511 | 1.338 | — |
| multi-weighted-12-d10-s47-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.061 | 5.151 | 6.14 | 0.9892 | — |
| multi-weighted-12-d10-s47-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.171 | 1.909 | 2.341 | 0.4325 | — |
| multi-weighted-12-d10-s47-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 16.32 | 16.13 | 17.19 | 1.059 | — |
| multi-weighted-12-d10-s47-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 21.33 | 19.77 | 22.03 | 2.259 | — |
| multi-weighted-12-d10-s47-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 27.02 | 26.9 | 28.1 | 1.201 | — |
| multi-weighted-12-d10-s47-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.452 | 2.404 | 2.605 | 0.2008 | — |
| multi-weighted-12-d10-s47-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 66.47 | 64.32 | 67.96 | 3.641 | — |
| multi-weighted-12-d10-s47-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 90.43 | 90.09 | 92.72 | 2.626 | — |
| multi-weighted-12-d10-s47-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 126.3 | 120 | 127.4 | 7.356 | — |
| multi-weighted-12-d10-s47-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.947 | 2.629 | 3.326 | 0.697 | — |
| multi-weighted-12-d10-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.42 | 3.873 | 4.777 | 0.9042 | — |
| multi-weighted-12-d10-s71-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.672 | 4.62 | 5.556 | 0.9361 | — |
| multi-weighted-12-d10-s71-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.809 | 5.791 | 6.141 | 0.3499 | — |
| multi-weighted-12-d10-s71-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.23 | 2.111 | 2.234 | 0.1229 | — |
| multi-weighted-12-d10-s71-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 14.95 | 13.81 | 15.18 | 1.366 | — |
| multi-weighted-12-d10-s71-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 20.98 | 20.9 | 22 | 1.102 | — |
| multi-weighted-12-d10-s71-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 27.47 | 27.17 | 28.26 | 1.086 | — |
| multi-weighted-12-d10-s71-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.96 | 2.335 | 3.578 | 1.243 | — |
| multi-weighted-12-d10-s71-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 60.69 | 60.12 | 63.94 | 3.812 | — |
| multi-weighted-12-d10-s71-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 80.49 | 78.53 | 87.69 | 9.154 | — |
| multi-weighted-12-d10-s71-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 118.8 | 116 | 133.2 | 17.18 | — |
| multi-weighted-12-d10-s71-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.596 | 2.373 | 2.962 | 0.5888 | — |
| multi-weighted-12-d10-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.779 | 2.243 | 3.204 | 0.9618 | — |
| multi-weighted-12-d10-s101-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.633 | 1.915 | 2.639 | 0.7233 | — |
| multi-weighted-12-d10-s101-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.043 | 2.399 | 3.078 | 0.6797 | — |
| multi-weighted-12-d10-s101-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.117 | 0.9793 | 1.536 | 0.557 | — |
| multi-weighted-12-d10-s101-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 14.16 | 13.39 | 14.34 | 0.9431 | — |
| multi-weighted-12-d10-s101-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 18.98 | 18.41 | 20.2 | 1.79 | — |
| multi-weighted-12-d10-s101-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 27.19 | 22 | 32.5 | 10.5 | — |
| multi-weighted-12-d10-s101-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.07 | 3.029 | 3.601 | 0.5718 | — |
| multi-weighted-12-d10-s101-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 65.37 | 58.82 | 65.85 | 7.025 | — |
| multi-weighted-12-d10-s101-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 78.43 | 75.45 | 80.06 | 4.606 | — |
| multi-weighted-12-d10-s101-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 109.3 | 107.3 | 120.9 | 13.68 | — |
| multi-weighted-12-d10-s101-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.28 | 2.481 | 3.969 | 1.487 | — |
| multi-weighted-12-d10-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.129 | 3.726 | 4.751 | 1.025 | — |
| multi-weighted-12-d10-s137-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.112 | 3.485 | 4.186 | 0.7011 | — |
| multi-weighted-12-d10-s137-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.372 | 5.128 | 6.619 | 1.491 | — |
| multi-weighted-12-d10-s137-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.804 | 1.799 | 2.105 | 0.3061 | — |
| multi-weighted-12-d10-s137-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 18.49 | 15.91 | 20.51 | 4.601 | — |
| multi-weighted-12-d10-s137-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 24.87 | 22.84 | 25.38 | 2.54 | — |
| multi-weighted-12-d10-s137-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 28.2 | 27.42 | 31.06 | 3.643 | — |
| multi-weighted-12-d10-s137-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.03 | 2.726 | 3.565 | 0.8389 | — |
| multi-weighted-12-d10-s137-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 63.58 | 59.21 | 70.49 | 11.29 | — |
| multi-weighted-12-d10-s137-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 83.78 | 67.08 | 86.82 | 19.74 | — |
| multi-weighted-12-d10-s137-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 97.41 | 97.18 | 130.3 | 33.14 | — |
| multi-weighted-12-d10-s137-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.896 | 2.821 | 3.301 | 0.4795 | — |
| multi-weighted-12-d30-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.855 | 1.744 | 1.963 | 0.2192 | — |
| multi-weighted-12-d30-s11-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.263 | 2.217 | 2.447 | 0.2298 | — |
| multi-weighted-12-d30-s11-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.954 | 2.82 | 3.917 | 1.097 | — |
| multi-weighted-12-d30-s11-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.497 | 1.473 | 1.527 | 0.0533 | — |
| multi-weighted-12-d30-s11-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 7.705 | 7.338 | 8.431 | 1.093 | — |
| multi-weighted-12-d30-s11-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.99 | 10.6 | 12.34 | 1.747 | — |
| multi-weighted-12-d30-s11-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 17.08 | 12.56 | 17.55 | 4.99 | — |
| multi-weighted-12-d30-s11-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.122 | 1.609 | 2.685 | 1.076 | — |
| multi-weighted-12-d30-s11-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 30.21 | 28.16 | 33.34 | 5.176 | — |
| multi-weighted-12-d30-s11-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 36.26 | 36.15 | 37.81 | 1.653 | — |
| multi-weighted-12-d30-s11-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 55.04 | 54.28 | 56.68 | 2.393 | — |
| multi-weighted-12-d30-s11-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.827 | 1.504 | 1.883 | 0.3784 | — |
| multi-weighted-12-d30-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.416 | 2.386 | 2.759 | 0.3732 | — |
| multi-weighted-12-d30-s29-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.42 | 2.976 | 4.22 | 1.244 | — |
| multi-weighted-12-d30-s29-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.312 | 3.12 | 3.355 | 0.2354 | — |
| multi-weighted-12-d30-s29-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.328 | 1.288 | 2.252 | 0.9644 | — |
| multi-weighted-12-d30-s29-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 9.358 | 8.389 | 10.12 | 1.726 | — |
| multi-weighted-12-d30-s29-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 12.63 | 12.13 | 13.36 | 1.225 | — |
| multi-weighted-12-d30-s29-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 14.74 | 14.18 | 20.67 | 6.488 | — |
| multi-weighted-12-d30-s29-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.405 | 1.568 | 2.539 | 0.9707 | — |
| multi-weighted-12-d30-s29-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 31.82 | 31.02 | 32.39 | 1.378 | — |
| multi-weighted-12-d30-s29-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 45.3 | 42.03 | 46.71 | 4.682 | — |
| multi-weighted-12-d30-s29-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 68.47 | 66 | 69.27 | 3.269 | — |
| multi-weighted-12-d30-s29-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.275 | 2.05 | 2.632 | 0.582 | — |
| multi-weighted-12-d30-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.476 | 2.447 | 3.128 | 0.6809 | — |
| multi-weighted-12-d30-s47-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.074 | 2.849 | 3.514 | 0.6653 | — |
| multi-weighted-12-d30-s47-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.794 | 3.103 | 3.968 | 0.8648 | — |
| multi-weighted-12-d30-s47-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.189 | 1.07 | 1.43 | 0.3606 | — |
| multi-weighted-12-d30-s47-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.342 | 7.992 | 8.749 | 0.757 | — |
| multi-weighted-12-d30-s47-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.09 | 10.79 | 11.5 | 0.7179 | — |
| multi-weighted-12-d30-s47-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 14.94 | 14.46 | 16.09 | 1.631 | — |
| multi-weighted-12-d30-s47-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.513 | 1.479 | 1.525 | 0.0456 | — |
| multi-weighted-12-d30-s47-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 35.25 | 34.52 | 40.55 | 6.034 | — |
| multi-weighted-12-d30-s47-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 47.49 | 46.39 | 52.71 | 6.316 | — |
| multi-weighted-12-d30-s47-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 71.79 | 69.83 | 72.56 | 2.724 | — |
| multi-weighted-12-d30-s47-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.929 | 1.785 | 1.941 | 0.156 | — |
| multi-weighted-12-d30-s71-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s71-p1 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s71-p1 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s71-p1 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s71-p3 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s71-p3 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s71-p3 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s71-p3 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s71-p5 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s71-p5 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s71-p5 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s71-p5 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s101-p1 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s101-p1 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s101-p1 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s101-p1 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s101-p3 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s101-p3 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s101-p3 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s101-p3 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s101-p5 | UCS | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s101-p5 | A* max | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s101-p5 | A* MST | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s101-p5 | Nearest-neighbor | 5/5 | 0 | 5 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-12-d30-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.877 | 1.814 | 1.885 | 0.07 | — |
| multi-weighted-12-d30-s137-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.139 | 2.098 | 2.242 | 0.144 | — |
| multi-weighted-12-d30-s137-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.317 | 2.174 | 3.109 | 0.9351 | — |
| multi-weighted-12-d30-s137-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.777 | 0.7663 | 0.7809 | 0.0146 | — |
| multi-weighted-12-d30-s137-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 16.94 | 15.65 | 20.37 | 4.727 | — |
| multi-weighted-12-d30-s137-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 24.31 | 21.06 | 24.5 | 3.434 | — |
| multi-weighted-12-d30-s137-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 26.21 | 25.82 | 31.3 | 5.478 | — |
| multi-weighted-12-d30-s137-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.555 | 2.355 | 2.702 | 0.3465 | — |
| multi-weighted-12-d30-s137-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 70.08 | 66.75 | 71.27 | 4.514 | — |
| multi-weighted-12-d30-s137-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 91.24 | 80.38 | 100.8 | 20.37 | — |
| multi-weighted-12-d30-s137-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 151.5 | 117.7 | 153.8 | 36.08 | — |
| multi-weighted-12-d30-s137-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.719 | 4.135 | 4.985 | 0.8503 | — |
| multi-weighted-16-d10-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.718 | 6.456 | 7.605 | 1.149 | — |
| multi-weighted-16-d10-s11-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 7.409 | 7.114 | 7.47 | 0.3562 | — |
| multi-weighted-16-d10-s11-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 7.149 | 6.732 | 7.205 | 0.4726 | — |
| multi-weighted-16-d10-s11-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.712 | 2.454 | 3.099 | 0.6454 | — |
| multi-weighted-16-d10-s11-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 38.91 | 36.58 | 41.57 | 4.989 | — |
| multi-weighted-16-d10-s11-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 48.39 | 42.85 | 48.64 | 5.785 | — |
| multi-weighted-16-d10-s11-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 66.44 | 58.1 | 70.84 | 12.75 | — |
| multi-weighted-16-d10-s11-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.597 | 5.336 | 7.956 | 2.621 | — |
| multi-weighted-16-d10-s11-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 116.4 | 110.8 | 123.2 | 12.31 | — |
| multi-weighted-16-d10-s11-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 155.3 | 153 | 170.1 | 17.08 | — |
| multi-weighted-16-d10-s11-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 234.5 | 224.2 | 244.1 | 19.91 | — |
| multi-weighted-16-d10-s11-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.267 | 4.215 | 4.99 | 0.7746 | — |
| multi-weighted-16-d10-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.324 | 5.423 | 6.728 | 1.305 | — |
| multi-weighted-16-d10-s29-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.477 | 7.843 | 8.638 | 0.7951 | — |
| multi-weighted-16-d10-s29-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 10.28 | 10.09 | 10.46 | 0.3739 | — |
| multi-weighted-16-d10-s29-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.059 | 3.806 | 4.199 | 0.3939 | — |
| multi-weighted-16-d10-s29-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 30.46 | 26.07 | 36.26 | 10.19 | — |
| multi-weighted-16-d10-s29-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 37.12 | 36.74 | 44.11 | 7.37 | — |
| multi-weighted-16-d10-s29-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 46.67 | 46.49 | 61.86 | 15.37 | — |
| multi-weighted-16-d10-s29-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.515 | 4.383 | 4.766 | 0.3834 | — |
| multi-weighted-16-d10-s29-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 111.8 | 109.1 | 113 | 3.857 | — |
| multi-weighted-16-d10-s29-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 148.7 | 146.5 | 149.1 | 2.625 | — |
| multi-weighted-16-d10-s29-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 219.2 | 218.9 | 227.6 | 8.719 | — |
| multi-weighted-16-d10-s29-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.579 | 4.147 | 6.558 | 2.411 | — |
| multi-weighted-16-d10-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 7.446 | 6.838 | 7.485 | 0.6463 | — |
| multi-weighted-16-d10-s47-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 8.452 | 8.151 | 8.791 | 0.6398 | — |
| multi-weighted-16-d10-s47-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 9.903 | 8.764 | 10.17 | 1.405 | — |
| multi-weighted-16-d10-s47-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.107 | 3.067 | 3.654 | 0.5874 | — |
| multi-weighted-16-d10-s47-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 36.57 | 31.85 | 38.23 | 6.376 | — |
| multi-weighted-16-d10-s47-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 42.65 | 39.99 | 49.21 | 9.221 | — |
| multi-weighted-16-d10-s47-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 60.79 | 50.11 | 63.88 | 13.77 | — |
| multi-weighted-16-d10-s47-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.582 | 3.519 | 4.85 | 1.331 | — |
| multi-weighted-16-d10-s47-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 125.9 | 125.7 | 132.5 | 6.806 | — |
| multi-weighted-16-d10-s47-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 168.8 | 167.6 | 172.1 | 4.554 | — |
| multi-weighted-16-d10-s47-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 231.8 | 230.1 | 237.6 | 7.5 | — |
| multi-weighted-16-d10-s47-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.043 | 4.336 | 5.312 | 0.9756 | — |
| multi-weighted-16-d10-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.091 | 3.641 | 5.443 | 1.802 | — |
| multi-weighted-16-d10-s71-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.96 | 3.878 | 4.698 | 0.8199 | — |
| multi-weighted-16-d10-s71-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.474 | 4.215 | 4.658 | 0.4433 | — |
| multi-weighted-16-d10-s71-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.645 | 1.548 | 2.214 | 0.6664 | — |
| multi-weighted-16-d10-s71-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 25.93 | 25.66 | 26.83 | 1.166 | — |
| multi-weighted-16-d10-s71-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 35.89 | 35.09 | 36.59 | 1.495 | — |
| multi-weighted-16-d10-s71-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 48.3 | 47.52 | 60.99 | 13.47 | — |
| multi-weighted-16-d10-s71-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.892 | 4.335 | 5.333 | 0.9984 | — |
| multi-weighted-16-d10-s71-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 110.6 | 109.9 | 114.5 | 4.52 | — |
| multi-weighted-16-d10-s71-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 157.4 | 152.6 | 179.9 | 27.27 | — |
| multi-weighted-16-d10-s71-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 217.7 | 212.3 | 217.8 | 5.521 | — |
| multi-weighted-16-d10-s71-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.424 | 4.182 | 4.867 | 0.685 | — |
| multi-weighted-16-d10-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.655 | 5.517 | 6.067 | 0.5506 | — |
| multi-weighted-16-d10-s101-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.348 | 5.262 | 6.584 | 1.322 | — |
| multi-weighted-16-d10-s101-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 9.225 | 6.373 | 9.629 | 3.256 | — |
| multi-weighted-16-d10-s101-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.752 | 2.514 | 3.42 | 0.9058 | — |
| multi-weighted-16-d10-s101-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 23.78 | 23.48 | 24.26 | 0.7782 | — |
| multi-weighted-16-d10-s101-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 35.52 | 32.49 | 38.28 | 5.786 | — |
| multi-weighted-16-d10-s101-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 37.17 | 37.01 | 41.65 | 4.637 | — |
| multi-weighted-16-d10-s101-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.922 | 3.704 | 4.048 | 0.3446 | — |
| multi-weighted-16-d10-s101-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 99.3 | 96.8 | 101.8 | 4.995 | — |
| multi-weighted-16-d10-s101-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 119.9 | 116.4 | 123.3 | 6.962 | — |
| multi-weighted-16-d10-s101-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 142.6 | 138.8 | 142.8 | 4.025 | — |
| multi-weighted-16-d10-s101-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.539 | 3.398 | 4.023 | 0.625 | — |
| multi-weighted-16-d10-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.48 | 1.36 | 1.597 | 0.2366 | — |
| multi-weighted-16-d10-s137-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.628 | 1.073 | 1.663 | 0.5909 | — |
| multi-weighted-16-d10-s137-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.412 | 1.016 | 1.453 | 0.4374 | — |
| multi-weighted-16-d10-s137-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.4906 | 0.4239 | 0.4996 | 0.0757 | — |
| multi-weighted-16-d10-s137-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 29.09 | 29.04 | 29.7 | 0.6559 | — |
| multi-weighted-16-d10-s137-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 34.28 | 33.78 | 35.59 | 1.816 | — |
| multi-weighted-16-d10-s137-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 44.17 | 43.32 | 49.6 | 6.28 | — |
| multi-weighted-16-d10-s137-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.075 | 3.978 | 4.126 | 0.1484 | — |
| multi-weighted-16-d10-s137-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 118.9 | 118.1 | 121.7 | 3.633 | — |
| multi-weighted-16-d10-s137-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 154.7 | 154.5 | 156.6 | 2.047 | — |
| multi-weighted-16-d10-s137-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 234.2 | 226.7 | 236.3 | 9.614 | — |
| multi-weighted-16-d10-s137-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.305 | 6.295 | 6.445 | 0.1494 | — |
| multi-weighted-16-d30-s11-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.397 | 4.32 | 5.893 | 1.574 | — |
| multi-weighted-16-d30-s11-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.659 | 4.609 | 4.856 | 0.247 | — |
| multi-weighted-16-d30-s11-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.96 | 4.713 | 5.309 | 0.5954 | — |
| multi-weighted-16-d30-s11-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.36 | 1.813 | 2.495 | 0.6822 | — |
| multi-weighted-16-d30-s11-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 20.23 | 18.6 | 20.48 | 1.88 | — |
| multi-weighted-16-d30-s11-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 24.81 | 24.44 | 25.07 | 0.625 | — |
| multi-weighted-16-d30-s11-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 43.7 | 33.14 | 45.03 | 11.89 | — |
| multi-weighted-16-d30-s11-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.203 | 3.39 | 4.357 | 0.9666 | — |
| multi-weighted-16-d30-s11-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 77.7 | 76.98 | 83.68 | 6.694 | — |
| multi-weighted-16-d30-s11-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 106.5 | 104.3 | 109.3 | 4.978 | — |
| multi-weighted-16-d30-s11-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 160.7 | 160 | 164 | 4.062 | — |
| multi-weighted-16-d30-s11-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.337 | 3.329 | 4.407 | 1.078 | — |
| multi-weighted-16-d30-s29-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.653 | 3.737 | 4.791 | 1.054 | — |
| multi-weighted-16-d30-s29-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.387 | 5.055 | 5.578 | 0.5237 | — |
| multi-weighted-16-d30-s29-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 6.195 | 5.87 | 6.984 | 1.114 | — |
| multi-weighted-16-d30-s29-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.12 | 1.763 | 2.14 | 0.3772 | — |
| multi-weighted-16-d30-s29-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 15.63 | 14.85 | 19.19 | 4.341 | — |
| multi-weighted-16-d30-s29-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 21.61 | 20.07 | 27 | 6.933 | — |
| multi-weighted-16-d30-s29-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 26.04 | 25.63 | 27.02 | 1.39 | — |
| multi-weighted-16-d30-s29-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.662 | 2.495 | 2.765 | 0.2698 | — |
| multi-weighted-16-d30-s29-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 68.13 | 68.04 | 77.98 | 9.94 | — |
| multi-weighted-16-d30-s29-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 94.45 | 89.85 | 109.3 | 19.43 | — |
| multi-weighted-16-d30-s29-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 127.7 | 123.7 | 142.4 | 18.64 | — |
| multi-weighted-16-d30-s29-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.49 | 4.153 | 4.798 | 0.6449 | — |
| multi-weighted-16-d30-s47-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.555 | 5.253 | 6.387 | 1.134 | — |
| multi-weighted-16-d30-s47-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 7.416 | 6.211 | 8.133 | 1.923 | — |
| multi-weighted-16-d30-s47-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 7.749 | 7.639 | 8.194 | 0.5553 | — |
| multi-weighted-16-d30-s47-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.403 | 2.778 | 3.843 | 1.065 | — |
| multi-weighted-16-d30-s47-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 21.35 | 20.74 | 22.29 | 1.551 | — |
| multi-weighted-16-d30-s47-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 27.69 | 27.52 | 28.67 | 1.152 | — |
| multi-weighted-16-d30-s47-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 35.76 | 35.59 | 39.78 | 4.193 | — |
| multi-weighted-16-d30-s47-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.972 | 3.802 | 4.107 | 0.3054 | — |
| multi-weighted-16-d30-s47-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 87.74 | 86.41 | 92.58 | 6.174 | — |
| multi-weighted-16-d30-s47-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 127.2 | 121.9 | 130.3 | 8.409 | — |
| multi-weighted-16-d30-s47-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 170.4 | 170.1 | 174 | 3.83 | — |
| multi-weighted-16-d30-s47-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.29 | 3.574 | 4.573 | 0.9985 | — |
| multi-weighted-16-d30-s71-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.599 | 2.331 | 2.736 | 0.4049 | — |
| multi-weighted-16-d30-s71-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.247 | 2.595 | 3.337 | 0.7422 | — |
| multi-weighted-16-d30-s71-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.256 | 2.836 | 3.754 | 0.9176 | — |
| multi-weighted-16-d30-s71-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.949 | 0.842 | 1.304 | 0.4625 | — |
| multi-weighted-16-d30-s71-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 20.48 | 18.33 | 23.37 | 5.043 | — |
| multi-weighted-16-d30-s71-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 28.05 | 26.73 | 31.56 | 4.831 | — |
| multi-weighted-16-d30-s71-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 34.62 | 32.89 | 35.24 | 2.35 | — |
| multi-weighted-16-d30-s71-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 4.166 | 3.566 | 4.551 | 0.9849 | — |
| multi-weighted-16-d30-s71-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 77.35 | 74.1 | 81.67 | 7.573 | — |
| multi-weighted-16-d30-s71-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 107.7 | 105.9 | 108.8 | 2.866 | — |
| multi-weighted-16-d30-s71-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 165.4 | 161.8 | 165.6 | 3.865 | — |
| multi-weighted-16-d30-s71-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.664 | 3.512 | 3.848 | 0.3362 | — |
| multi-weighted-16-d30-s101-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.007 | 4.339 | 5.029 | 0.6895 | — |
| multi-weighted-16-d30-s101-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.513 | 5.5 | 6.061 | 0.5613 | — |
| multi-weighted-16-d30-s101-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.958 | 5.947 | 6.142 | 0.195 | — |
| multi-weighted-16-d30-s101-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 1.812 | 1.668 | 2.194 | 0.526 | — |
| multi-weighted-16-d30-s101-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 9.014 | 8.634 | 9.704 | 1.07 | — |
| multi-weighted-16-d30-s101-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 11.77 | 11.76 | 12.48 | 0.7219 | — |
| multi-weighted-16-d30-s101-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 14.17 | 13.8 | 15.2 | 1.402 | — |
| multi-weighted-16-d30-s101-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 2.56 | 2.386 | 3.106 | 0.7203 | — |
| multi-weighted-16-d30-s101-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 35.43 | 33.9 | 40.45 | 6.547 | — |
| multi-weighted-16-d30-s101-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 46.54 | 45.71 | 47.52 | 1.814 | — |
| multi-weighted-16-d30-s101-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 60.82 | 60.26 | 61.11 | 0.8493 | — |
| multi-weighted-16-d30-s101-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.129 | 3.016 | 3.999 | 0.9824 | — |
| multi-weighted-16-d30-s137-p1 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.4422 | 0.4149 | 0.4714 | 0.0565 | — |
| multi-weighted-16-d30-s137-p1 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.754 | 0.5094 | 0.7632 | 0.2538 | — |
| multi-weighted-16-d30-s137-p1 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.735 | 0.6379 | 0.7492 | 0.1113 | — |
| multi-weighted-16-d30-s137-p1 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 0.356 | 0.3156 | 0.4706 | 0.155 | — |
| multi-weighted-16-d30-s137-p3 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 19.62 | 18.79 | 20.54 | 1.749 | — |
| multi-weighted-16-d30-s137-p3 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 25.05 | 25.03 | 26.46 | 1.425 | — |
| multi-weighted-16-d30-s137-p3 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 35.25 | 33.99 | 38.99 | 5 | — |
| multi-weighted-16-d30-s137-p3 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 3.15 | 2.889 | 3.193 | 0.3031 | — |
| multi-weighted-16-d30-s137-p5 | UCS | 5/5 | 5 | 0 | 0 | 0 | 0 | 79.91 | 79.4 | 79.99 | 0.5872 | — |
| multi-weighted-16-d30-s137-p5 | A* max | 5/5 | 5 | 0 | 0 | 0 | 0 | 112.7 | 112.7 | 113.6 | 0.9275 | — |
| multi-weighted-16-d30-s137-p5 | A* MST | 5/5 | 5 | 0 | 0 | 0 | 0 | 169.5 | 165.2 | 171.1 | 5.878 | — |
| multi-weighted-16-d30-s137-p5 | Nearest-neighbor | 5/5 | 5 | 0 | 0 | 0 | 0 | 5.12 | 4.976 | 5.819 | 0.8432 | — |
