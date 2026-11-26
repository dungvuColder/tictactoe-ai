import importlib.util
import os
import subprocess
import sys
import unittest
from threading import Event
from types import SimpleNamespace
from unittest.mock import patch

HAS_PYGAME = importlib.util.find_spec("pygame") is not None
if HAS_PYGAME:
    from bonus.warehouse import gui


@unittest.skipUnless(HAS_PYGAME, "Pygame chưa được cài")
class WarehouseGuiTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict("os.environ", {"SDL_VIDEODRIVER": "dummy"})
        env.start()
        self.addCleanup(env.stop)
        gui.pg.display.init()
        gui.pg.font.init()
        self.addCleanup(gui.pg.quit)

    def app(self, **options):
        args = dict(map="small_uniform", mode="single", algorithm="astar", heuristic="max",
                    pickup=None, replay_limit=1000)
        args.update(options)
        app = gui.WarehouseApp(SimpleNamespace(**args))
        self.addCleanup(app.cancel_task)
        return app

    def receive(self, app):
        outcome = app.mailbox.get(timeout=3)
        app.mailbox.put(outcome)
        app.poll()
        return outcome

    def test_help_uses_utf8_with_legacy_stdout(self):
        completed = subprocess.run(
            [sys.executable, "-m", "bonus.warehouse.gui", "--help"],
            env={**os.environ, "PYTHONIOENCODING": "cp1252"},
            capture_output=True,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertIn("Giao diện robot kho", completed.stdout.decode("utf-8"))

    def test_single_multi_and_no_path_render_and_play_back(self):
        cases = [
            ("small_uniform", "single", "astar", "success", 3),
            ("multi_pickup", "multi", "astar", "success", 17),
            ("nearest_neighbor_trap", "multi", "nearest_neighbor", "success", 8),
            ("no_path", "single", "astar", "no_path", None),
        ]
        for name, mode, algorithm, status, cost in cases:
            with self.subTest(map=name, mode=mode, algorithm=algorithm):
                app = self.app(map=name, mode=mode, algorithm=algorithm, heuristic="mst")
                app.draw()
                app.handle_event(gui.pg.event.Event(gui.pg.MOUSEBUTTONDOWN, button=1, pos=(852, 332)))
                self.receive(app)
                result = app.result
                self.assertEqual((result.status, result.total_cost), (status, cost))
                self.assertEqual(len(app.expansions), result.expanded_nodes)
                app.draw()
                app.toggle_pause()
                app.advance(30)
                self.assertEqual((app.expansion_index, app.path_index), (0, 0))
                app.handle_event(gui.pg.event.Event(gui.pg.MOUSEBUTTONDOWN, button=1, pos=(1094, 402)))
                self.assertEqual(app.speed_index, 2)
                self.assertTrue(app.paused)
                app.toggle_pause()
                app.advance(30)
                self.assertEqual(app.expanded_tiles, set(app.expansions))
                self.assertEqual(app.path_index, max(0, len(result.path) - 1))
                self.assertIs(app.result, result)
                app.draw()

    def test_replay_limit_keeps_full_result(self):
        app = self.app(replay_limit=0)
        app.start_search()
        self.receive(app)
        self.assertFalse(app.expansions)
        self.assertGreater(app.result.expanded_nodes, 0)
        self.assertEqual(app.result.steps, 3)
        app.advance(30)
        self.assertEqual(app.path_index, 3)
        app.draw()

    def test_reset_map_change_and_quit_discard_late_results(self):
        for action in ("reset", "map", "quit"):
            with self.subTest(action=action):
                app = self.app()
                started, release = Event(), Event()
                real_search = gui.search
                cancelled = []
                self.addCleanup(release.set)

                def delayed(problem, **options):
                    started.set()
                    if not release.wait(3):
                        raise TimeoutError("Test đã chờ quá lâu")
                    cancelled.append(options["should_cancel"]())
                    return real_search(problem, algorithm=options["algorithm"])

                with patch.object(gui, "search", side_effect=delayed):
                    app.start_search()
                    self.assertTrue(started.wait(3))
                    app.toggle_pause()
                    self.assertFalse(app.paused)
                    if action == "reset":
                        app.handle_event(gui.pg.event.Event(gui.pg.KEYDOWN, key=gui.pg.K_r))
                    elif action == "map":
                        app.draw()
                        app.handle_event(gui.pg.event.Event(gui.pg.MOUSEBUTTONDOWN, button=1, pos=(1094, 160)))
                        self.assertEqual(app.map_name, "detour")
                    else:
                        gui.pg.event.post(gui.pg.event.Event(gui.pg.QUIT))
                        app.run()
                    release.set()
                    stale = self.receive(app)
                self.assertEqual(cancelled, [True])
                self.assertEqual(stale.result.status, "success")
                self.assertIsNone(app.result)
                self.assertIsNone(app.cancel_flag)

    def test_worker_error_reaches_panel(self):
        app = self.app()
        with patch.object(gui, "search", side_effect=ValueError("test worker failure")):
            app.start_search()
            self.receive(app)
        self.assertIsNone(app.cancel_flag)
        self.assertIsNone(app.result)
        self.assertIn("test worker failure", app.error)
        app.draw()
