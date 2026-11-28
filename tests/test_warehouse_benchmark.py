import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from statistics import median
from tempfile import TemporaryDirectory
from unittest.mock import patch

from bonus.warehouse import benchmark, plotting


class BenchmarkTests(unittest.TestCase):
    small = {
        **benchmark.PROFILES["quick"],
        "single_sizes": (4,), "multi_sizes": (4,),
        "single_densities": (10,), "multi_densities": (10,), "seeds": (11,),
    }

    def test_validation_reports_bad_arguments(self):
        for flag, value in (("--repeats", "0"), ("--repeats", "1.5"), ("--warmups", "-1")):
            with self.subTest(flag=flag, value=value), redirect_stderr(io.StringIO()) as stderr:
                with self.assertRaises(SystemExit) as raised:
                    benchmark.main([flag, value])
                self.assertEqual(raised.exception.code, 2)
                self.assertIn(flag, stderr.getvalue())
                self.assertNotIn("Traceback", stderr.getvalue())

    def test_manifest_distinguishes_repeats_warmups_and_environment(self):
        maps, tasks = benchmark._inputs(self.small)
        with patch.dict(benchmark.PROFILES, {"quick": self.small}):
            manifests = [benchmark._manifest("quick", maps, tasks, r, w)
                         for r, w in ((3, 0), (3, 1), (5, 1))]
            env = {**manifests[1]["environment"], "machine": "other"}
            with patch.object(benchmark, "_environment", return_value=env):
                manifests.append(benchmark._manifest("quick", maps, tasks, 3, 1))
        self.assertEqual(len({m["config_id"] for m in manifests}), 4)
        self.assertEqual(manifests[1]["measurement"], {
            "repeats": 3, "warmups": 1, "order": benchmark.ORDER_RULE,
        })

    def test_interleaved_repeats_resume_and_warmups_stay_out_of_raw(self):
        calls = []

        def measure(directory, identity, task):
            calls.append(identity)
            return {**identity, **_row("success", 4, 0.01)}

        with TemporaryDirectory() as folder, redirect_stdout(io.StringIO()):
            output = Path(folder)
            with patch.dict(benchmark.PROFILES, {"quick": self.small}), patch.object(
                benchmark, "_measure", side_effect=measure
            ):
                directory = benchmark.run("quick", output, repeats=3, warmups=1)
                manifest, tasks = benchmark.load_run(directory)
                self.assertEqual(len(tasks), 5)
                raw = sorted((directory / "raw").glob("*.json"))
                self.assertEqual(len(raw), 57)
                self.assertEqual(len(calls), 76)
                first = [call for call in calls if call["task_id"] == tasks[0]["task_id"]]
                self.assertEqual([call["variant"] for call in first[:8]],
                                 ["astar", "bfs", "ucs", "greedy", "bfs", "ucs", "greedy", "astar"])
                self.assertEqual([call["variant"] for call in first[8:12]],
                                 ["ucs", "greedy", "astar", "bfs"])
                self.assertTrue(all("session_id" not in call for call in first[:4]))
                self.assertEqual({benchmark.read_json(path)["repeat_index"] for path in raw}, {1, 2, 3})
                preserved = raw[1].read_bytes()
                removed = benchmark.read_json(raw[0])
                raw[0].unlink()
                cases = plotting.collect(directory, manifest, tasks)
                self.assertIn("**56/57**", plotting.summary(manifest, cases))
                calls.clear()
                self.assertEqual(benchmark.run("quick", output, repeats=3, warmups=1), directory)
                self.assertEqual(raw[1].read_bytes(), preserved)
                changed = benchmark.read_json(raw[0])
                self.assertEqual(len(calls), 2)
                self.assertNotIn("session_id", calls[0])
                self.assertEqual(calls[1]["repeat_index"], removed["repeat_index"])
                self.assertEqual(changed["variant"], removed["variant"])
                self.assertNotEqual(changed["session_id"], removed["session_id"])
                session = benchmark.read_json(directory / "sessions" / f"{changed['session_id']}.json")
                self.assertEqual((session["existing_attempts"], session["warmup_attempts"],
                                  session["new_attempts"], session["status"]), (56, 1, 1, "complete"))
                self.assertLessEqual(session["started_utc"], session["finished_utc"])
                changed["config_id"] = "different-config"
                benchmark.write_json(raw[0], changed)
                with self.assertRaisesRegex(ValueError, "không khớp cấu hình"):
                    benchmark.run("quick", output, repeats=3, warmups=1)

    def test_legacy_data_has_no_within_task_spread_and_is_left_untouched(self):
        source = benchmark.OUTPUT_DIR / "quick" / "499428006f3cdd0d2ad4"
        manifest, tasks = benchmark.load_run(source)
        self.assertEqual(manifest["schema_version"], 1)
        cases = plotting.collect(source, manifest, tasks)
        self.assertEqual(len(cases), 40)
        self.assertTrue(all(stats.quartiles is None for _, rows in cases for stats in rows.values()))
        with TemporaryDirectory() as folder, patch.object(plotting, "_charts"):
            legacy = Path(folder) / "legacy"
            benchmark.write_json(legacy / "manifest.json", manifest)
            benchmark.write_json(legacy / "tasks.json", tasks)
            original = legacy / "summary.md"
            original.write_text("legacy summary", encoding="utf-8")
            plotting.plot(legacy)
            self.assertEqual(original.read_text(encoding="utf-8"), "legacy summary")
            details = (legacy.with_name("legacy-analysis-v2") / "repeat_details.md").read_text(encoding="utf-8")
            self.assertIn("không có", details)


def _row(status, cost=None, time=0.001, **overrides):
    return dict(
        status=status, total_cost=cost, elapsed_seconds=time, steps=4, expanded_nodes=4,
        generated_nodes=7, peak_frontier_entries=3, pickup_order=["P1"],
    ) | overrides


class AggregationTests(unittest.TestCase):
    def case(self, name, **variants):
        task = dict(task_id=name, mode="single", cost_kind="weighted", size=8, density_percent=30,
                    pickup_count=1, variants=("ucs", "astar"))
        return task, {variant: plotting._task_stats(attempts, 3) for variant, attempts in variants.items()}

    def test_timing_uses_one_median_per_task(self):
        first = self.case(
            "first", ucs=[_row("success", 4, t) for t in (1, 2, 100)],
            astar=[_row("success", 4, t) for t in (2, 4, 6)],
        )
        second = self.case(
            "second", ucs=[_row("success", 4, t) for t in (6, 7, 8)],
            astar=[_row("success", 4, t) for t in (7, 14, 21)],
        )
        self.assertEqual(first[1]["ucs"].quartiles, (1.5, 51.0))
        self.assertEqual(first[1]["ucs"].median_seconds, 2)
        paired = plotting._paired([first, second], ("ucs", "astar"))
        self.assertEqual(len(paired), 2)
        self.assertEqual(median(row["ucs"]["elapsed_seconds"] for row in paired), 4.5)
        self.assertEqual(plotting._time_ratios(paired, "astar"), [2, 2])
        self.assertEqual(plotting._ratios([first, second], "astar"), [1, 1])

    def test_missing_failures_and_mixed_timeouts_are_reported_separately(self):
        success = _row("success", 4)
        cases = [
            self.case("mixed", ucs=[_row("timeout", time=99), success, success], astar=[success] * 3),
            self.case("failures", ucs=[_row("no_path")] * 3, astar=[_row("node_limit")] * 3),
            self.case("missing", ucs=[], astar=[success]),
            self.case("zero", ucs=[_row("success", 0)] * 3, astar=[_row("success", 0)] * 3),
            self.case("no-ucs", astar=[success] * 3),
        ]
        self.assertEqual(cases[0][1]["ucs"].median_seconds, success["elapsed_seconds"])
        self.assertIsNone(cases[0][1]["ucs"].quartiles)
        self.assertTrue(cases[0][1]["ucs"].mixed_timeout)
        self.assertEqual(len(plotting._paired(cases, ("ucs", "astar"))), 1)
        self.assertEqual(plotting._ratios(cases, "astar"), [])
        self.assertEqual(plotting._time_ratios(plotting._paired(cases[-1:], ("astar",)), "astar"), [])
        report = plotting.summary(
            {"profile": "quick", "config_id": "test", "schema_version": 2,
             "measurement": {"repeats": 3}, "environment": benchmark._environment()}, cases,
        )
        self.assertIn("**22/30**", report)
        self.assertIn("Có timeout xen trạng thái khác 1", report)
        self.assertIn("Timeout xen trạng thái khác", plotting.repeat_details(cases))

    def test_inconsistent_success_fields_exclude_task_from_comparison(self):
        original = _row("success", 4)
        modified = _row("success", 6, expanded_nodes=8, steps=5, pickup_order=["P2"])
        case = self.case("inconsistent", ucs=[original] * 3, astar=[original, modified, original])
        self.assertEqual(case[1]["astar"].inconsistent,
                         ("total_cost", "steps", "expanded_nodes", "pickup_order"))
        self.assertEqual(plotting._paired([case], ("ucs", "astar")), [])
        self.assertEqual(plotting._ratios([case], "astar"), [])
        self.assertIn("Success lệch total_cost", plotting.repeat_details([case]))
