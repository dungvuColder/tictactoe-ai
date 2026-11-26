# Bài 2 bonus · Lập kế hoạch lấy hàng cho robot kho

Module mô phỏng một robot đi bốn hướng trên lưới kho tĩnh. Robot tìm đường đến một điểm lấy hàng hoặc lấy đủ nhiều điểm rồi về depot. Mục tiêu là tối thiểu hóa tổng chi phí vào ô. Số bước được ghi riêng.

Bài áp dụng mô hình PEAS, tìm kiếm đồ thị BFS, UCS, Greedy Best-First và A*, cùng heuristic Manhattan và cây khung nhỏ nhất (MST). Trạng thái nhiều điểm dùng vị trí và bitmask hàng đã lấy. Baseline nearest-neighbor dùng UCS để chọn điểm gần nhất theo chi phí đường đi thật.

## Cài đặt

Dùng Python 3.10 trở lên. Chạy các lệnh trong tài liệu từ **gốc repo**. CLI và benchmark chỉ dùng thư viện chuẩn. GUI cần Pygame, còn plotting cần Matplotlib.

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -p 'test_warehouse*.py'
```

## Chạy CLI

```powershell
python -m bonus.warehouse.cli --map bonus/warehouse/maps/weighted.json --mode single --algorithm astar --pickup A --json
python -m bonus.warehouse.cli --map bonus/warehouse/maps/nearest_neighbor_trap.json --mode multi --algorithm astar --heuristic mst --json
python -m bonus.warehouse.cli --help
```

- `--map` nhận đường dẫn đến bản đồ JSON. Mặc định chạy `single` và `astar`. Một đích lấy hàng theo `--pickup ID` hoặc dùng điểm đầu tiên nếu bỏ tùy chọn này. Nhiều điểm lấy tất cả hàng trong bản đồ rồi quay về depot.
- `--heuristic max|mst` chọn heuristic cho A* nhiều điểm, mặc định `max`. `--timeout SECONDS` và `--max-expanded-nodes N` đặt giới hạn thời gian và số lần mở rộng. Ctrl+C trong lúc tìm kiếm yêu cầu hủy.
- `--json` xuất chi phí, số bước, đường đi, thứ tự lấy hàng và các bộ đếm. Mã thoát **0** ứng với `success`, **1** ứng với `no_path`, `timeout`, `node_limit` hoặc `cancelled`, và **2** ứng với lỗi đầu vào.

### Phạm vi và giới hạn thuật toán

| Thuật toán | Chế độ CLI/GUI | Đặc điểm và giới hạn |
|---|---|---|
| `bfs` | Một đích | Tìm ít bước nhất. Bảo đảm tối ưu chi phí khi mọi bước có cùng chi phí. |
| `ucs` | Cả hai | Tối ưu tổng chi phí bước dương nếu tìm được nghiệm trước khi chạm giới hạn. Có thể mở rộng nhiều trạng thái. |
| `greedy` | Một đích | Ưu tiên ước lượng Manhattan tới đích. Có thể trả tuyến đắt hơn UCS. |
| `astar` | Cả hai | Ưu tiên chi phí đã đi cộng cận dưới còn lại. Một đích dùng Manhattan nhân chi phí ô đi được nhỏ nhất. Nhiều điểm dùng cận xa nhất (`max`) hoặc MST (`mst`). Với các cận này và cơ chế mở lại trạng thái, nghiệm trả về có chi phí tối ưu. Tính heuristic tốn thời gian, kể cả khi giảm số nút. |
| `nearest_neighbor` | Nhiều điểm | Dùng UCS đi tới điểm chưa lấy rẻ nhất, lặp lại rồi về depot. Tối ưu từng chặng, và tổng tuyến có thể đắt hơn nghiệm tối ưu. |

Số trạng thái nhiều điểm tăng theo số bit hàng. Mô phỏng dùng một robot, bản đồ cố định và tải trọng không giới hạn. Các số đo trên bản đồ tổng hợp chưa được kiểm chứng trong kho thật.

## Chạy GUI

```powershell
python -m bonus.warehouse.gui
python -m bonus.warehouse.gui --map multi_pickup --mode multi --algorithm astar --heuristic mst
python -m bonus.warehouse.gui --help
```

GUI nhận tên bản đồ mẫu bỏ đuôi `.json`. Dùng mũi tên trong panel để chọn bản đồ, chế độ, thuật toán, điểm lấy hoặc heuristic. Chú giải trên bản đồ phân biệt kệ, chi phí ô, depot, hàng, ô đã mở rộng và tuyến.

| Nút hoặc phím | Thao tác |
|---|---|
| **Run** hoặc **Enter** | Tìm đường với cấu hình đang chọn. |
| **Pause/Resume** hoặc **Space** | Dừng hoặc tiếp tục hoạt họa sau khi có kết quả. Tác vụ tìm kiếm vẫn chạy tới khi có kết quả hoặc được hủy. |
| **Reset** hoặc **R** | Hủy lượt hiện tại và đưa robot về vị trí ban đầu. |
| **Tốc độ** | Dùng mũi tên để điều chỉnh tốc độ phát lại. |
| **Esc** hoặc đóng cửa sổ | Thoát GUI và yêu cầu hủy tác vụ đang chạy. |

GUI phát lại các ô đã mở rộng và đánh dấu hàng khi robot đi qua. Nếu chạm giới hạn sự kiện, panel ghi số lần mở rộng đã lưu trên tổng số lần mở rộng. Tuyến và thống kê vẫn được hiển thị đầy đủ. Thời gian phát lại nằm ngoài số đo tìm kiếm.

Smoke test bằng SDL dummy trên PowerShell.

```powershell
$env:SDL_VIDEODRIVER = 'dummy'
python -m bonus.warehouse.gui --map multi_pickup --mode multi --algorithm astar --heuristic mst --autostart --frames 30
Remove-Item Env:SDL_VIDEODRIVER
```

## Schema bản đồ JSON

```json
{
  "schema_version": 1,
  "grid": [[1, 0, 3], [1, 1, 2]],
  "start": [0, 0],
  "depot": [0, 0],
  "pickups": [{"id": "A", "position": [0, 2]}]
}
```

- Tệp UTF-8 có đúng các trường trên. `grid` phải là lưới chữ nhật khác rỗng. `0` là kệ. Số nguyên dương là chi phí **vào** ô đó.
- Tọa độ là `[hàng, cột]`, bắt đầu từ 0. `start`, `depot` và mọi điểm lấy hàng phải là ô đi được. Ô xuất phát và depot có thể trùng nhau hoặc trùng một điểm lấy.
- `pickups` chứa ít nhất một điểm. ID là chuỗi phân biệt hoa thường, có ít nhất một ký tự khác khoảng trắng. Các điểm lấy phải có ID và tọa độ riêng. Lấy hàng tại ô xuất phát và ở các ô đi qua không phát sinh chi phí riêng.

Xem sáu [bản đồ mẫu](maps/) hoặc schema đầy đủ trong [DESIGN.md](DESIGN.md).

## Benchmark, plotting và dữ liệu đã lưu

```powershell
python -m bonus.warehouse.benchmark --profile quick
python -m bonus.warehouse.plotting
python -m bonus.warehouse.benchmark --profile full
python -m bonus.warehouse.plotting --profile full
python -m bonus.warehouse.benchmark --help
python -m bonus.warehouse.plotting --help
```

`quick` kiểm tra toàn bộ pipeline. `full` dùng nhiều bản đồ và seed hơn. Benchmark lưu bản đồ, danh sách nhiệm vụ và từng kết quả trong `results/<profile>/<mã cấu hình>/` bên dưới module. Chạy lại cùng cấu hình tiếp tục các mẫu còn thiếu. Dùng `--output-dir PATH` để chọn thư mục đầu ra khác. Plotting mặc định vẽ lần quick mới nhất và hỗ trợ `--run-dir PATH` để chỉ định dữ liệu cụ thể.

- [Kịch bản demo](DEMO.md) có bốn ca, các bước trình bày và kết quả đã đo.
- [Báo cáo](REPORT.md) phân tích kết quả full và ghi lệnh tái lập. [Tiến độ](PROGRESS.md) lưu các lần kiểm tra.
- [Bảng quick](results/quick/499428006f3cdd0d2ad4/summary.md) và [đồ thị quick](results/quick/499428006f3cdd0d2ad4/figures/).
- [Bảng full](results/full/80bda12138afbdcca4ef/summary.md), [dữ liệu thô full](results/full/80bda12138afbdcca4ef/raw/) và [đồ thị full](results/full/80bda12138afbdcca4ef/figures/).
