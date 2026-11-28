# Tiến độ Bài 2 bonus

## Đo thời gian lặp

- Thêm `--repeats` và `--warmups` vào benchmark. Schema 2 lưu chỉ số lượt đo, quy tắc xoay thứ tự, cấu hình và nhật ký phiên. Resume làm nóng những biến thể còn lượt thiếu rồi chỉ đo phần thiếu. Schema 1 tiếp tục đọc được, với đầu ra phân tích ở thư mục bên cạnh.
- Plotting tách IQR trong cùng nhiệm vụ khỏi Q1–Q3 giữa các nhiệm vụ. Tập so sánh dùng một trung vị thời gian mỗi nhiệm vụ và yêu cầu các biến thể có đủ lượt thành công, kết quả nhất quán. Các lượt thiếu, trạng thái hỗn hợp và kết quả xác định sai khác có ghi chú riêng.
- `python -m bonus.warehouse.benchmark --profile quick --repeats 3 --warmups 1` ghi 456/456 lượt chính thức trên 40 nhiệm vụ. Chạy lại cùng lệnh giữ 456 và thêm 0 lượt. Kết quả nằm ở `results/quick/e3e485108211f8988adf/`.
- `python -u -m bonus.warehouse.benchmark --profile full --repeats 5 --warmups 1` ghi 4.680/4.680 lượt chính thức trên 252 nhiệm vụ, trong `results/full/2784d6551c6e7550b5b6/`. Chạy plotting bằng CPython portable và `--run-dir` cho từng thư mục. Đã vẽ thử một bản sao dữ liệu cũ để xác minh tương thích.
- `.venv/warehouse-cpython/python.exe -m unittest discover -s tests -p 'test_warehouse*.py' -v` đạt 54/54. `python tests/test_all.py` đạt 8/8. Không sửa bộ giải hay hai bộ kết quả schema 1.
- Báo cáo phân biệt phép đo lặp với phép đo một lượt. Số đo trên một máy và các thanh phân tán mô tả mẫu quan sát được, chưa đánh giá khác biệt giữa các máy.

## Sửa lỗi khởi tạo GUI

- **Nguyên nhân.** Khi kiểm tra ID hàng hoặc nạp bản đồ trong `WarehouseApp`, lỗi đầu vào thoát ra điểm chạy GUI dưới dạng traceback.
- **Cách sửa.** `gui.py` chuyển lỗi đọc hoặc parse bản đồ và ID không tồn tại thành lỗi đầu vào riêng, rồi báo qua `argparse` với mã 2. Thông báo ID liệt kê các lựa chọn trên bản đồ. Khối `finally` dọn Pygame, kể cả khi khởi tạo dở. Lỗi lập trình xảy ra ngoài phần xác thực đầu vào vẫn được truyền ra.
- **Kiểm tra.** `.venv/warehouse-cpython/python.exe -m unittest discover -s tests -p test_warehouse_gui.py -v` đạt 9/9 với SDL dummy. `.venv/warehouse-cpython/python.exe -m unittest discover -s tests -p 'test_warehouse*.py'` đạt 49/49. `python tests/test_all.py` đạt 8/8.
- **Xác minh CLI.** Chạy bằng CPython portable với SDL dummy và `PYTHONIOENCODING=cp1252`. `--pickup DOES_NOT_EXIST --frames 1` trả mã 2, báo tiếng Việt UTF-8 và liệt kê ID `A` trên bản đồ mặc định, không in traceback. `--pickup A --frames 1` trả mã 0.
- Thuật toán và kết quả benchmark giữ nguyên.

## Lượt 9 · Nghiệm thu

### Đã hoàn thành

- Đối chiếu PROGRESS, DESIGN, REPORT và README gốc với API và các entry point. Tạo README riêng của module và DEMO với bốn kịch bản đã chạy. README gốc bổ sung mục Bài 2 sau phần Bài 1.
- Sửa `gui --help` để xuất UTF-8 trên Windows khi stdout mặc định là CP1252. Thêm kiểm thử hồi quy. Mã thuật toán và benchmark giữ nguyên, đối chiếu thành công với dấu băm trong manifest full.

### File và API quan trọng

- `bonus/warehouse/README.md` có hướng dẫn cài đặt, CLI, GUI, schema, giới hạn và liên kết dữ liệu.
- `bonus/warehouse/DEMO.md` có cấu hình, thao tác và số đo cho bốn kịch bản. REPORT.md dẫn đến dữ liệu và biểu đồ full.

### Kiểm tra đã chạy

- `python -m unittest discover -s tests -p 'test_warehouse*.py'` đạt 45/45 khi dùng CPython portable với Pygame. `python tests/test_all.py` đạt 8/8.
- `--help` của `cli`, `gui`, `benchmark` và `plotting` đều thoát mã 0 sau bản sửa.
- CLI chạy UCS và A* trên `detour.json`, BFS, UCS và A* trên `weighted.json`, A* MST và nearest-neighbor trên `nearest_neighbor_trap.json`, và A* trên `no_path.json`. Ca cuối trả `no_path` với mã thoát 1.
- `python -m bonus.warehouse.benchmark --profile quick --output-dir .venv/warehouse-acceptance-round9` tạo mới 152/152 bản ghi. `python -m bonus.warehouse.plotting --profile quick --output-dir .venv/warehouse-acceptance-round9` tạo bảng và bốn PNG từ lần chạy đó.
- GUI smoke test bằng SDL dummy và driver Windows. Đã xem ảnh render Windows của tuyến nhiều điểm và trạng thái không có đường. Luồng thao tác được kích hoạt bằng sự kiện kiểm thử.
- Xác minh các liên kết tài liệu, phần Bài 1 trong README gốc và 936 bản ghi full đã lưu. Không chạy lại full và không sửa kết quả Bài 1.

### Hạn chế còn lại

- GUI dùng sáu bản đồ mẫu, cửa sổ cố định và mô hình một robot trên lưới tĩnh. Bản Python dùng để mở GUI cần Pygame, còn plotting cần Matplotlib. Máy nghiệm thu dùng CPython portable cho hai phần này.

### Bước tiếp theo

- Module đã đủ điều kiện demo cả CLI và GUI theo DEMO.md.

## Lượt 8 · Chạy full và viết báo cáo

### Đã hoàn thành

- Kiểm tra 152 bản ghi quick. Tổng thời gian đo là 0,7438 giây và lượt dài nhất là 63,63 ms. Profile full có 936 lượt, mỗi lượt tối đa 2 giây và 50.000 lần mở rộng. Dùng bộ hẹn giờ 300 giây cho cả tiến trình và cơ chế tiếp tục từ từng tệp JSON.
- Chạy đủ 936/936 lượt full trên 180 bản đồ và 252 nhiệm vụ. Có 680 lần thành công, 256 lần vô nghiệm và 0 lượt chạm giới hạn, hủy hoặc còn thiếu.
- Tạo lại bảng và bốn biểu đồ từ số liệu full. Kiểm tra liên thông trực tiếp trên lưới khớp với tất cả trạng thái. A* cùng chi phí với UCS trên mọi cặp có nghiệm.
- Viết REPORT.md với mô hình PEAS, thuật toán, heuristic, kết quả, phân tích đánh đổi, hạn chế và lệnh tái lập.

### File và API quan trọng

- `bonus/warehouse/REPORT.md` là báo cáo Bài 2.
- `bonus/warehouse/results/full/80bda12138afbdcca4ef/` chứa manifest, bản đồ, nhiệm vụ, cả 936 bản ghi, bảng Markdown và biểu đồ. Dữ liệu quick nằm ở thư mục riêng từ lượt 7.

### Kiểm tra đã chạy

- Chạy entry point benchmark với `--profile full` và bộ hẹn giờ 300 giây trong PowerShell. Lệnh đầy đủ được lưu ở mục 10 của REPORT.md. Tổng thời gian đo trong các bản ghi là 10,2826 giây.
- `python -m bonus.warehouse.benchmark --profile full` chạy lại và giữ 936 bản ghi, tạo thêm 0 lượt.
- `python -m bonus.warehouse.plotting --profile full --run-dir bonus/warehouse/results/full/80bda12138afbdcca4ef` chạy bằng CPython portable có Matplotlib 3.11.2 và tạo bảng cùng bốn PNG.
- `python -m unittest discover -s tests -p 'test_warehouse*.py'` đạt 44/44 với CPython portable. `python tests/test_all.py` đạt 8/8.

### Hạn chế còn lại

- Toàn bộ cấu hình full hiện tại đã chạy. Dữ liệu này dùng lưới mô phỏng, tối đa năm điểm lấy hàng và một phép đo thời gian trên mỗi nhiệm vụ–thuật toán.

### Bước tiếp theo

- Nếu được giao đo thêm, dùng thư mục đầu ra mới cho số liệu lặp hoặc bản đồ kho có cấu trúc.

## Lượt 7 · Benchmark và biểu đồ

### Đã hoàn thành

- Thêm hai profile với kích thước, mật độ, seed và giới hạn riêng. Các thuật toán trong một phép so sánh nhận cùng bản đồ, nhiệm vụ và ngân sách.
- Lưu bản đồ JSON, nhiệm vụ, manifest cấu hình và số liệu từng lần chạy. Mã cấu hình gắn với dữ liệu, mã nguồn và môi trường. Khi tiếp tục, giữ các bản ghi hợp lệ và chỉ chạy phần thiếu.
- Đo thời gian gồm khởi tạo bài toán, tính heuristic và toàn bộ các chặng. Tắt GUI và callback sự kiện. Ghi riêng các trạng thái thất bại và giữ số lần còn thiếu trong bảng.
- Thêm bảng Markdown và bốn biểu đồ. Chi phí, thời gian và số nút dùng tập thành công chung. Tỷ số chi phí dùng từng cặp nghiệm có UCS với chi phí dương.

### File và API quan trọng

- `benchmark.py` cung cấp CLI, hai profile, thư mục kết quả theo mã cấu hình và chức năng tiếp tục.
- `plotting.py` tổng hợp một thư mục chạy. Các đầu ra là `summary.md`, `expanded_by_size.png`, `time_by_size.png`, `cost_ratio_vs_ucs.png` và `multi_by_pickups.png`.
- Dữ liệu quick nằm trong `bonus/warehouse/results/quick/499428006f3cdd0d2ad4/`. Quy trình và cách đọc dữ liệu được ghi trong README và DESIGN.

### Kiểm tra đã chạy

- `python -m bonus.warehouse.benchmark --profile quick` ghi 152/152 lần chạy trên 24 bản đồ và 40 nhiệm vụ. Có 107 lần thành công và 45 lần vô nghiệm. Chạy lại cùng lệnh giữ nguyên 152 bản ghi.
- `python -m bonus.warehouse.plotting` với CPython portable và Matplotlib 3.11.2 tạo bảng và bốn PNG. Đã xem ảnh để kiểm tra trục, đường chuẩn UCS, cỡ mẫu và nhãn quick.
- Chạy plotting trên bản sao tạm chỉ có 45 bản ghi thất bại. Bảng và bốn biểu đồ được tạo khi còn thiếu dữ liệu và không có nghiệm UCS tham chiếu. Kiểm tra trực tiếp hai ngân sách bằng 0 trên một nhiệm vụ quick xác nhận `timeout` và `node_limit` được ghi riêng.
- `python -m unittest discover -s tests -p 'test_warehouse*.py'` đạt 44/44 với CPython portable. `python tests/test_all.py` đạt 8/8. Kiểm tra Git xác nhận không có thay đổi dưới `results/` của Bài 1.

### Hạn chế còn lại

- Lượt này chỉ chạy quick để xác nhận pipeline. Profile full gồm 936 lần chạy theo thiết kế và chưa được thực thi. Các thời gian quick là số đo kiểm tra trên môi trường hiện tại.

### Bước tiếp theo

- Khi được giao thực nghiệm full, chạy profile full và vẽ kết quả từ mã cấu hình tương ứng.

## Lượt 6 · Giao diện robot kho

### Đã hoàn thành

- Thêm giao diện Pygame cho sáu bản đồ mẫu, hai chế độ lấy hàng, bộ chọn thuật toán, điểm đích hoặc heuristic, Run, Pause/Resume, Reset và tốc độ.
- Vẽ kệ, lối đi và chi phí ô, depot, hàng, robot, ô đã mở rộng và đường đi. Robot phát lại toàn bộ đường đi và đánh dấu món đã lấy. Panel hiển thị trạng thái, chi phí, số bước, số nút, frontier, thời gian và thứ tự lấy hàng.
- Luồng nền chỉ gọi API tìm kiếm. Hàng đợi mang ID tác vụ, kết quả hoặc lỗi. Reset, đổi bản đồ và đóng cửa sổ đặt cờ hủy và loại bỏ phản hồi cũ.
- Giới hạn mặc định 1.000 sự kiện trung gian. GUI báo tỷ lệ lần mở rộng ghi được và giữ đầy đủ kết quả. Tốc độ và Pause chỉ áp dụng cho phát lại, sau khi có kết quả.

### File và API quan trọng

- `bonus/warehouse/gui.py` là điểm khởi động. `WarehouseApp` xử lý Pygame, luồng nền và phát lại.
- `planning.py` mở rộng `nearest_neighbor` với `on_event` và `max_events` dùng chung qua các chặng UCS.
- `tests/test_warehouse_gui.py` kiểm tra thao tác và vòng đời tác vụ với SDL dummy. README và DESIGN ghi cách chạy và cơ chế phát lại.

### Kiểm tra đã chạy

- `python -m unittest discover -s tests -p 'test_warehouse*.py' -v` với CPython 3.11.9 portable và Pygame 2.6.1 đạt 42/42. Kiểm tra một đích, nhiều điểm, nearest-neighbor, không có đường, Pause/Resume, tốc độ, replay bị giới hạn, Reset khi đang tìm, đổi bản đồ, đóng cửa sổ và lỗi luồng nền.
- `python tests/test_all.py` đạt 8/8 cho Bài 1.
- Với `SDL_VIDEODRIVER=dummy`, chạy `python -m bonus.warehouse.gui` với các nhóm tham số `--frames 4`, `--autostart --frames 20`, `--map multi_pickup --mode multi --algorithm astar --heuristic mst --autostart --frames 40` và `--map no_path --autostart --frames 20`. Cả bốn thoát mã 0.
- Đã xem ảnh render SDL dummy để kiểm tra bố cục và ký hiệu hàng đã lấy.

### Hạn chế còn lại

- Kiểm thử tương tác dùng sự kiện Pygame trong SDL dummy. Chưa thao tác trực quan trên cửa sổ thật. GUI có kích thước cố định và dùng các bản đồ mẫu.

### Bước tiếp theo

- Khi được giao benchmark, chạy API tìm kiếm với callback sự kiện tắt và dùng cùng cấu hình giới hạn cho các lượt so sánh.

## Lượt 5 · Rà soát thuật toán và đối chứng độc lập

### Đã hoàn thành

- Rà soát cách tính chi phí khi vào ô đích, truy vết bảng cha, kiểm tra đích khi lấy khỏi frontier, cập nhật `best_g`, bỏ entry cũ và mở lại trạng thái.
- Kiểm tra bitmask tại ô xuất phát và từng bước di chuyển, điều kiện về depot, hệ số chi phí ô đi được nhỏ nhất trong các heuristic và cách nearest-neighbor chọn chặng theo chi phí thật.
- Đối chiếu cách phân biệt `success`, `no_path`, `timeout`, `node_limit`, `cancelled` và quy tắc đếm nút mở rộng, nút sinh, đỉnh frontier, thời gian và ngân sách cộng dồn qua các chặng.
- Bổ sung một ví dụ có đáp án tính tay và 16 bản đồ sinh từ seed `20261126`. Bộ đối chứng dùng Floyd–Warshall có hướng tính trực tiếp từ lưới và vét cạn thứ tự ghé với tối đa ba điểm. So sánh cả trạng thái kết thúc và chi phí của UCS, A* một đích và A* nhiều điểm với hai heuristic. Kiểm tra nearest-neighbor theo chi phí nhỏ nhất từng chặng và khi về depot.
- Bộ kiểm tra đường đi đọc trực tiếp lưới để xác nhận hai đầu tuyến, từng bước kề, vật cản, tổng chi phí, bitmask và thứ tự lấy hàng. Các lần chạy đối chứng đều khớp. Mã thuật toán giữ nguyên sau rà soát.

### File và API quan trọng

- `tests/test_warehouse_oracle.py` chứa bộ đối chứng độc lập và bộ kiểm tra đường đi.
- Đối chứng chạy qua các API hiện có `search`, `SingleGoalProblem`, `MultiPickupProblem` và `nearest_neighbor`.

### Kiểm tra đã chạy

- `python -m unittest discover -s tests -p 'test_warehouse*.py' -v` đạt 37/37. Tập cố định có 5 bản đồ không có đường, 7 trường hợp xuất phát tại đích và 4 trường hợp cần di chuyển ở chế độ một đích. Chế độ nhiều điểm có 11 trường hợp thành công và 5 trường hợp không có đường.
- `python tests/test_all.py` đạt 8/8 cho Bài 1.
- `python -m bonus.warehouse.cli --map bonus/warehouse/maps/weighted.json --mode single --algorithm astar --json` trả `success`, 5 bước, chi phí 5.
- `python -m bonus.warehouse.cli --map bonus/warehouse/maps/multi_pickup.json --mode multi --algorithm astar --heuristic mst --json` trả `success`, 12 bước, chi phí 17, lấy A → C → B rồi về depot.
- `python -m bonus.warehouse.cli --map bonus/warehouse/maps/nearest_neighbor_trap.json --mode multi --algorithm nearest_neighbor --json` trả `success`, 8 bước, chi phí 8.

### Hạn chế còn lại

- Bộ đối chứng giới hạn ở lưới tối đa 4×4 và tối đa ba điểm lấy hàng. Chưa đánh giá hiệu năng trên bản đồ lớn. Timeout và hủy được kiểm tra tại các điểm dừng mô tả trong DESIGN.md.

### Bước tiếp theo

- Giữ bộ đối chứng làm kiểm thử hồi quy cho các lượt tích hợp tiếp theo.

## Lượt 4 · Tìm đường nhiều điểm

### Đã hoàn thành

- Chạy UCS và A* trên trạng thái đầy đủ gồm vị trí và bitmask. A* hỗ trợ `h_max` và `h_mst` bằng Prim.
- Thêm nearest-neighbor dùng UCS theo chi phí thật từng chặng, ghi nhận hàng trên từng ô đi qua và chia sẻ giới hạn thời gian, số nút, hủy tìm kiếm.
- Mở rộng CLI với chế độ nhiều điểm, lựa chọn heuristic và thuật toán nearest-neighbor. Thêm bản đồ 2×3 và giải thích tính chấp nhận được của các heuristic trong DESIGN.md.

### File và API quan trọng

- `environment.py` có `MultiPickupProblem(warehouse, heuristic="max")`, `h_max`, `h_mst`, `state_at` và `remaining_positions`.
- `planning.py` có `nearest_neighbor`, trả `SearchResult[MultiState]` và tổng hợp thống kê các chặng.
- `maps/nearest_neighbor_trap.json` và `tests/test_warehouse_multi.py` lưu bản đồ phản ví dụ và kiểm thử nhiều điểm.

### Kiểm tra đã chạy

- `python -m unittest discover -s tests -p 'test_warehouse*.py' -v` đạt 35/35. Kiểm thử đối chiếu hai heuristic với chi phí UCS từ các trạng thái có thể đến trên bản đồ nhỏ.
- `python tests/test_all.py` đạt 8/8 cho Bài 1.
- Chạy `python -m bonus.warehouse.cli --map bonus/warehouse/maps/nearest_neighbor_trap.json --mode multi ... --json` với UCS, A* `max`, A* `mst` và nearest-neighbor. Ba lượt tìm kiếm tối ưu đều trả chi phí 6. Baseline trả chi phí 8. Baseline với `--max-expanded-nodes 2` trả `node_limit` sau đúng hai lần mở rộng.
- Chạy CLI A* `mst` trên `multi_pickup.json` ở dạng văn bản và kiểm tra `--help`. Tuyến thành công lấy A, C, B, quay về depot với chi phí 17.

### Vấn đề còn lại

- Lượt 4 hoàn tất tìm đường nhiều điểm. GUI và benchmark thuộc các lượt sau.

### Bước tiếp theo

- Khi được giao lượt tiếp theo, dùng kết quả đường đi và API sự kiện tìm kiếm đã có cho phần việc được giao.

## Lượt 3 · Tìm đường một đích

### Đã hoàn thành

- Triển khai BFS, UCS, Greedy Best-First và A* dùng giao thức chung. Đích được kiểm tra khi lấy khỏi frontier và đường đi được truy vết qua bảng trạng thái cha. UCS và A* cập nhật `best_g`, bỏ entry cũ và mở lại trạng thái khi chi phí giảm.
- Thêm giới hạn thời gian, số lần mở rộng và cơ chế hủy. Callback sự kiện có hạn mức và gửi riêng sự kiện kết thúc. Benchmark về sau sẽ chạy với callback tắt.
- Thêm CLI một đích hỗ trợ chọn bản đồ, thuật toán, điểm lấy hàng, giới hạn tài nguyên và xuất JSON. Đầu ra UTF-8 đã được kiểm tra trên môi trường có mã hóa mặc định CP1252.

### File và API quan trọng

- `bonus/warehouse/search.py` cung cấp `search`, `SearchProblem`, `SearchResult` và `SearchEvent`. `max_events` giới hạn số sự kiện trung gian. `should_cancel` nhận hàm kiểm tra yêu cầu hủy.
- `bonus/warehouse/cli.py` là điểm chạy từ dòng lệnh. `--pickup ID` chọn đích. Nếu bỏ qua, đích là điểm lấy hàng đầu tiên trong bản đồ.
- `tests/test_warehouse_search.py` kiểm tra đường đi, chi phí, giới hạn, hủy, sự kiện, entry cũ, mở lại trạng thái và đầu ra CLI.

### Kiểm tra đã chạy

- `python -m unittest discover -s tests -p 'test_warehouse*.py' -v` đạt 26/26.
- `python tests/test_all.py` đạt 8/8 cho Bài 1.
- `python -m bonus.warehouse.cli --help` hiển thị hướng dẫn và giới hạn tối ưu của BFS, Greedy.
- Chạy `python -m bonus.warehouse.cli --map bonus/warehouse/maps/weighted.json --algorithm ALG --mode single` cho cả bốn giá trị `bfs`, `ucs`, `greedy`, `astar`. Cả bốn trả `success`. BFS và Greedy có 3 bước, chi phí 19. UCS và A* có 5 bước, chi phí 5. Lượt A* cũng kiểm tra `--pickup A --json`.
- CLI trả riêng `no_path` trên `no_path.json`, `timeout` với `--timeout 0` và `node_limit` với `--max-expanded-nodes 1`. Kiểm thử API xác nhận trạng thái `cancelled`.

### Vấn đề còn lại

- Chế độ CLI và kiểm thử tìm kiếm nhiều điểm, GUI và benchmark thuộc các lượt sau.

### Bước tiếp theo

- Khi được giao phần nhiều điểm, dùng `MultiPickupProblem` với API tìm kiếm chung và kiểm tra tuyến lấy đủ hàng rồi về depot.

## Lượt 2 · Mô hình kho

### Đã hoàn thành

- Triển khai đọc JSON UTF-8, kiểm tra schema phiên bản 1 và thông báo lỗi kèm đường dẫn, trường hoặc ô sai.
- Triển khai lưới chi phí, sinh nước đi theo thứ tự lên, phải, xuống, trái, trạng thái một đích và trạng thái nhiều điểm có bitmask. Hàng tại ô xuất phát được ghi nhận ngay.
- Thêm năm bản đồ mẫu và kiểm thử bằng `unittest`. Cập nhật thiết kế theo module `environment.py` và quy tắc từ chối điểm lấy hàng trùng tọa độ hoặc trùng ID.

### File và API quan trọng

- `bonus/warehouse/environment.py` cung cấp `load_map`, `MAPS_DIR`, `WarehouseMap`, `Pickup`, `MultiState`, `SingleGoalProblem` và `MultiPickupProblem`.
- Hai lớp bài toán cung cấp `initial_state`, `is_goal`, `successors`, `heuristic` và `pickup_order`.
- `bonus/warehouse/maps/` chứa các bản đồ đồng chi phí, đi vòng, chi phí có trọng số, nhiều điểm lấy hàng và đích cô lập. `tests/test_warehouse.py` kiểm tra bộ nạp và chuyển trạng thái.

### Kiểm tra đã chạy

- `python -m unittest discover -s tests -p test_warehouse.py -v` đạt 14/14.
- `python tests/test_all.py` đạt 8/8 cho Bài 1.
- `python -c "from bonus.warehouse.environment import load_map; print(load_map('bonus/warehouse/maps/weighted.json'))"` tải được bản đồ bằng đường dẫn tương đối từ gốc repo.

### Vấn đề còn lại

- Phần môi trường đã hoàn thành. Thuật toán tìm kiếm, CLI, GUI và benchmark còn ở các lượt triển khai sau.

### Bước tiếp theo

- Khi được giao phần tìm kiếm, dùng trực tiếp lớp bài toán trong `environment.py` và API kết quả trong DESIGN.md.

## Lượt 1 · Khảo sát và thiết kế

### Đã hoàn thành

- Đọc README, requirements, nhật ký ban đầu và khảo sát `games/`, `agents/`, `experiments/`, `tests/` cùng vòng lặp Pygame. Không tìm thấy `AGENTS.md` áp dụng cho repo.
- Đọc phần tìm kiếm mù và tìm kiếm có thông tin của tài liệu tóm tắt AI trên ổ D để chốt phạm vi kiến thức.
- Hoàn tất thiết kế bản đồ, bài toán một đích và nhiều điểm, contract tìm kiếm, CLI, phép đo, hủy và sự kiện.

### File và API quan trọng

- `bonus/__init__.py` và `bonus/warehouse/__init__.py` đánh dấu package và chứa mô tả module.
- `bonus/warehouse/DESIGN.md` mô tả schema bản đồ phiên bản 1 và các API dự kiến `load_map`, `SearchProblem`, `SingleGoalProblem`, `MultiPickupProblem`, `search`, `SearchResult`, `SearchEvent`.
- Khóa trạng thái nhiều điểm gồm vị trí và mask hàng đã lấy. Kết quả lưu đường đi theo trạng thái và danh sách ID theo thứ tự lấy.

### Kiểm tra đã chạy

- `python tests/test_all.py` trả mã thoát 0, cả 8 kiểm thử Bài 1 đều PASS trong lượt này.
- Kiểm tra nhanh bằng Python đọc ví dụ JSON từ DESIGN.md, xác nhận lưới và các tọa độ đi được, kiểm tra ID duy nhất và import `bonus.warehouse`. Kết quả PASS.
- `git status --short --untracked-files=all` chỉ liệt kê bốn file trong `bonus/`.

### Vấn đề còn lại

- Lượt 1 hoàn tất phần thiết kế. Mô hình chạy được, thuật toán, CLI, GUI và benchmark thuộc các lượt triển khai.

### Bước tiếp theo

- Khi được giao lượt tiếp theo, triển khai phần được giao theo chữ ký và quy tắc đo trong DESIGN.md.

## Ghi nhận trước lượt 1

### Đã hoàn thành

- Rà soát README, cấu trúc repo và trạng thái Git trước khi bắt đầu. Cây làm việc sạch tại thời điểm kiểm tra.
- Chạy bộ kiểm thử Bài 1 để ghi nhận trạng thái ban đầu.

### File và API quan trọng

- `bonus/warehouse/PROGRESS.md` ghi nhận tiến độ triển khai ứng dụng A* lập kế hoạch lấy hàng cho robot kho.
- API cho mô hình kho và thuật toán tìm đường sẽ được xác định trong lượt triển khai tương ứng.

### Kiểm tra đã chạy

- `git status --short -b` hiển thị `## main...origin/main` trước khi tạo nhật ký.
- `python tests/test_all.py` trả mã thoát 0, cả 8 kiểm thử Bài 1 đều PASS.

### Vấn đề còn lại khi ghi nhận

- Phạm vi triển khai của lượt đầu chưa được giao. Phần bonus hiện mới có nhật ký tiến độ.

### Bước tiếp theo khi ghi nhận

- Xác nhận phạm vi lượt đầu. Một phạm vi đề xuất là mô hình lưới kho, A* cho một điểm đến và kiểm thử đường đi trên bản đồ nhỏ.
