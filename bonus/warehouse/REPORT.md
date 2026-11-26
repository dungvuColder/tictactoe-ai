# Bài 2 bonus · Ứng dụng A* vào lập kế hoạch lấy hàng cho robot kho

## 1. Bài toán thực tế và phạm vi mô phỏng

Robot kho cần chọn đường đi qua các vị trí lấy hàng với tổng chi phí di chuyển thấp. Đường ít bước có thể tốn nhiều hơn nếu đi qua ô có chi phí cao. Khi đơn hàng có nhiều điểm lấy, thứ tự ghé cũng ảnh hưởng đến tổng chi phí.

Bài này mô phỏng **một robot trên lưới tĩnh, biết trước**. Kệ cản đường, robot đi bốn hướng và tự động lấy hàng khi đến ô có hàng thuộc nhiệm vụ. Lấy hàng có chi phí bằng 0 và tải trọng không giới hạn. Nhiệm vụ một đích kết thúc tại điểm lấy đã chọn. Nhiệm vụ nhiều điểm yêu cầu lấy đủ hàng và về depot. Chi phí ô là số nguyên dùng để mô phỏng, chưa được hiệu chỉnh bằng dữ liệu vận hành của kho thật.

## 2. PEAS

| Thành phần | Mô hình |
|---|---|
| **P · Thước đo hiệu năng** | Hoàn thành nhiệm vụ, tối thiểu hóa tổng chi phí. Khi đánh giá bộ lập kế hoạch, ghi thêm số bước, số nút, thời gian và tỷ lệ thành công. |
| **E · Môi trường** | Lưới hữu hạn có kệ, lối đi, ô xuất phát, depot và các điểm lấy hàng. Môi trường tĩnh, xác định và quan sát đầy đủ. |
| **A · Cơ cấu tác động** | Di chuyển lên, phải, xuống hoặc trái một ô. Hệ thống tự động ghi nhận hàng ở ô robot đến. |
| **S · Cảm biến** | Đầu vào mô phỏng là bản đồ JSON, tọa độ robot và danh sách hàng cần lấy. Trạng thái phần mềm theo dõi các món đã lấy. |

## 3. Mô hình tìm kiếm

- **Trạng thái.** Một đích dùng tọa độ `(hàng, cột)`. Nhiều điểm dùng `(vị trí, bitmask)`, với bit thứ *i* đánh dấu hàng thứ *i*. Cùng vị trí với hai bitmask khác nhau là hai trạng thái. Hàng tại ô xuất phát được ghi nhận ngay.
- **Hành động và chuyển trạng thái.** Một bước đi tới ô kề theo bốn hướng nếu ô đó nằm trong lưới và đi được. Khi vào ô có hàng thuộc nhiệm vụ, đặt bit tương ứng.
- **Đích.** Với một đích, tọa độ robot bằng tọa độ điểm lấy đã chọn. Với nhiều điểm, bitmask phải đầy và robot phải ở depot. Đi ngang depot khi chưa đủ hàng vẫn phải tiếp tục.
- **Chi phí.** Mỗi bước cộng chi phí của ô đến, kể cả bước quay về depot. Ô xuất phát không bị tính phí lúc khởi tạo. Một tuyến được chấm theo tổng chi phí, với số bước ghi riêng.

## 4. Thuật toán so sánh

| Thuật toán | Quy tắc tìm kiếm |
|---|---|
| BFS | Hàng đợi FIFO. Tối ưu số bước, và bảo đảm tối ưu chi phí khi mọi bước có cùng chi phí. |
| UCS | Ưu tiên chi phí đã đi `g`. Làm mốc chi phí tối ưu với chi phí bước dương. |
| Greedy Best-First | Ưu tiên ước lượng còn lại `h`. Có thể chọn tuyến đắt vì quyết định ưu tiên dựa trên `h`. |
| A* | Ưu tiên `g + h`. Ở bài nhiều điểm, tìm trên toàn bộ trạng thái vị trí và bitmask. |
| Nearest-neighbor | Mỗi chặng dùng UCS để tìm điểm chưa lấy có chi phí đường đi thực tế nhỏ nhất. Khi đủ hàng, dùng UCS về depot. Cách tối ưu từng chặng có thể cho tuyến toàn cục đắt hơn. |

Các thuật toán kiểm tra đích khi lấy trạng thái hợp lệ khỏi frontier và dùng bảng trạng thái cha để truy vết. UCS và A* lưu `best_g`, bỏ phần tử heap đã cũ và mở lại trạng thái nếu tìm được chi phí nhỏ hơn. Nearest-neighbor cộng số nút của các chặng và dùng chung ngân sách thời gian, số nút cho toàn tuyến.

## 5. Heuristic và lập luận cận dưới

Gọi `m` là chi phí nhỏ nhất của một ô đi được và `d(u,v)` là khoảng cách Manhattan. Để đi từ `u` đến `v` cần ít nhất `d(u,v)` bước, mỗi bước tốn ít nhất `m`. Vì vậy `m × d(u,v)` là cận dưới của chi phí thực, kể cả khi có vật cản hoặc trọng số khác nhau. A* và Greedy một đích dùng cận này tới điểm lấy đã chọn.

- **`h_max`.** Khi còn hàng, lấy giá trị lớn nhất của `m × d(vị trí, điểm lấy)` trên các điểm chưa lấy. Tuyến hợp lệ phải đến từng điểm, nên chi phí toàn tuyến ít nhất bằng giá trị lớn nhất đó. Khi đã đủ hàng, dùng cận Manhattan tới depot.
- **`h_mst`.** Dùng Prim để tính cây khung nhỏ nhất trên các tọa độ phân biệt gồm vị trí robot, điểm chưa lấy và depot, với cạnh trọng số `m × d(u,v)`. Trên bất kỳ tuyến hợp lệ nào, các đoạn giữa những lần ghé các tọa độ cần thiết tạo một đồ thị liên thông. Tổng cận Manhattan của các đoạn ấy không vượt chi phí tuyến thật. Đồ thị đó chứa một cây khung, nên chi phí MST cũng không vượt chi phí tuyến thật.

Hai heuristic nhiều điểm đều bằng 0 tại đích. Kiểm thử trên lưới nhỏ còn đối chiếu giá trị heuristic với chi phí còn lại do UCS tìm được.

## 6. Thiết kế thực nghiệm và ngân sách

| Nhóm full | Cỡ lưới (ô/cạnh) | Mật độ cản danh nghĩa | Mỗi nhiệm vụ | Số nhiệm vụ |
|---|---|---|---|---:|
| Một đích, đồng nhất | 12, 24, 40, 64 | 10%, 25%, 40% | BFS, UCS, Greedy, A* | 72 |
| Một đích, có trọng số | 12, 24, 40, 64 | 10%, 25%, 40% | UCS, Greedy, A* | 72 |
| Nhiều điểm, có trọng số | 8, 12, 16 | 10%, 30% | UCS, A* max, A* MST, nearest-neighbor | 108 |

Full dùng sáu seed `11, 29, 47, 71, 101, 137`. Nhiệm vụ nhiều điểm dùng 1, 3 hoặc 5 điểm lấy hàng. Ba nhiệm vụ cùng bản đồ dùng các tiền tố của cùng danh sách điểm. Hai nhóm một đích có bố trí vật cản giống nhau khi cỡ, mật độ và seed trùng nhau. Giữ cả các bản đồ có đích hoặc hàng bị cô lập.

Mỗi lượt có ngân sách **2 giây theo đồng hồ và 50.000 lần mở rộng**, áp dụng chung cho các chặng của nearest-neighbor. Chạy tuần tự, xoay thứ tự thuật toán giữa các nhiệm vụ, dùng đối tượng bản đồ mới cho mỗi lượt và tắt GUI cùng callback sự kiện. Đồng hồ bắt đầu sau khi đọc JSON, gồm khởi tạo bài toán, tính heuristic, tìm kiếm và dựng kết quả. Một lượt dừng tại điểm kiểm tra ngân sách. Frontier lớn nhất đếm số phần tử, còn RAM cần phép đo riêng.

Quick trước đó ghi 152 lượt với tổng thời gian đo **0,7438 giây** và lượt dài nhất **63,63 ms**. Với 936 lượt, riêng tổng trần 2 giây mỗi lượt là 1.872 giây nếu tất cả chạm ngưỡng. Thực tế full được chạy với **ngân sách 300 giây cho cả tiến trình**. Bộ hẹn giờ sẽ ngắt chương trình sau ngưỡng này, còn tệp JSON hoàn chỉnh của từng lượt cho phép chạy tiếp.

## 7. Kết quả thực sự đã chạy

**Full hoàn thành 936/936 lượt trên 180 bản đồ và 252 nhiệm vụ.** Có 680 lượt thành công và 256 lượt `no_path`. Timeout, giới hạn nút, hủy và lượt thiếu đều bằng 0. Benchmark chạy trên CPython 3.11.8, Windows 10 AMD64, 16 CPU logic, với một tiến trình đo tuần tự. Tổng thời gian đo của 936 lượt là **10,2826 giây**. Lượt dài nhất là **217,58 ms** với A* MST trên `multi-weighted-16-d10-s11-p5`. Mốc ghi bản ghi đầu và cuối cách nhau **15,81 giây**, trong đó có thời gian ghi tệp giữa các lượt. Lệnh chạy lại nhận đủ 936 bản ghi và đo thêm 0 lượt.

| Nhóm | Thuật toán | Thành công mỗi thuật toán | Vô nghiệm mỗi thuật toán |
|---|---|---:|---:|
| Một đích, đồng nhất | BFS, UCS, Greedy, A* | 44/72 (61,11%) | 28 |
| Một đích, có trọng số | UCS, Greedy, A* | 44/72 (61,11%) | 28 |
| Nhiều điểm, có trọng số | UCS, A* max, A* MST, nearest-neighbor | 93/108 (86,11%) | 15 |

Nguồn dữ liệu full với mã cấu hình `80bda12138afbdcca4ef03b3e5119ebefbd0d25f8111ee86f429c2e05a1a6bf6`.

- [Manifest và thông số](results/full/80bda12138afbdcca4ef/manifest.json), [danh sách nhiệm vụ](results/full/80bda12138afbdcca4ef/tasks.json), [bản đồ JSON](results/full/80bda12138afbdcca4ef/maps) và [dữ liệu từng lượt](results/full/80bda12138afbdcca4ef/raw).
- [Bảng tổng hợp theo cỡ, mật độ và số điểm](results/full/80bda12138afbdcca4ef/summary.md).
- [Nút mở rộng theo kích thước](results/full/80bda12138afbdcca4ef/figures/expanded_by_size.png) và [thời gian theo kích thước](results/full/80bda12138afbdcca4ef/figures/time_by_size.png).
- [Tỷ số chi phí so với UCS](results/full/80bda12138afbdcca4ef/figures/cost_ratio_vs_ucs.png) và [số nút, thời gian theo số điểm lấy](results/full/80bda12138afbdcca4ef/figures/multi_by_pickups.png).

Bảng và đồ thị nút, thời gian dùng trung vị trên các nhiệm vụ có nghiệm ở mọi thuật toán trong cùng phép so sánh. Các lượt vô nghiệm và lượt chạm giới hạn được đếm trong bảng trạng thái. Tỷ số chi phí dùng từng cặp thành công cùng nhiệm vụ có nghiệm UCS với chi phí dương. Dữ liệu quick phục vụ kiểm tra pipeline và được giữ trong [thư mục riêng](results/quick/499428006f3cdd0d2ad4/).

## 8. Phân tích

### 8.1 A* đối chiếu với UCS

A* và UCS trả cùng chi phí ở **44/44** cặp thành công trên bản đồ đồng nhất, **44/44** trên bản đồ có trọng số một đích và **93/93** cho mỗi heuristic nhiều điểm. Trạng thái kết thúc cũng trùng nhau trong toàn bộ nhiệm vụ đối chiếu. BFS cùng chi phí với UCS ở 44/44 cặp đồng nhất.

Ở một đích, A* mở rộng ít nút hơn UCS trong **44/44** nhiệm vụ đồng nhất và **33/44** nhiệm vụ có trọng số. Thời gian A* thấp hơn UCS lần lượt ở **21/44** và **5/44** nhiệm vụ. Ví dụ ở lưới có trọng số 64×64, trên 11 nhiệm vụ thành công chung, trung vị số nút giảm từ **3.664** xuống **3.657**, còn trung vị thời gian tăng từ **24,177 ms** lên **29,444 ms**. Cận Manhattan dùng chi phí bước thấp nhất có thể khá lỏng khi nhiều ô đắt hơn và có đường vòng quanh kệ. Trong nhóm này, số nút tiết kiệm được nhỏ so với tổng số nút.

### 8.2 Chi phí tính MST

Bảng dưới dùng các nhiệm vụ thành công chung theo số điểm lấy, gộp các kích thước và mật độ tương ứng. Mỗi ô ghi **trung vị số nút mở rộng / trung vị thời gian (ms)**.

| Điểm lấy | n chung | UCS | A* max | A* MST | Nearest-neighbor |
|---:|---:|---:|---:|---:|---:|
| 1 | 32 | 192,5 / 2,238 | 170 / 2,540 | 155 / 3,316 | 130,5 / 1,071 |
| 3 | 31 | 979 / 11,426 | 975 / 14,861 | 971 / 18,474 | 256 / 1,896 |
| 5 | 30 | 3.924 / 45,839 | 3.833 / 60,313 | 3.750 / 89,503 | 310 / 2,607 |

So với A* max, MST mở rộng ít nút hơn ở **20/32**, **28/31** và **29/30** nhiệm vụ ứng với 1, 3 và 5 điểm. MST nhanh hơn max ở **8/32** nhiệm vụ một điểm và **0** nhiệm vụ trong hai nhóm còn lại. Với 5 điểm, trung vị của tỷ số theo từng cặp `MST/max` là **0,9856** cho số nút và **1,4705** cho thời gian. Mức tiết kiệm khoảng 1,44% số nút đi cùng thời gian cao hơn khoảng 47,05% theo các tỷ số trung vị này. Trên tập full này, lợi ích giảm mở rộng của MST chưa bù được thời gian tính toán khi có 3 hoặc 5 điểm. Đo theo từng lượt bao gồm toàn bộ chi phí tìm kiếm. Thí nghiệm chưa tách thời gian riêng của Prim khỏi các thao tác khác.

### 8.3 Đánh đổi của Greedy và nearest-neighbor

| So với UCS trên cùng nhiệm vụ | Cặp có nghiệm | Cặp chi phí cao hơn | Trung vị chi phí/UCS | Tỷ số cao nhất |
|---|---:|---:|---:|---:|
| Greedy, một đích đồng nhất | 44 | 36 | 1,0781 | 1,5455 |
| Greedy, một đích có trọng số | 44 | 44 | 1,5814 | 1,8701 |
| Nearest-neighbor, 1 điểm | 32 | 0 | 1,0000 | 1,0000 |
| Nearest-neighbor, 3 điểm | 31 | 4 | 1,0000 | 1,04494 |
| Nearest-neighbor, 5 điểm | 30 | 17 | 1,01667 | 1,1600 |

Greedy mở rộng ít nút hơn UCS trên cả 88 nhiệm vụ một đích có nghiệm. Đổi lại, ở [mẫu có trọng số 40×40](results/full/80bda12138afbdcca4ef/maps/single-weighted-40-d10-s11.json), Greedy tốn **475** so với **254** của UCS. Nearest-neighbor có trung vị **2,607 ms** so với **45,839 ms** của UCS ở nhóm 5 điểm. Ở [mẫu 8×8 có 5 điểm](results/full/80bda12138afbdcca4ef/maps/multi-weighted-8-d30-s137.json), các chặng tối ưu cục bộ cộng lại thành **145**, còn UCS trên trạng thái đầy đủ đạt **125**. Ví dụ này và số cặp thua cho thấy trung vị gộp bằng 1 vẫn có thể đi cùng các tuyến kém hơn.

### 8.4 Vô nghiệm và kết quả ngoài kỳ vọng

Một phép duyệt liên thông độc lập trên các ô đi được khớp với trạng thái của cả 936 lượt. Nó xác nhận **71 nhiệm vụ không thể tới đủ đích cần thiết**, tương ứng với 256 bản ghi `no_path`. Với mỗi chế độ chi phí một đích, cả **24/24** nhiệm vụ ở mật độ danh nghĩa 40% đều vô nghiệm. Ở 25% có **4/24**, còn 10% có **0/24**. Với nhiều điểm, 15 nhiệm vụ vô nghiệm đều thuộc mật độ 30%. Việc giữ các ca này cho thấy khả năng tiếp cận của bố trí kho ảnh hưởng đến tỷ lệ hoàn thành trước khi so sánh thuật toán.

Đồ thị thời gian theo kích thước vì thế chỉ dùng các nhiệm vụ có đường. Ở một đích, tỷ lệ thất bại cao trong nhóm mật độ 40% làm thay đổi thành phần mẫu dùng để lấy trung vị. Hơn nữa, việc A* giảm số nút nhưng nhiều lần vẫn chậm hơn UCS là một kết quả đo được, phù hợp với việc heuristic cũng tiêu tốn thời gian.

## 9. Hạn chế và hướng mở rộng

- Lưới, trọng số và vật cản là dữ liệu tổng hợp. Một robot đi bốn hướng trên bản đồ tĩnh chưa thể hiện động học, pin, tải trọng, người đi bộ hay xung đột giữa robot.
- Full khảo sát tối đa năm điểm lấy hàng và sáu seed. Không gian trạng thái tăng theo số bit hàng, nên kết quả của lưới nhỏ chưa định lượng được khả năng mở rộng ở đơn lớn. Mỗi biến thể chỉ đo một lần trên mỗi nhiệm vụ và trên một môi trường. Sai khác nhỏ về thời gian có thể do tải máy.
- Các hướng mở rộng gồm dùng bản đồ có lối đi và trọng số được hiệu chỉnh, tách tập liên thông để đánh giá khả năng lập kế hoạch, đo lặp với thứ tự hoán đổi, và thử các cận dưới có tính đến đường vòng. Đánh giá robot thực tế hoặc nhiều robot cần dữ liệu và mô hình chuyển động phù hợp.

## 10. Lệnh tái lập

Từ gốc repo, chạy cùng mã nguồn với Python đã cài các gói trong `requirements.txt`. Các lệnh mặc định tiếp tục cấu hình có sẵn hoặc tạo thư mục mới khi thay đổi môi trường hay mã tính toán.

```powershell
python -m bonus.warehouse.benchmark --profile full
python -m bonus.warehouse.plotting --profile full
```

Lần đo đã lưu dùng lệnh PowerShell dưới đây để giữ ngân sách chung 300 giây. Lệnh CLI chạy trực tiếp sau đó xác nhận hồ sơ đã hoàn tất. Bảng và biểu đồ trong báo cáo được tạo bằng Matplotlib 3.11.2 trên CPython portable.

```powershell
@'
from _thread import interrupt_main
from threading import Timer
from bonus.warehouse.benchmark import main
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
timer = Timer(300, interrupt_main)
timer.daemon = True
timer.start()
try:
    raise SystemExit(main(["--profile", "full"]))
finally:
    timer.cancel()
'@ | python -u -

python -m bonus.warehouse.benchmark --profile full
.\.venv\warehouse-cpython\python.exe -m bonus.warehouse.plotting --profile full --run-dir bonus/warehouse/results/full/80bda12138afbdcca4ef
```

Để đo lại độc lập, thêm `--output-dir PATH` với một thư mục mới rồi dùng cùng đối số với plotting. Profile quick đã chạy ở lượt 7 và full đã chạy đủ ở lượt 8. Trong ma trận full hiện tại, không còn cấu hình chưa chạy.
