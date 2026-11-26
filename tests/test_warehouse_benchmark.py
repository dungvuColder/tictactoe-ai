import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from bonus.warehouse import benchmark, plotting


class BenchmarkTests(unittest.TestCase):
    def test_resume_restores_missing_jobs_and_rejects_changed_identity(self):
        small = {
            **benchmark.PROFILES["quick"],
            "single_sizes": (4,), "multi_sizes": (4,),
            "single_densities": (10,), "multi_densities": (10,), "seeds": (11,),
        }
        with TemporaryDirectory() as folder, redirect_stdout(io.StringIO()):
            output = Path(folder)
            with patch.dict(benchmark.PROFILES, {"quick": small}):
                directory = benchmark.run("quick", output)
                manifest, tasks = benchmark.load_run(directory)
                self.assertEqual(len(tasks), 5)
                raw = sorted((directory / "raw").glob("*.json"))
                self.assertEqual(len(raw), 19)
                preserved = raw[1].read_bytes()
                raw[0].unlink()
                cases = plotting.collect(directory, manifest, tasks)
                self.assertIn("**18/19**", plotting.summary(manifest, cases))
                self.assertEqual(benchmark.run("quick", output), directory)
                self.assertEqual(raw[1].read_bytes(), preserved)
                self.assertTrue(raw[0].is_file())
                changed = benchmark.read_json(raw[0])
                changed["config_id"] = "different-config"
                benchmark.write_json(raw[0], changed)
                with self.assertRaisesRegex(ValueError, "không khớp cấu hình"):
                    benchmark.run("quick", output)

    def test_summary_uses_paired_times_and_excludes_unsolved_ucs_references(self):
        template = dict(mode="single", cost_kind="weighted", size=8, density_percent=30,
                        pickup_count=1, variants=("ucs", "astar"))

        def row(status, cost=None):
            return dict(status=status, total_cost=cost, elapsed_seconds=0.001, expanded_nodes=4)

        cases = [
            (template, {"ucs": row("success", 4), "astar": row("success", 6)}),
            (template, {"ucs": row("timeout"), "astar": row("success", 7)}),
            (template, {"ucs": row("no_path"), "astar": row("node_limit")}),
            (template, {"ucs": row("success", 0), "astar": row("success", 0)}),
            (template, {}),
        ]
        self.assertEqual(len(plotting._paired(cases, template["variants"])), 2)
        self.assertEqual(plotting._ratios(cases, "astar"), [1.5])
        self.assertEqual(plotting._ratios(cases[1:3], "astar"), [])
        self.assertEqual(plotting._paired(cases[1:3], template["variants"]), [])
        self.assertEqual(plotting._paired(cases[-1:], template["variants"]), [])
        report = plotting.summary(
            {"profile": "quick", "config_id": "test", "environment": benchmark._environment()}, cases,
        )
        self.assertIn("**8/10**", report)
        self.assertIn("2/4 (50%) | 1 | 1 | 0", report)
        self.assertIn("3/4 (75%) | 0 | 0 | 1", report)
