# Thiết kế lập kế hoạch lấy hàng cho robot kho

## Phạm vi và cơ sở thiết kế

Một robot lập kế hoạch trên bản đồ lưới tĩnh đã biết trước. Robot di chuyển một ô theo bốn hướng, tránh kệ và trả chi phí của ô vừa đi vào. Mỗi ô đi được có chi phí nguyên dương. Robot tự động lấy hàng khi đứng ở điểm lấy hàng thuộc nhiệm vụ, kể cả tại vị trí xuất phát. Lấy hàng có chi phí bằng 0 và tải trọng không giới hạn. Nhiệm vụ một đích kết thúc ở điểm lấy hàng đã chọn. Nhiệm vụ nhiều điểm kết thúc ở depot sau khi lấy đủ hàng.

Phần 1–2 của [tài liệu tóm tắt AI](<D:/t_m_t_t_ki_n_th_c_m_n_tr_tu_nh_n_t_o.md>) cung cấp khung phát biểu bài toán, tìm kiếm đồ thị, UCS, A* và điều kiện của heuristic. Mục tiêu tối ưu là tổng chi phí di chuyển. Số bước là một chỉ số riêng.

Repo hiện tách luật trong `games/`, thuật toán trong `agents/`, kiểm thử trong `tests/` và các script đấu loạt, tổng hợp JSON, vẽ biểu đồ trong `experiments/`. `gui.py` xử lý sự kiện và vẽ Pygame trên luồng chính, còn tính nước đi trên luồng nền. Bonus dùng cách tách tương tự trong một package riêng. `requirements.txt` đã có Pygame cho giao diện và Matplotlib cho biểu đồ. Lõi bản đồ và tìm kiếm dùng thư viện chuẩn.

## 1. Định dạng JSON

Ví dụ bản đồ phiên bản 1.

```json
{
  "schema_version": 1,
  "grid": [
    [1, 2, 0, 1],
    [1, 1, 3, 1],
    [1, 0, 1, 1]
  ],
  "start": [0, 0],
  "depot": [0, 0],
  "pickups": [
    {"id": "A", "position": [0, 1]},
    {"id": "B", "position": [2, 3]}
  ]
}
```

- Đọc UTF-8. Đối tượng gốc và mỗi điểm lấy hàng có đúng các trường trong ví dụ. Từ chối khóa JSON lặp và phiên bản khác 1.
- `grid` là ma trận chữ nhật có ít nhất một hàng và một cột. `0` biểu thị kệ, số nguyên dương biểu thị chi phí đi vào ô. Mọi trường số nguyên từ chối boolean, số thực và chuỗi.
- Tọa độ là mảng hai số nguyên `[hàng, cột]`, bắt đầu từ 0, gốc ở góc trên bên trái. `start`, `depot` và mọi điểm lấy hàng phải nằm trong lưới và ở ô đi được. `start` và `depot` có thể trùng nhau hoặc trùng một điểm lấy hàng.
- `pickups` có ít nhất một phần tử. `id` là chuỗi phân biệt hoa thường, có ít nhất một ký tự khác khoảng trắng và duy nhất trong bản đồ. Hai điểm lấy hàng phải có tọa độ khác nhau. Thứ tự phần tử là thứ tự gán bit.
- Bản đồ có thể chứa điểm bị cô lập. Việc xác nhận có đường đi thuộc về thuật toán tìm kiếm.

## 2. Kiểu dữ liệu và chuyển trạng thái

```python
Coord = tuple[int, int]
MAPS_DIR: pathlib.Path

@dataclass(frozen=True)
class Pickup:
    id: str
    position: Coord

@dataclass(frozen=True)
class WarehouseMap:
    grid: tuple[tuple[int, ...], ...]
    start: Coord
    depot: Coord
    pickups: tuple[Pickup, ...]

    @property
    def rows(self) -> int: ...

    @property
    def cols(self) -> int: ...

    @property
    def min_enter_cost(self) -> int: ...

    def is_walkable(self, position: Coord) -> bool: ...
    def enter_cost(self, position: Coord) -> int: ...
    def neighbors(self, position: Coord) -> Iterator[Coord]: ...

def load_map(path: str | pathlib.Path) -> WarehouseMap: ...

@dataclass(frozen=True)
class MultiState:
    position: Coord
    collected_mask: int
```

`is_walkable` trả `False` cho kệ và tọa độ ngoài lưới. `enter_cost` trả chi phí dương của ô đi được và ném `ValueError` cho các ô khác. `neighbors` nhận tọa độ ô đang đứng và sinh các ô kề đi được. `load_map` ném `ValueError` nếu JSON sai cú pháp, sai mã hóa hoặc sai schema. Thông báo gồm đường dẫn và dữ liệu sai. Lỗi đọc tệp giữ kiểu `OSError`. `MAPS_DIR` là đường dẫn tuyệt đối đến thư mục bản đồ mẫu cạnh module.

- **Một đích** dùng trực tiếp `Coord` làm trạng thái. Nhiệm vụ chỉ có món mang ID đã chọn. Kiểm tra đích bằng vị trí của món đó. Nếu xuất phát tại đích thì chi phí và số bước đều bằng 0.
- **Nhiều điểm** dùng khóa trạng thái là cả `(position, collected_mask)`. Hai trạng thái tại cùng vị trí với hai bitmask khác nhau được tìm kiếm độc lập. Món thứ `i` tương ứng với bit `1 << i`. Khởi tạo mask với bit của món tại `start` nếu có. Khi đi vào ô có món, OR mask cũ với bit của món đó. Đích thỏa `position == depot` và `collected_mask == (1 << len(pickups)) - 1`.
- Sinh ô kề theo thứ tự **lên, phải, xuống, trái** và chỉ sinh ô đi được. Chi phí mỗi bước bằng `enter_cost` của ô đến, kể cả khi quay về depot. Chi phí ban đầu là 0. Việc lấy hàng được gộp vào trạng thái đầu hoặc bước di chuyển.

## 3. API chung cho tìm kiếm

Trong các chữ ký dưới đây, `S` là `TypeVar` có cận `Hashable`. Hai lớp bài toán dùng chung giao thức này.

```python
class SearchProblem(Protocol[S]):
    @property
    def initial_state(self) -> S: ...

    def is_goal(self, state: S) -> bool: ...
    def successors(self, state: S) -> Iterable[tuple[S, int]]: ...
    def heuristic(self, state: S) -> int: ...
    def pickup_order(self, path: tuple[S, ...]) -> tuple[str, ...]: ...

class SingleGoalProblem:
    def __init__(self, warehouse: WarehouseMap, pickup_id: str) -> None: ...

class MultiPickupProblem:
    def __init__(self, warehouse: WarehouseMap, heuristic: Literal["max", "mst"] = "max") -> None: ...
    def state_at(self, position: Coord, collected_mask: int = 0) -> MultiState: ...
    def remaining_positions(self, state: MultiState) -> Iterator[Coord]: ...
    def h_max(self, state: MultiState) -> int: ...
    def h_mst(self, state: MultiState) -> int: ...

def search(
    problem: SearchProblem[S],
    *,
    algorithm: Literal["bfs", "ucs", "greedy", "astar"] = "astar",
    timeout_seconds: float | None = None,
    max_expanded_nodes: int | None = None,
    should_cancel: Callable[[], bool] | None = None,
    on_event: Callable[[SearchEvent[S]], None] | None = None,
    max_events: int = 1000,
) -> SearchResult[S]: ...
```

- `successors` trả các cặp (trạng thái kế tiếp, chi phí cạnh dương) theo thứ tự xác định. Lời gọi hữu hạn và không thay đổi trạng thái đầu vào. `pickup_order` chỉ được gọi với đường đi nghiệm. ID lạ trong `SingleGoalProblem` gây `ValueError`.
- BFS dùng hàng đợi FIFO, đánh dấu đã gặp khi chèn và tối ưu số bước. BFS chỉ bảo đảm chi phí tối ưu khi mọi bước có cùng chi phí. Greedy Best-First dùng ưu tiên `(h, sequence)`, đánh dấu đã gặp khi chèn và không bảo đảm nghiệm tối ưu.
- UCS dùng `h = 0`. A* và Greedy ở chế độ một đích dùng `m * d(position, goal)`, với `m = min_enter_cost` và `d` là khoảng cách Manhattan.
- UCS và A* dùng ưu tiên `(g + h, sequence)` và lưu `best_g` theo toàn bộ trạng thái. Chèn khi phát hiện `g` nhỏ hơn mức đã biết, kể cả với trạng thái từng mở rộng. Bỏ qua entry có `g` khác mức tốt nhất hiện tại. `sequence` tăng ở mỗi lần chèn để phá hòa theo thứ tự chèn. Mọi thuật toán kiểm tra đích khi lấy entry còn hiệu lực khỏi frontier và truy vết nghiệm bằng bảng trạng thái cha.
- UCS và A* nhiều điểm tìm trực tiếp trên `MultiState(position, collected_mask)`. Thứ tự lấy hàng được suy ra từ đường đi tìm được.

### Heuristic nhiều điểm và tính chấp nhận được

Mọi đường đi giữa hai tọa độ có ít nhất số bước bằng khoảng cách Manhattan và mỗi bước tốn ít nhất `m`. Vì vậy `m * d(u, v)` là cận dưới chi phí đi từ `u` đến `v`, kể cả khi có kệ hoặc chi phí vào ô thay đổi.

- **`h_max`** lấy giá trị lớn nhất của `m * d(position, pickup)` trên các điểm chưa lấy. Mỗi tuyến hợp lệ phải đến tất cả các điểm này, nên chi phí toàn tuyến ít nhất bằng cận dưới lớn nhất đó. Khi đã lấy đủ, dùng `m * d(position, depot)` vì robot còn phải về depot.
- **`h_mst`** dùng Prim trên đồ thị đầy đủ gồm vị trí robot, các điểm chưa lấy và depot. Mỗi tọa độ xuất hiện một lần, cạnh có trọng số `m * d(u, v)`. Với bất kỳ tuyến hợp lệ nào, ghi lại tọa độ cần thiết theo thứ tự đi qua, gồm tọa độ bắt đầu và depot cuối. Các cặp liên tiếp tạo đồ thị liên thông chứa mọi tọa độ cần thiết, với tổng trọng số không vượt chi phí tuyến thật. Đồ thị liên thông đó chứa một cây khung, nên chi phí cây khung nhỏ nhất cũng không vượt chi phí tuyến thật.

Cả hai heuristic đều bằng 0 tại trạng thái đã lấy đủ hàng và đang ở depot. Kiểm thử đối chiếu với chi phí UCS từ các trạng thái có thể đến trên một bản đồ nhỏ.

### Baseline nearest-neighbor

`nearest_neighbor(warehouse, *, timeout_seconds=None, max_expanded_nodes=None, should_cancel=None, on_event=None, max_events=1000)` trong `planning.py` trả `SearchResult[MultiState]`. Mỗi chặng chạy một UCS trên tọa độ với toàn bộ điểm chưa lấy là tập đích. Điểm đầu tiên lấy ra khỏi frontier có chi phí đường đi ngắn nhất thực tế. Khi cùng chi phí, UCS ưu tiên entry được chèn trước theo thứ tự sinh hàng xóm lên, phải, xuống, trái. Sau mỗi chặng, cập nhật bitmask trên từng ô đi qua và nối đường đi, bỏ ô nối bị lặp. Chặng cuối dùng UCS với depot là đích duy nhất.

Trên `nearest_neighbor_trap.json`, CLI đo được nearest-neighbor lấy theo thứ tự C → A → B với chi phí **8**. UCS và A* với cả hai heuristic tìm được tuyến C → B → A với chi phí **6**.

## 4. Kết quả tìm kiếm

```python
SearchStatus = Literal["success", "no_path", "timeout", "node_limit", "cancelled"]

@dataclass(frozen=True)
class SearchResult(Generic[S]):
    status: SearchStatus
    path: tuple[S, ...]
    total_cost: int | None
    steps: int | None
    expanded_nodes: int
    generated_nodes: int
    peak_frontier_entries: int
    elapsed_seconds: float
    pickup_order: tuple[str, ...]
```

- `success` trả các trạng thái từ đầu đến đích, gồm cả hai đầu. `steps = len(path) - 1`, `total_cost` là tổng chi phí vào các ô sau ô đầu. Trong bài toán nhiều điểm, giữ nguyên cả vị trí và bitmask trong `path`.
- `pickup_order` lấy từ đường đi nghiệm. Một đích trả tuple chứa ID đã chọn. Nhiều điểm đọc bit tại trạng thái đầu, rồi các bit mới được bật ở từng bước theo thứ tự đường đi. Mỗi ID xuất hiện một lần.
- Bốn trạng thái kết thúc còn lại trả `path=()`, `total_cost=None`, `steps=None` và `pickup_order=()`. Các chỉ số vẫn ghi số liệu đến thời điểm dừng.

## 5. Điều kiện dừng

| Status | Điều kiện |
| --- | --- |
| `success` | Lấy được trạng thái đích với entry còn hiệu lực. |
| `no_path` | Frontier đã hết sau khi bỏ các entry cũ, và chưa tìm được đích. |
| `timeout` | Thời gian đã chạm hoặc vượt `timeout_seconds` tại điểm kiểm tra. |
| `node_limit` | Nút hợp lệ kế tiếp chưa phải đích và muốn mở rộng nó sẽ vượt `max_expanded_nodes`. |
| `cancelled` | `should_cancel()` trả `True` tại điểm kiểm tra. |

`None` bỏ giới hạn tương ứng. `timeout_seconds` nhận `int` hoặc `float` hữu hạn không âm. `max_expanded_nodes` nhận số nguyên không âm. Boolean, giá trị ngoài miền và tên thuật toán lạ gây `ValueError`.

Kiểm tra hủy trước, rồi thời gian, trước khi chèn gốc và ở đầu mỗi vòng lặp trước khi kiểm tra frontier hoặc lấy entry kế tiếp. Sau khi lấy entry hợp lệ, kiểm tra đích trước giới hạn mở rộng. Nhờ vậy giới hạn 0 vẫn cho phép nghiệm tại vị trí xuất phát. Một lần mở rộng xử lý hết successor rồi mới trở lại điểm kiểm tra. Sau khi xác nhận đích, tái dựng đường đi và trả nghiệm.

## 6. Tổ chức module và CLI

| Module | Trách nhiệm |
| --- | --- |
| `bonus/warehouse/environment.py` | `Coord`, `Pickup`, `WarehouseMap`, `load_map`, `MultiState`, hai lớp bài toán, heuristic và thứ tự lấy hàng. Các lớp bài toán đáp ứng giao thức tìm kiếm qua chữ ký phương thức. |
| `bonus/warehouse/search.py` | Giao thức, kết quả, sự kiện và tìm kiếm BFS, UCS, Greedy Best-First, A*. |
| `bonus/warehouse/planning.py` | Baseline nearest-neighbor và ngân sách dùng chung qua các chặng UCS. |
| `bonus/warehouse/cli.py` | CLI một đích và nhiều điểm, dùng `argparse`. |
| `bonus/warehouse/maps/` và `tests/test_warehouse*.py` | Bản đồ mẫu và kiểm thử môi trường, tìm kiếm và CLI. |
| `bonus/warehouse/gui.py` | Giao diện Pygame và phát lại tìm kiếm. |
| `bonus/warehouse/benchmark.py` và `plotting.py` | Chạy benchmark, tạo bảng và biểu đồ trong `bonus/warehouse/results/`. |

CLI chạy từ gốc repo với `--map PATH`. `--mode single` hỗ trợ `bfs`, `ucs`, `greedy` và `astar`. `--pickup ID` chọn điểm lấy hàng, mặc định là điểm đầu tiên trong bản đồ. `--mode multi` hỗ trợ `ucs`, `astar` và `nearest_neighbor`. `--heuristic {max,mst}` chọn heuristic cho A* nhiều điểm, mặc định là `max`. Mặc định CLI chạy A* ở chế độ một đích. `--timeout SECONDS` và `--max-expanded-nodes N` giới hạn tài nguyên. Ctrl+C trong lúc tìm kiếm yêu cầu hủy.

```text
python -m bonus.warehouse.cli --help
python -m bonus.warehouse.cli --map bonus/warehouse/maps/weighted.json --algorithm astar --mode single
python -m bonus.warehouse.cli --map bonus/warehouse/maps/weighted.json --algorithm ucs --mode single --pickup A --json
python -m bonus.warehouse.cli --map bonus/warehouse/maps/nearest_neighbor_trap.json --mode multi --algorithm astar --heuristic mst --json
python -m bonus.warehouse.cli --map bonus/warehouse/maps/nearest_neighbor_trap.json --mode multi --algorithm nearest_neighbor --json
```

Có thể nạp các bản đồ mẫu ngay từ gốc repo với `load_map("bonus/warehouse/maps/weighted.json")` hoặc `load_map(MAPS_DIR / "weighted.json")`. Sáu bản đồ là `small_uniform.json`, `detour.json`, `weighted.json`, `multi_pickup.json`, `no_path.json` và `nearest_neighbor_trap.json`. Trong `weighted.json`, đường thẳng dài 3 bước và tốn 19, còn đường vòng qua hàng dưới dài 5 bước và tốn 5.

Mặc định CLI in tóm tắt cho người đọc. `--json` in một đối tượng theo các trường của `SearchResult`. Trong `path`, một đích dùng mảng `[hàng, cột]`, nhiều điểm dùng đối tượng có `position` và `collected_mask`. Đầu ra CLI dùng UTF-8. CLI trả mã 0 khi thành công, 1 cho kết quả tìm kiếm còn lại và 2 cho lỗi đầu vào, với lỗi đầu vào ghi vào stderr.

## 7. Đo số nút và thời gian

- `expanded_nodes` tăng một lần khi bắt đầu gọi `successors` cho entry hợp lệ ngoài đích, kể cả khi lời gọi không sinh successor nào. Lần mở rộng lại được đếm riêng. Entry cũ và trạng thái đích không tính.
- `generated_nodes` tăng một lần cho mỗi successor hợp lệ mà bài toán trả về, trước khi lọc theo chi phí. Đếm cả trạng thái lặp và successor dẫn tới đích. Root không phải successor.
- `peak_frontier_entries` là giá trị lớn nhất của số entry thực tế trong frontier sau mỗi lần chèn, gồm root và các entry cũ còn nằm trong heap. Đơn vị là entry, có thể có nhiều entry cho cùng một trạng thái. Mức sử dụng RAM cần một phép đo riêng.
- `elapsed_seconds` dùng `time.perf_counter()`, bắt đầu sau khi kiểm tra tham số, trước điểm kiểm tra hủy đầu tiên. Kết thúc sau khi tái dựng nghiệm và thứ tự lấy hàng nếu có, ngay trước sự kiện cuối. Khoảng đo bao gồm callback trong lúc tìm kiếm. Tải bản đồ, tạo bài toán, callback cuối và xuất kết quả nằm ngoài khoảng đo. Timeout dùng cùng mốc bắt đầu.
- Khi so sánh thuật toán, dùng cùng bản đồ, nhiệm vụ, giới hạn, thứ tự successor và quy tắc phá hòa. Benchmark phải để `on_event=None` và đo các lần chạy độc lập.
- Với nearest-neighbor, cộng `expanded_nodes` và `generated_nodes` của tất cả lượt UCS đã chạy, kể cả chặng dừng giữa chừng. Dùng mức cao nhất của `peak_frontier_entries` trong các chặng vì các frontier hoạt động lần lượt. Nếu đã ở đích ngay từ đầu, cả ba thống kê đều bằng 0 vì không cần chạy UCS con.
- Nearest-neighbor đo thời gian theo một đồng hồ cho toàn bộ lần lập kế hoạch, gồm khởi tạo bài toán, các lượt UCS, cập nhật bitmask và ghép đường. Mỗi chặng chỉ được mở rộng tối đa phần ngân sách nút còn lại. Hủy và timeout được kiểm tra giữa các chặng và ở các điểm kiểm tra của UCS con theo đồng hồ chung. Kết quả giữ trạng thái dừng tương ứng và thống kê đã cộng dồn.

## 8. Hủy tìm kiếm và sự kiện cho GUI

`should_cancel` là hàm đồng bộ tùy chọn, có thể truyền `threading.Event.is_set`. Luồng Pygame đặt cờ khi người dùng hủy hoặc đổi nhiệm vụ. Tìm kiếm trả `cancelled` ở điểm kiểm tra tiếp theo. `on_event` nhận dữ liệu bất biến đồng bộ trên luồng gọi `search`. Lỗi do callback phát sinh truyền về caller.

```python
@dataclass(frozen=True)
class SearchEvent(Generic[S]):
    kind: Literal["frontier_push", "expand", "finish"]
    state: S | None
    g: int | None
    h: int | None
    frontier_entries: int
    expanded_nodes: int
    generated_nodes: int
    result: SearchResult[S] | None
```

- `frontier_push` phát ngay sau mỗi lần chèn, gồm cả root. `expand` phát sau khi tăng bộ đếm mở rộng và trước khi sinh successor. Hai sự kiện mang trạng thái và điểm `g, h`, với `result=None`.
- `max_events` giới hạn tổng số sự kiện `frontier_push` và `expand` được gửi trong một lượt. Giá trị mặc định là 1000, giá trị 0 chỉ gửi `finish`. Hết hạn mức sự kiện thì tìm kiếm tiếp tục. Giá trị phải là số nguyên không âm và từ chối boolean.
- `finish` phát đúng một lần cho mọi kết quả trả về nếu có callback. Sự kiện chứa `result`, với `state, g, h` đều là `None`. Các trường đếm mô tả thời điểm phát sự kiện. Khi `on_event=None`, bỏ qua việc tạo đối tượng sự kiện.
- Nearest-neighbor chuyển tiếp sự kiện trung gian của UCS với số nút và chi phí cộng dồn. Tọa độ được gắn bitmask của hàng đã lấy trên các chặng trước và hàng tại ô đang xét. `frontier_entries` là kích thước frontier của chặng đang chạy. `max_events` dùng chung cho toàn tuyến và chỉ có một sự kiện `finish` cho kết quả cuối.
- GUI chỉ gọi Pygame trên luồng chính. Luồng nền lưu các tọa độ mở rộng trong phạm vi hạn mức, rồi gửi một gói kết quả hoặc lỗi qua hàng đợi có ID tác vụ. Reset, thay lựa chọn tìm kiếm hoặc đóng cửa sổ đặt cờ hủy và tăng ID. Luồng chính bỏ gói có ID cũ.
- GUI bắt đầu phát lại sau khi tìm kiếm kết thúc. Pause, Resume và tốc độ chỉ ảnh hưởng phát lại. Panel dùng thời gian trả về từ bộ tìm kiếm, đã bao gồm chi phí ghi callback nhưng nằm trước khi vẽ hoạt họa. Nếu thiếu sự kiện mở rộng, panel hiển thị số đã ghi trên tổng số lần mở rộng và dùng toàn bộ `SearchResult.path` để phát lại robot.

## 9. Benchmark và tổng hợp

| Profile | Lưới một đích | Mật độ cản danh nghĩa | Lưới nhiều điểm | Mật độ cản danh nghĩa | Seed | Giới hạn mỗi lần | Số lần chạy |
|---|---|---|---|---|---|---|---:|
| Quick | 8, 14 ô/cạnh | 10%, 30% | 7, 10 ô/cạnh | 10%, 30% | 11, 29 | 0,5 giây và 12.000 lần mở rộng | 152 |
| Full | 12, 24, 40, 64 ô/cạnh | 10%, 25%, 40% | 8, 12, 16 ô/cạnh | 10%, 30% | 11, 29, 47, 71, 101, 137 | 2 giây và 50.000 lần mở rộng | 936 |

- Một đích chạy BFS, UCS, Greedy và A* trên chi phí đồng nhất. Trên chi phí có trọng số, chạy UCS, Greedy và A*. Hai biến thể chi phí dùng cùng bố trí vật cản với cùng kích thước, mật độ và seed.
- Nhiều điểm chạy UCS, A* max, A* MST và nearest-neighbor trên bản đồ có trọng số. Các nhiệm vụ 1, 3 và 5 điểm dùng các tiền tố của cùng danh sách hàng trên bản đồ. Ô đầu, depot và điểm lấy hàng luôn đi được. Mật độ cản thực có thể chênh giá trị danh nghĩa và được ghi trong nhiệm vụ dưới dạng số ô cản. Không chọn lại bản đồ khi đích bị cô lập.
- Chạy tuần tự, xoay thứ tự thuật toán giữa các nhiệm vụ và tắt callback sự kiện. Mỗi lần đo nạp một đối tượng bản đồ mới để cache của thuật toán trước không ảnh hưởng lượt sau. Đồng hồ bắt đầu sau khi đọc và kiểm tra JSON, trước khi chọn tập điểm và khởi tạo bài toán. Thời gian dùng trong báo cáo bao gồm khởi tạo, tính heuristic, các chặng và dựng kết quả. `solver_elapsed_seconds` lưu riêng thời gian do API trả về. Deadline dùng chung cho tiền xử lý và tìm kiếm, kiểm tra tại các điểm dừng của thuật toán. Nút mở rộng dùng cùng một hạn mức cho toàn lần chạy.
- Mỗi thư mục chạy chứa `manifest.json`, `tasks.json`, `maps/` và một bản ghi JSON cho mỗi cặp nhiệm vụ–thuật toán trong `raw/`. Mã cấu hình băm thông số, bản đồ, nhiệm vụ, mã nguồn benchmark và bộ giải, cùng metadata môi trường. Bản ghi lưu mã này và danh tính nhiệm vụ. Khi tiếp tục, kiểm tra bản ghi hiện có trước khi đo phần còn thiếu. Khóa ghi ngăn hai tiến trình ghi cùng cấu hình. Tệp được thay thế nguyên tử để một lần ghi gián đoạn không thành bản ghi hoàn chỉnh.
- Thống kê trạng thái giữ riêng `no_path`, `timeout`, `node_limit`, `cancelled` và số lần còn thiếu. Tỷ lệ thành công dùng mẫu có bản ghi làm mẫu số. Bảng báo trung vị chi phí, nút và thời gian trên tập nhiệm vụ mà tất cả biến thể trong nhóm đều tìm được nghiệm. Biểu đồ theo kích thước và số điểm gộp các mật độ tương ứng rồi dùng tập thành công chung tại mỗi điểm. Các lượt timeout xuất hiện trong bảng trạng thái và nằm ngoài trung vị. Cỡ mẫu chung có thể thay đổi theo cấu hình hoặc kích thước.
- Tỷ số chi phí dùng cặp kết quả thành công cùng nhiệm vụ có UCS với chi phí dương. Khi UCS vắng mặt, thất bại hoặc trả chi phí 0, tỷ số bỏ trống. Bảng và biểu đồ ghi cả số cặp hợp lệ và nhóm thiếu mẫu. Mỗi lần vẽ chỉ đọc một mã cấu hình, và đầu ra quick được gắn nhãn kiểm tra pipeline.
