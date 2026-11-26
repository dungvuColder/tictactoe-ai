"""Giao diện Pygame cho robot kho. Tìm đường chạy trong luồng nền."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from queue import Empty, SimpleQueue
from threading import Event, Thread

import pygame as pg

from .environment import MAPS_DIR, Coord, MultiPickupProblem, MultiState, SingleGoalProblem, WarehouseMap, load_map
from .planning import nearest_neighbor
from .search import ALGORITHMS, SearchEvent, SearchResult, search

SIZE = (1160, 770)
REPLAY_LIMIT = 1000
SAMPLE_NAMES = {
    "small_uniform": "Kho nhỏ",
    "detour": "Lối đi vòng",
    "weighted": "Chi phí khác nhau",
    "multi_pickup": "Nhiều điểm lấy hàng",
    "no_path": "Đích bị cô lập",
    "nearest_neighbor_trap": "So sánh nearest-neighbor",
}
MODE_ALGORITHMS = {"single": ALGORITHMS, "multi": ("ucs", "astar", "nearest_neighbor")}
ALGORITHM_NAMES = {
    "bfs": "BFS", "ucs": "UCS", "greedy": "Greedy Best-First",
    "astar": "A*", "nearest_neighbor": "Nearest-neighbor",
}
STATUSES = {
    "success": "Đã tìm thấy đường", "no_path": "Không có đường đi",
    "timeout": "Hết thời gian", "node_limit": "Đạt giới hạn nút", "cancelled": "Đã hủy",
}
SPEEDS = (0.5, 1, 2, 4, 8)

BACKGROUND = "#edf1f5"
PANEL = "#ffffff"
INK = "#172738"
MUTED = "#485e73"
BORDER = "#d4dfe7"
WALK = "#f2f6f7"
RACK = "#34485a"
DEPOT = "#7358a9"
GOODS = "#f2bc52"
INACTIVE_GOODS = "#b0c0cb"
EXPANDED = "#b5d7fa"
PATH = "#00816f"
ERROR = "#942c3b"

Result = SearchResult[Coord] | SearchResult[MultiState]


@dataclass(frozen=True)
class Outcome:
    task_id: int
    result: Result | None = None
    expanded: tuple[Coord, ...] = ()
    error: str | None = None


def _solve(
    task_id: int,
    warehouse: WarehouseMap,
    mode: str,
    algorithm: str,
    heuristic: str,
    pickup_id: str,
    cancelled: Event,
    mailbox: SimpleQueue[Outcome],
    replay_limit: int,
) -> None:
    expanded: list[Coord] = []

    def capture(event: SearchEvent) -> None:
        if event.kind == "expand":
            state = event.state
            if state is not None:
                expanded.append(state.position if isinstance(state, MultiState) else state)

    try:
        options = dict(should_cancel=cancelled.is_set, on_event=capture, max_events=replay_limit)
        if algorithm == "nearest_neighbor":
            result = nearest_neighbor(warehouse, **options)
        elif mode == "multi":
            result = search(MultiPickupProblem(warehouse, heuristic), algorithm=algorithm, **options)
        else:
            result = search(SingleGoalProblem(warehouse, pickup_id), algorithm=algorithm, **options)
        outcome = Outcome(task_id, result, tuple(expanded))
    except Exception as exc:
        outcome = Outcome(task_id, error=f"{type(exc).__name__}: {exc}")
    mailbox.put(outcome)


class WarehouseApp:
    def __init__(self, args):
        self.samples = tuple(name for name in SAMPLE_NAMES if (MAPS_DIR / f"{name}.json").is_file())
        self.map_name = args.map
        self.warehouse = load_map(MAPS_DIR / f"{self.map_name}.json")
        self.mode = args.mode
        self.algorithm = args.algorithm
        self.heuristic = args.heuristic
        self.pickup_id = args.pickup if args.pickup is not None else self.warehouse.pickups[0].id
        if self.mode == "single":
            SingleGoalProblem(self.warehouse, self.pickup_id)
        self.replay_limit = args.replay_limit
        self.speed_index = 1
        self.task_id = 0
        self.cancel_flag: Event | None = None
        self.mailbox: SimpleQueue[Outcome] = SimpleQueue()
        self.reset()

        self.screen = pg.display.set_mode(SIZE)
        pg.display.set_caption("Robot kho")
        self.clock = pg.time.Clock()
        self.fonts = {
            "title": pg.font.SysFont("segoeui,dejavusans", 32, bold=True),
            "heading": pg.font.SysFont("segoeui,dejavusans", 21, bold=True),
            "body": pg.font.SysFont("segoeui,dejavusans", 17),
            "small": pg.font.SysFont("segoeui,dejavusans", 15),
        }
        self.hitboxes = []

    def cancel_task(self) -> None:
        self.task_id += 1
        if self.cancel_flag is not None:
            self.cancel_flag.set()
            self.cancel_flag = None

    def reset(self) -> None:
        self.cancel_task()
        self.result: Result | None = None
        self.error: str | None = None
        self.expansions: tuple[Coord, ...] = ()
        self.expansion_index = 0
        self.expanded_tiles: set[Coord] = set()
        self.path_index = 0
        self.paused = False
        self.playback_time = 0.0

    def change_map(self, name: str) -> None:
        self.reset()
        try:
            warehouse = load_map(MAPS_DIR / f"{name}.json")
        except (OSError, ValueError) as exc:
            self.error = str(exc)
            return
        self.map_name = name
        self.warehouse = warehouse
        self.pickup_id = warehouse.pickups[0].id

    def change_option(self, attr, values, direction) -> None:
        if attr == "pickup_id":
            if self.mode != "single":
                return
            values = tuple(pickup.id for pickup in self.warehouse.pickups)
        elif attr == "algorithm":
            values = MODE_ALGORITHMS[self.mode]
        elif attr == "heuristic" and (self.mode != "multi" or self.algorithm != "astar"):
            return
        value = values[(values.index(getattr(self, attr)) + direction) % len(values)]
        if attr == "speed_index":
            self.speed_index = value
        elif attr == "map_name":
            self.change_map(value)
        else:
            self.reset()
            setattr(self, attr, value)
            if attr == "mode" and self.algorithm not in MODE_ALGORITHMS[value]:
                self.algorithm = "astar"

    def start_search(self) -> None:
        self.reset()
        cancelled = self.cancel_flag = Event()
        worker = Thread(
            target=_solve,
            args=(self.task_id, self.warehouse, self.mode, self.algorithm, self.heuristic,
                  self.pickup_id, cancelled, self.mailbox, self.replay_limit),
            daemon=True,
        )
        try:
            worker.start()
        except RuntimeError as exc:
            self.cancel_task()
            self.error = str(exc)

    def poll(self) -> None:
        while True:
            try:
                outcome = self.mailbox.get_nowait()
            except Empty:
                return
            if outcome.task_id != self.task_id:
                continue
            self.cancel_flag = None
            self.result = outcome.result
            self.error = outcome.error
            self.expansions = outcome.expanded

    @property
    def replaying(self) -> bool:
        return bool(self.result and (
            self.expansion_index < len(self.expansions) or self.path_index + 1 < len(self.result.path)
        ))

    def toggle_pause(self) -> None:
        if self.replaying:
            self.paused = not self.paused

    def advance(self, seconds: float) -> None:
        if self.paused or not self.replaying:
            return
        self.playback_time += seconds * SPEEDS[self.speed_index]
        if self.expansion_index < len(self.expansions):
            interval = min(1 / 25, 1.8 / len(self.expansions))
            count = int(self.playback_time / interval)
            end = min(self.expansion_index + count, len(self.expansions))
            if end == self.expansion_index:
                return
            self.expanded_tiles.update(self.expansions[self.expansion_index:end])
            self.playback_time -= (end - self.expansion_index) * interval
            self.expansion_index = end
            if end < len(self.expansions):
                return
        count = int(self.playback_time / 0.22)
        self.path_index = min(self.path_index + count, max(0, len(self.result.path) - 1))
        self.playback_time -= count * 0.22

    def _text(self, text, x, y, font="body", color=INK, width=None):
        face = self.fonts[font]
        if width is not None and face.size(text)[0] > width:
            while text and face.size(text + "…")[0] > width:
                text = text[:-1]
            text += "…"
        self.screen.blit(face.render(text, True, color), (x, y))

    def _button(self, box, label, action, *, primary=False, enabled=True):
        color = PATH if primary else WALK
        pg.draw.rect(self.screen, color, box, border_radius=8)
        if not primary:
            pg.draw.rect(self.screen, BORDER, box, 1, border_radius=8)
        foreground = PANEL if primary else INK if enabled else MUTED
        image = self.fonts["small"].render(label, True, foreground)
        self.screen.blit(image, image.get_rect(center=box.center))
        if enabled:
            self.hitboxes.append((box, action))

    def _choice(self, y, label, value, attr, choices):
        self._text(label, 804, y + 8, "small", MUTED)
        box = pg.Rect(906, y, 204, 34)
        pg.draw.rect(self.screen, WALK, box, border_radius=8)
        pg.draw.rect(self.screen, BORDER, box, 1, border_radius=8)
        self._text(value, box.x + 34, y + 6, "small", width=box.width - 68)
        for direction, x, arrow in ((-1, box.x, "‹"), (1, box.right - 31, "›")):
            self._button(
                pg.Rect(x, y, 31, 34), arrow,
                lambda step=direction: self.change_option(attr, choices, step),
                enabled=len(choices) > 1,
            )

    def _draw_board(self):
        warehouse = self.warehouse
        board = pg.Rect(47, 166, 682, 464)
        cell = min(122, board.width // warehouse.cols, board.height // warehouse.rows)
        left = board.centerx - warehouse.cols * cell // 2
        top = board.centery - warehouse.rows * cell // 2

        def rect(position):
            row, col = position
            return pg.Rect(left + col * cell, top + row * cell, cell, cell)

        for row, costs in enumerate(warehouse.grid):
            for col, cost in enumerate(costs):
                position = (row, col)
                tile = rect(position)
                fill = RACK if cost == 0 else EXPANDED if position in self.expanded_tiles else WALK
                pg.draw.rect(self.screen, fill, tile.inflate(-3, -3), border_radius=7)
                if cost == 0:
                    pg.draw.line(self.screen, MUTED, (tile.x + 13, tile.centery),
                                 (tile.right - 13, tile.centery), 2)
                else:
                    self._text(str(cost), tile.x + 9, tile.y + 5, "small", MUTED, width=cell - 15)

        path = self.result.path if self.result else ()
        route = [state.position if isinstance(state, MultiState) else state for state in path]
        centers = [rect(position).center for position in route]
        if len(centers) > 1:
            pg.draw.lines(self.screen, PATH, False, centers, 5)
        active = path[self.path_index] if path else warehouse.start
        position = active.position if isinstance(active, MultiState) else active
        depot = rect(warehouse.depot)
        depot_mark = pg.Rect(depot.x + 8, depot.bottom - 29, 24, 22)
        pg.draw.rect(self.screen, DEPOT, depot_mark, border_radius=5)
        self._text("D", depot_mark.x + 6, depot_mark.y + 1, "small", PANEL)
        for index, pickup in enumerate(warehouse.pickups):
            tile = rect(pickup.position)
            selected = self.mode == "multi" or pickup.id == self.pickup_id
            collected = selected and (
                bool(active.collected_mask & (1 << index)) if isinstance(active, MultiState)
                else pickup.position == position
            )
            mark = pg.Rect(tile.right - 48, tile.bottom - 30, 40, 23)
            fill = PATH if collected else GOODS if selected else INACTIVE_GOODS
            pg.draw.rect(self.screen, fill, mark, border_radius=6)
            if collected:
                pg.draw.lines(self.screen, PANEL, False, (
                    (mark.x + 5, mark.y + 11), (mark.x + 8, mark.y + 14), (mark.x + 14, mark.y + 8)
                ), 2)
            self._text(pickup.id, mark.x + (19 if collected else 7), mark.y + 2,
                       "small", PANEL if collected else INK, width=17 if collected else 26)
        center = rect(position).center
        pg.draw.circle(self.screen, PANEL, center, 19)
        pg.draw.circle(self.screen, INK, center, 16)
        self._text("R", center[0] - 5, center[1] - 11, "body", PANEL)

        legend = ((RACK, "Kệ"), (WALK, "Lối đi / chi phí"), (DEPOT, "Depot"),
                  (GOODS, "Hàng"), (INACTIVE_GOODS, "Hàng khác"), (INK, "Robot"),
                  (EXPANDED, "Đã mở rộng"), (PATH, "Đường đi / Đã lấy"))
        x = 49
        for color, label in legend:
            swatch = pg.Rect(x, 676, 13, 13)
            pg.draw.rect(self.screen, color, swatch, border_radius=3)
            pg.draw.rect(self.screen, BORDER, swatch, 1, border_radius=3)
            self._text(label, x + 19, 671, "small", MUTED)
            x += self.fonts["small"].size(label)[0] + 27

    def _draw_controls(self):
        self._choice(146, "Bản đồ", SAMPLE_NAMES[self.map_name], "map_name", self.samples)
        self._choice(187, "Chế độ", "Một đích" if self.mode == "single" else "Nhiều điểm",
                     "mode", ("single", "multi"))
        self._choice(228, "Thuật toán", ALGORITHM_NAMES[self.algorithm], "algorithm", MODE_ALGORITHMS[self.mode])
        if self.mode == "single":
            self._choice(269, "Điểm lấy", self.pickup_id, "pickup_id",
                         tuple(pickup.id for pickup in self.warehouse.pickups))
        elif self.algorithm == "astar":
            self._choice(269, "Heuristic", self.heuristic.upper(), "heuristic", ("max", "mst"))

        self._button(pg.Rect(804, 317, 92, 36), "Run", self.start_search, primary=True)
        self._button(pg.Rect(903, 317, 100, 36), "Resume" if self.paused else "Pause",
                     self.toggle_pause, enabled=self.replaying)
        self._button(pg.Rect(1010, 317, 100, 36), "Reset", self.reset)
        self._text("Pause chỉ dừng phát lại sau khi tìm xong.", 804, 359, "small", MUTED)
        self._choice(389, "Tốc độ", f"{SPEEDS[self.speed_index]:g}×", "speed_index", tuple(range(len(SPEEDS))))

        pg.draw.line(self.screen, BORDER, (804, 438), (1110, 438))
        self._text("Kết quả", 804, 449, "heading")
        status = "Sẵn sàng"
        if self.cancel_flag is not None:
            status = "Đang tìm đường…"
        elif self.error:
            status = "Lỗi tác vụ"
        elif self.result is not None:
            status = STATUSES[self.result.status]
        self._text(status, 804, 482, "body", ERROR if self.error else PATH)
        if self.error:
            self._text(self.error, 804, 511, "small", ERROR, width=301)
        if self.result is None:
            return
        result = self.result
        cost = result.total_cost if result.total_cost is not None else "—"
        steps = result.steps if result.steps is not None else "—"
        self._text(f"Chi phí  {cost}", 804, 515)
        self._text(f"Số bước  {steps}", 970, 515)
        self._text(f"Mở rộng  {result.expanded_nodes}", 804, 543)
        self._text(f"Nút sinh  {result.generated_nodes}", 970, 543)
        self._text(f"Frontier lớn nhất  {result.peak_frontier_entries}", 804, 571, "small")
        self._text(f"Tìm kiếm  {result.elapsed_seconds * 1000:.2f} ms", 804, 597, "small")
        if len(self.expansions) < result.expanded_nodes:
            self._text(f"Phát lại {len(self.expansions)}/{result.expanded_nodes} lần mở rộng",
                       804, 623, "small", ERROR)
        if result.pickup_order:
            self._text("Thứ tự  " + " → ".join(result.pickup_order), 804, 652, "small", width=304)

    def draw(self) -> None:
        self.hitboxes.clear()
        self.screen.fill(BACKGROUND)
        self._text("Robot kho", 28, 21, "title")
        self._text("Lập kế hoạch lấy hàng", 30, 61, "body", MUTED)
        pg.draw.rect(self.screen, PANEL, pg.Rect(24, 102, 730, 620), border_radius=14)
        pg.draw.rect(self.screen, PANEL, pg.Rect(778, 102, 358, 620), border_radius=14)
        self._text(SAMPLE_NAMES[self.map_name], 48, 122, "heading")
        self._text(f"{self.warehouse.rows} × {self.warehouse.cols} ô", 644, 126, "small", MUTED)
        self._text("Thiết lập", 804, 114, "heading")
        self._draw_board()
        self._draw_controls()
        self._text("Enter  Run      Space  Pause/Resume      R  Reset      Esc  Thoát", 29, 736, "small", MUTED)
        pg.display.flip()

    def handle_event(self, event) -> bool:
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            return False
        if event.type == pg.KEYDOWN:
            action = {pg.K_RETURN: self.start_search, pg.K_SPACE: self.toggle_pause, pg.K_r: self.reset}
            if event.key in action:
                action[event.key]()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for box, action in self.hitboxes:
                if box.collidepoint(event.pos):
                    action()
                    break
        return True

    def run(self, frames: int | None = None) -> None:
        try:
            rendered = 0
            self.draw()
            while frames is None or rendered < frames:
                seconds = self.clock.tick(60) / 1000
                for event in pg.event.get():
                    if not self.handle_event(event):
                        return
                self.poll()
                self.advance(seconds)
                self.draw()
                rendered += 1
        finally:
            self.cancel_task()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Giao diện robot kho. Pause chỉ dừng hoạt họa sau khi tìm kiếm hoàn tất."
    )
    parser.add_argument("--map", choices=SAMPLE_NAMES, default="small_uniform", help="Tên bản đồ mẫu")
    parser.add_argument("--mode", choices=MODE_ALGORITHMS, default="single")
    parser.add_argument("--algorithm", choices=ALGORITHM_NAMES, default="astar")
    parser.add_argument("--heuristic", choices=("max", "mst"), default="max")
    parser.add_argument("--pickup", help="ID điểm lấy hàng ở chế độ một đích")
    parser.add_argument("--replay-limit", type=int, default=REPLAY_LIMIT, help="Giới hạn sự kiện phát lại")
    parser.add_argument("--frames", type=int, help="Số khung hình trước khi thoát")
    parser.add_argument("--autostart", action="store_true", help="Tìm đường khi vừa mở cửa sổ")
    args = parser.parse_args(argv)
    if args.algorithm not in MODE_ALGORITHMS[args.mode]:
        parser.error("Thuật toán không được hỗ trợ trong chế độ đã chọn")
    if args.replay_limit < 0 or (args.frames is not None and args.frames < 1):
        parser.error("--replay-limit phải không âm và --frames phải dương")
    pg.display.init()
    pg.font.init()
    try:
        app = WarehouseApp(args)
        if args.autostart:
            app.start_search()
        app.run(args.frames)
    finally:
        pg.quit()
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
