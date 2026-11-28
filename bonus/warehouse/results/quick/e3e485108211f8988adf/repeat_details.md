# Độ dao động trong cùng nhiệm vụ

Thống kê thời gian chỉ dùng các lượt success của từng biến thể. Q1, Q3 và IQR được tính bằng nội suy phân vị khi có ít nhất ba lượt success. Schema cũ có một lượt nên độ phân tán không có.

| Nhiệm vụ | Thuật toán | Ghi/kỳ vọng | Success | No path | Timeout | Giới hạn nút | Hủy | Trung vị (ms) | Q1 (ms) | Q3 (ms) | IQR (ms) | Ghi chú |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| single-uniform-8-d10-s11-p1 | BFS | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.4842 | 0.4785 | 0.5392 | 0.0607 | — |
| single-uniform-8-d10-s11-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.4702 | 0.4353 | 0.5122 | 0.07695 | — |
| single-uniform-8-d10-s11-p1 | Greedy | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.255 | 0.2421 | 0.4614 | 0.2193 | — |
| single-uniform-8-d10-s11-p1 | A* | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.4834 | 0.4797 | 0.5524 | 0.07265 | — |
| single-uniform-8-d10-s29-p1 | BFS | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.4615 | 0.4484 | 0.5135 | 0.0651 | — |
| single-uniform-8-d10-s29-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.5318 | 0.4657 | 0.5711 | 0.1054 | — |
| single-uniform-8-d10-s29-p1 | Greedy | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.2164 | 0.2072 | 0.2217 | 0.0145 | — |
| single-uniform-8-d10-s29-p1 | A* | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.4868 | 0.4855 | 0.5231 | 0.0376 | — |
| single-uniform-8-d30-s11-p1 | BFS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-8-d30-s11-p1 | UCS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-8-d30-s11-p1 | Greedy | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-8-d30-s11-p1 | A* | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-8-d30-s29-p1 | BFS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-8-d30-s29-p1 | UCS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-8-d30-s29-p1 | Greedy | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-8-d30-s29-p1 | A* | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-14-d10-s11-p1 | BFS | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.08 | 1.016 | 1.332 | 0.3162 | — |
| single-uniform-14-d10-s11-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.07 | 1.062 | 1.154 | 0.09215 | — |
| single-uniform-14-d10-s11-p1 | Greedy | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.3148 | 0.3069 | 0.3374 | 0.03055 | — |
| single-uniform-14-d10-s11-p1 | A* | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.121 | 1.112 | 1.124 | 0.0122 | — |
| single-uniform-14-d10-s29-p1 | BFS | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.145 | 1.118 | 1.222 | 0.104 | — |
| single-uniform-14-d10-s29-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.264 | 1.204 | 1.294 | 0.08985 | — |
| single-uniform-14-d10-s29-p1 | Greedy | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.5026 | 0.4354 | 0.5227 | 0.08725 | — |
| single-uniform-14-d10-s29-p1 | A* | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.337 | 1.279 | 1.436 | 0.1577 | — |
| single-uniform-14-d30-s11-p1 | BFS | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.7011 | 0.6902 | 0.9253 | 0.2351 | — |
| single-uniform-14-d30-s11-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.7029 | 0.7011 | 0.8925 | 0.1914 | — |
| single-uniform-14-d30-s11-p1 | Greedy | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.413 | 0.3956 | 0.5277 | 0.1321 | — |
| single-uniform-14-d30-s11-p1 | A* | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.6589 | 0.5729 | 0.7772 | 0.2043 | — |
| single-uniform-14-d30-s29-p1 | BFS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-14-d30-s29-p1 | UCS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-14-d30-s29-p1 | Greedy | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-uniform-14-d30-s29-p1 | A* | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-8-d10-s11-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.4281 | 0.41 | 0.4722 | 0.06225 | — |
| single-weighted-8-d10-s11-p1 | Greedy | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.2313 | 0.2201 | 0.2402 | 0.02015 | — |
| single-weighted-8-d10-s11-p1 | A* | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.613 | 0.512 | 0.6171 | 0.1052 | — |
| single-weighted-8-d10-s29-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.4142 | 0.3841 | 0.5599 | 0.1759 | — |
| single-weighted-8-d10-s29-p1 | Greedy | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.303 | 0.2651 | 0.3126 | 0.04755 | — |
| single-weighted-8-d10-s29-p1 | A* | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.5549 | 0.5218 | 0.6177 | 0.09595 | — |
| single-weighted-8-d30-s11-p1 | UCS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-8-d30-s11-p1 | Greedy | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-8-d30-s11-p1 | A* | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-8-d30-s29-p1 | UCS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-8-d30-s29-p1 | Greedy | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-8-d30-s29-p1 | A* | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-14-d10-s11-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.141 | 1.102 | 1.179 | 0.07655 | — |
| single-weighted-14-d10-s11-p1 | Greedy | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.3378 | 0.3208 | 0.3728 | 0.0521 | — |
| single-weighted-14-d10-s11-p1 | A* | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.479 | 1.456 | 1.543 | 0.0872 | — |
| single-weighted-14-d10-s29-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.74 | 1.435 | 1.748 | 0.3136 | — |
| single-weighted-14-d10-s29-p1 | Greedy | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.4554 | 0.3951 | 0.4555 | 0.06035 | — |
| single-weighted-14-d10-s29-p1 | A* | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.565 | 1.479 | 1.683 | 0.2046 | — |
| single-weighted-14-d30-s11-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.9041 | 0.8298 | 1.044 | 0.2144 | — |
| single-weighted-14-d30-s11-p1 | Greedy | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.5958 | 0.5104 | 0.6187 | 0.1083 | — |
| single-weighted-14-d30-s11-p1 | A* | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.028 | 0.9481 | 1.217 | 0.2686 | — |
| single-weighted-14-d30-s29-p1 | UCS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-14-d30-s29-p1 | Greedy | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| single-weighted-14-d30-s29-p1 | A* | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-7-d10-s11-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.25 | 1.166 | 1.351 | 0.1851 | — |
| multi-weighted-7-d10-s11-p1 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.563 | 1.348 | 1.681 | 0.3333 | — |
| multi-weighted-7-d10-s11-p1 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 2.257 | 2.24 | 2.571 | 0.3307 | — |
| multi-weighted-7-d10-s11-p1 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.8566 | 0.7755 | 0.9272 | 0.1517 | — |
| multi-weighted-7-d10-s11-p3 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 3.682 | 3.45 | 4.741 | 1.291 | — |
| multi-weighted-7-d10-s11-p3 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 4.287 | 4.191 | 4.532 | 0.3411 | — |
| multi-weighted-7-d10-s11-p3 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 4.689 | 4.668 | 5.276 | 0.6082 | — |
| multi-weighted-7-d10-s11-p3 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.6537 | 0.643 | 0.7101 | 0.0671 | — |
| multi-weighted-7-d10-s11-p5 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 16.81 | 16.45 | 16.85 | 0.3959 | — |
| multi-weighted-7-d10-s11-p5 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 22.22 | 20.78 | 25.24 | 4.462 | — |
| multi-weighted-7-d10-s11-p5 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 30.67 | 30.06 | 32.88 | 2.829 | — |
| multi-weighted-7-d10-s11-p5 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.107 | 0.9809 | 1.166 | 0.1853 | — |
| multi-weighted-7-d10-s29-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.9057 | 0.8928 | 0.9417 | 0.0489 | — |
| multi-weighted-7-d10-s29-p1 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.529 | 1.331 | 1.619 | 0.2879 | — |
| multi-weighted-7-d10-s29-p1 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.863 | 1.562 | 1.954 | 0.392 | — |
| multi-weighted-7-d10-s29-p1 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.4695 | 0.4605 | 0.4807 | 0.0202 | — |
| multi-weighted-7-d10-s29-p3 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 3.697 | 3.495 | 4.165 | 0.6709 | — |
| multi-weighted-7-d10-s29-p3 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 5.079 | 4.874 | 5.16 | 0.286 | — |
| multi-weighted-7-d10-s29-p3 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 7.432 | 6.984 | 8.307 | 1.323 | — |
| multi-weighted-7-d10-s29-p3 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.085 | 0.9331 | 1.148 | 0.2149 | — |
| multi-weighted-7-d10-s29-p5 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 14.38 | 14.29 | 14.88 | 0.5948 | — |
| multi-weighted-7-d10-s29-p5 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 24.51 | 22.14 | 25.5 | 3.362 | — |
| multi-weighted-7-d10-s29-p5 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 31.04 | 28.46 | 35.1 | 6.646 | — |
| multi-weighted-7-d10-s29-p5 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.9981 | 0.9877 | 1.232 | 0.2443 | — |
| multi-weighted-7-d30-s11-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.9189 | 0.8015 | 0.9808 | 0.1793 | — |
| multi-weighted-7-d30-s11-p1 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.9456 | 0.9006 | 1.124 | 0.2239 | — |
| multi-weighted-7-d30-s11-p1 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.13 | 1.077 | 1.326 | 0.2489 | — |
| multi-weighted-7-d30-s11-p1 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.5431 | 0.5187 | 0.5442 | 0.0255 | — |
| multi-weighted-7-d30-s11-p3 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 2.335 | 2.282 | 2.437 | 0.1553 | — |
| multi-weighted-7-d30-s11-p3 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 3.467 | 3.247 | 3.655 | 0.4079 | — |
| multi-weighted-7-d30-s11-p3 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 3.422 | 3.402 | 3.908 | 0.5064 | — |
| multi-weighted-7-d30-s11-p3 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.5228 | 0.5173 | 0.5266 | 0.0093 | — |
| multi-weighted-7-d30-s11-p5 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 11.65 | 10.55 | 12.79 | 2.239 | — |
| multi-weighted-7-d30-s11-p5 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 13.28 | 12.91 | 17.04 | 4.137 | — |
| multi-weighted-7-d30-s11-p5 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 18.72 | 18.71 | 18.99 | 0.2807 | — |
| multi-weighted-7-d30-s11-p5 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.077 | 0.9725 | 1.174 | 0.2012 | — |
| multi-weighted-7-d30-s29-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.9091 | 0.8628 | 1.044 | 0.1807 | — |
| multi-weighted-7-d30-s29-p1 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.264 | 1.095 | 1.589 | 0.4933 | — |
| multi-weighted-7-d30-s29-p1 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.069 | 1.029 | 1.21 | 0.1816 | — |
| multi-weighted-7-d30-s29-p1 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.4059 | 0.3953 | 0.5194 | 0.1242 | — |
| multi-weighted-7-d30-s29-p3 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 2.83 | 2.806 | 2.949 | 0.1432 | — |
| multi-weighted-7-d30-s29-p3 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 4.363 | 4.063 | 4.593 | 0.5294 | — |
| multi-weighted-7-d30-s29-p3 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 6.781 | 6.48 | 7.652 | 1.172 | — |
| multi-weighted-7-d30-s29-p3 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.8152 | 0.7772 | 0.9674 | 0.1902 | — |
| multi-weighted-7-d30-s29-p5 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 14.78 | 13.19 | 16.39 | 3.198 | — |
| multi-weighted-7-d30-s29-p5 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 26.02 | 22.79 | 26.9 | 4.112 | — |
| multi-weighted-7-d30-s29-p5 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 24.48 | 24.29 | 30.07 | 5.782 | — |
| multi-weighted-7-d30-s29-p5 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.203 | 1.019 | 1.252 | 0.233 | — |
| multi-weighted-10-d10-s11-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 3.164 | 2.987 | 3.61 | 0.6227 | — |
| multi-weighted-10-d10-s11-p1 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 3.751 | 3.543 | 4.002 | 0.4584 | — |
| multi-weighted-10-d10-s11-p1 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 4.679 | 4.407 | 6.009 | 1.602 | — |
| multi-weighted-10-d10-s11-p1 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 2.056 | 1.94 | 2.243 | 0.3034 | — |
| multi-weighted-10-d10-s11-p3 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 11.53 | 10.74 | 12.87 | 2.13 | — |
| multi-weighted-10-d10-s11-p3 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 15.98 | 14.92 | 16.1 | 1.178 | — |
| multi-weighted-10-d10-s11-p3 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 24 | 21.95 | 25.01 | 3.052 | — |
| multi-weighted-10-d10-s11-p3 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 1.875 | 1.68 | 2.263 | 0.5836 | — |
| multi-weighted-10-d10-s11-p5 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 41.04 | 40.46 | 44.84 | 4.38 | — |
| multi-weighted-10-d10-s11-p5 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 54.47 | 53.83 | 60.5 | 6.674 | — |
| multi-weighted-10-d10-s11-p5 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 81.31 | 77.78 | 81.48 | 3.707 | — |
| multi-weighted-10-d10-s11-p5 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 2.033 | 1.905 | 2.152 | 0.2466 | — |
| multi-weighted-10-d10-s29-p1 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 2.904 | 2.563 | 2.931 | 0.3685 | — |
| multi-weighted-10-d10-s29-p1 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 2.345 | 2.005 | 2.801 | 0.7956 | — |
| multi-weighted-10-d10-s29-p1 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 3.074 | 2.824 | 3.091 | 0.2666 | — |
| multi-weighted-10-d10-s29-p1 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 0.9968 | 0.8765 | 1.087 | 0.2102 | — |
| multi-weighted-10-d10-s29-p3 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 13.08 | 12.31 | 14.08 | 1.769 | — |
| multi-weighted-10-d10-s29-p3 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 17.69 | 16.39 | 17.8 | 1.412 | — |
| multi-weighted-10-d10-s29-p3 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 23.54 | 22 | 24.48 | 2.486 | — |
| multi-weighted-10-d10-s29-p3 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 2.18 | 1.991 | 2.285 | 0.2937 | — |
| multi-weighted-10-d10-s29-p5 | UCS | 3/3 | 3 | 0 | 0 | 0 | 0 | 43.96 | 43.01 | 47.53 | 4.518 | — |
| multi-weighted-10-d10-s29-p5 | A* max | 3/3 | 3 | 0 | 0 | 0 | 0 | 56.73 | 56.28 | 62.42 | 6.138 | — |
| multi-weighted-10-d10-s29-p5 | A* MST | 3/3 | 3 | 0 | 0 | 0 | 0 | 93.55 | 84.22 | 95.26 | 11.04 | — |
| multi-weighted-10-d10-s29-p5 | Nearest-neighbor | 3/3 | 3 | 0 | 0 | 0 | 0 | 2.169 | 2.05 | 2.273 | 0.223 | — |
| multi-weighted-10-d30-s11-p1 | UCS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s11-p1 | A* max | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s11-p1 | A* MST | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s11-p1 | Nearest-neighbor | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s11-p3 | UCS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s11-p3 | A* max | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s11-p3 | A* MST | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s11-p3 | Nearest-neighbor | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s11-p5 | UCS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s11-p5 | A* max | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s11-p5 | A* MST | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s11-p5 | Nearest-neighbor | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s29-p1 | UCS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s29-p1 | A* max | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s29-p1 | A* MST | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s29-p1 | Nearest-neighbor | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s29-p3 | UCS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s29-p3 | A* max | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s29-p3 | A* MST | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s29-p3 | Nearest-neighbor | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s29-p5 | UCS | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s29-p5 | A* max | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s29-p5 | A* MST | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
| multi-weighted-10-d30-s29-p5 | Nearest-neighbor | 3/3 | 0 | 3 | 0 | 0 | 0 | không có | không có | không có | không có | — |
