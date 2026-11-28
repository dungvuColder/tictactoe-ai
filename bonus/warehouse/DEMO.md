# Demo Bài 2 · Robot kho

Chạy lệnh từ gốc repo. Có thể trình bày bằng CLI hoặc mở GUI bằng `python -m bonus.warehouse.gui` rồi chọn cấu hình bên dưới. Sau mỗi lần đổi cấu hình trong GUI, nhấn **Run**. Khi cần quan sát đường đi chậm hơn, hạ tốc độ hoặc dùng **Pause/Resume** sau khi có kết quả.

Các số liệu dưới đây lấy từ lần kiểm tra CLI ở lượt nghiệm thu. Thời gian từng lượt có thể thay đổi theo máy và tải hệ thống.

## 1. UCS và A* trên cùng bản đồ

**Cấu hình.** [`detour.json`](maps/detour.json), một đích `A`. Trong GUI chọn **Lối đi vòng**, **Một đích** và điểm **A**.

1. Chạy **UCS**, xem tuyến vòng qua cạnh dưới của dãy kệ và ghi chi phí, số bước, số nút mở rộng.
2. Giữ nguyên bản đồ và điểm lấy, chuyển sang `A*` rồi chạy lại. Đối chiếu các chỉ số trong panel hoặc đầu ra JSON.

```powershell
python -m bonus.warehouse.cli --map bonus/warehouse/maps/detour.json --mode single --pickup A --algorithm ucs --json
python -m bonus.warehouse.cli --map bonus/warehouse/maps/detour.json --mode single --pickup A --algorithm astar --json
```

| Thuật toán | Chi phí | Bước | Nút mở rộng |
|---|---:|---:|---:|
| UCS | 6 | 6 | 7 |
| A* | 6 | 6 | 6 |

**Điều cần giải thích.** UCS ưu tiên chi phí đã đi. A* dùng thêm cận dưới Manhattan, vẫn tìm được cùng chi phí ở mẫu này và mở rộng ít hơn một nút. Kệ làm cho đường đi thực tế dài hơn khoảng cách Manhattan.

## 2. Đường ít bước và đường ít chi phí

**Cấu hình.** [`weighted.json`](maps/weighted.json), một đích `A`. Trong GUI chọn **Chi phí khác nhau** và **Một đích**.

1. Chạy **BFS** để xem đường thẳng qua hàng trên.
2. Chuyển sang **UCS** và xem tuyến vòng qua hàng dưới. Đối chiếu chi phí các ô được đi vào và số bước.

```powershell
python -m bonus.warehouse.cli --map bonus/warehouse/maps/weighted.json --mode single --pickup A --algorithm bfs --json
python -m bonus.warehouse.cli --map bonus/warehouse/maps/weighted.json --mode single --pickup A --algorithm ucs --json
```

| Thuật toán | Chi phí | Bước |
|---|---:|---:|
| BFS | 19 | 3 |
| UCS | 5 | 5 |

**Điều cần giải thích.** BFS chọn ít bước nhất nhưng vào hai ô chi phí 9. UCS đi nhiều bước hơn trên các ô chi phí 1. Chi phí của ô xuất phát chỉ được tính nếu robot quay lại ô đó.

## 3. Nhiều điểm lấy hàng với A* và nearest-neighbor

**Cấu hình.** [`nearest_neighbor_trap.json`](maps/nearest_neighbor_trap.json), chế độ nhiều điểm. Trong GUI chọn **So sánh nearest-neighbor** và **Nhiều điểm**. Depot là `[0, 2]`.

1. Chạy `A*` với heuristic **MST**. Quan sát thứ tự hàng được đánh dấu và thời điểm robot về depot.
2. Chuyển sang **Nearest-neighbor** rồi chạy lại. Đối chiếu thứ tự lấy, chi phí và số bước.

```powershell
python -m bonus.warehouse.cli --map bonus/warehouse/maps/nearest_neighbor_trap.json --mode multi --algorithm astar --heuristic mst --json
python -m bonus.warehouse.cli --map bonus/warehouse/maps/nearest_neighbor_trap.json --mode multi --algorithm nearest_neighbor --json
```

| Thuật toán | Thứ tự lấy | Chi phí | Bước |
|---|---|---:|---:|
| A* MST | C → B → A | 6 | 6 |
| Nearest-neighbor | C → A → B | 8 | 8 |

**Điều cần giải thích.** A* xét vị trí cùng bitmask và tối ưu cả tuyến. Nearest-neighbor dùng đường rẻ nhất cho từng chặng, nhưng chọn điểm kế tiếp theo chi phí cục bộ. Khi robot ghé depot trước lúc lấy đủ hàng, nhiệm vụ vẫn đang tiếp diễn.

## 4. Không có đường

**Cấu hình.** [`no_path.json`](maps/no_path.json), một đích `A`, thuật toán `A*`. Trong GUI chọn **Đích bị cô lập** và **Một đích**.

1. Chạy A* và quan sát những ô đã mở rộng ở phía robot. Dãy kệ chia lưới thành hai phía.
2. Đọc trạng thái **Không có đường đi** trong GUI hoặc `no_path` trong JSON. Kiểm tra đường đi rỗng và chi phí, số bước bỏ trống.

```powershell
python -m bonus.warehouse.cli --map bonus/warehouse/maps/no_path.json --mode single --pickup A --algorithm astar --json
```

**Kết quả đã đo.** `no_path`, hai nút mở rộng, mã thoát CLI 1.

**Điều cần giải thích.** Frontier đã cạn vì không thể vượt qua dãy kệ. `timeout` hoặc `node_limit` thể hiện tìm kiếm phải dừng do ngân sách và không đủ để kết luận vô nghiệm.
