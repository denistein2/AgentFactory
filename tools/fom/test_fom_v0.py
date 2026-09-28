#!/usr/bin/env python3
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

HERE = Path(__file__).resolve()
MODULE_PATH = HERE.parent / "run_fom_v0.py"
spec = importlib.util.spec_from_file_location("run_fom_v0", MODULE_PATH)
fom = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(fom)


class FomV0HardeningTests(unittest.TestCase):
    def git(self, root: Path, *args: str) -> str:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()

    def setup_repo(self, root: Path):
        self.git(root, "init", "-q", "-b", "main")
        self.git(root, "config", "user.email", "fom-test@example.invalid")
        self.git(root, "config", "user.name", "FOM Test")

        fixture = root / "docs/missions/FACTORY-FOM-001/fixtures/synthetic_payload.json"
        fixture.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "mission": "synthetic-canonical-json-hash",
            "items": [{"id": "B", "qty": 2}, {"id": "A", "qty": 1}],
            "metadata": {"synthetic": True, "contains_real_data": False},
        }
        fixture.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "base fixture")
        base_sha = self.git(root, "rev-parse", "main")

        self.git(root, "checkout", "-qb", "feature")
        runner_copy = root / "tools/fom/run_fom_v0.py"
        runner_copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(MODULE_PATH, runner_copy)

        mission = {
            "contract_version": fom.FOM_VERSION,
            "mission_id": "TEST-FOM-HARDENING",
            "issue": 5,
            "base_ref": "main",
            "base_sha": base_sha,
            "base_sha_policy": "PINNED",
            "requested_executor": "AUTO",
            "capabilities_required": ["canonicalize_json", "sha256"],
            "sources_required": [
                "docs/missions/FACTORY-FOM-001/fixtures/synthetic_payload.json"
            ],
            "risk_level": "LOW",
            "reversibility": "FULL",
            "permissions_allowed": [
                "READ_REPO_FIXTURE",
                "WRITE_EVIDENCE_LOCAL",
            ],
            "permissions_denied": [
                "NETWORK", "LIVE_DB", "LIVE_DB_WRITE", "PRODUCTION",
                "SECRETS", "DEPLOY", "MERGE", "DESTRUCTIVE",
            ],
            "human_gate": "NOT_REQUIRED_FOR_SYNTHETIC_LOCAL_RUN",
            "input_path": "docs/missions/FACTORY-FOM-001/fixtures/synthetic_payload.json",
            "expected_output_sha256": fom.sha256_text(fom.canonical_json(payload)),
            "idempotency_key": "TEST-FOM-HARDENING:v1",
        }

        mission_path = root / "docs/missions/FACTORY-FOM-001/MISSION_REFERENCE_SYNTHETIC.json"
        mission_path.write_text(json.dumps(mission, indent=2) + "\n", encoding="utf-8")
        self.git(root, "add", ".")
        self.git(root, "commit", "-qm", "feature runner and mission")
        return mission_path, mission, runner_copy, self.load_runtime(runner_copy)

    def load_runtime(self, runner_copy):
        spec = importlib.util.spec_from_file_location("fom_runtime_" + uuid4().hex, runner_copy)
        runtime = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(runtime)
        return runtime

    def run_fom(self, runtime, mission_path, root, **kwargs):
        return runtime.run_fom(
            mission_path=mission_path,
            repo_root=root,
            output_root=kwargs.pop("output_root", Path("evidence/test-fom")),
            **kwargs,
        )

    def commit_mission(self, root: Path, mission_path: Path, mission: dict):
        mission_path.write_text(json.dumps(mission, indent=2) + "\n", encoding="utf-8")
        self.git(root, "add", str(mission_path.relative_to(root)))
        self.git(root, "commit", "-qm", "mutate mission")

    def test_success_and_idempotent_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy, runtime = self.setup_repo(root)
            first = self.run_fom(runtime, mission_path, root)
            second = self.run_fom(runtime, mission_path, root)
            self.assertEqual(first["status"], "SUCCESS")
            self.assertEqual(second["status"], "IDEMPOTENT_REPLAY")
            self.assertEqual(first["run_id"], second["run_id"])

    def test_changed_runner_material_does_not_reuse_old_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy, runtime = self.setup_repo(root)
            first = self.run_fom(runtime, mission_path, root)
            runner_copy.write_text(runner_copy.read_text(encoding="utf-8") + "\n# changed\n", encoding="utf-8")
            self.git(root, "add", str(runner_copy.relative_to(root)))
            self.git(root, "commit", "-qm", "change runner material")
            runtime = self.load_runtime(runner_copy)
            second = self.run_fom(runtime, mission_path, root)
            self.assertEqual(second["status"], "SUCCESS")
            self.assertNotEqual(first["run_id"], second["run_id"])

    def test_uncommitted_runner_material_stops_before_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy, runtime = self.setup_repo(root)
            first = self.run_fom(runtime, mission_path, root)
            runner_copy.write_text(runner_copy.read_text(encoding="utf-8") + "\n# uncommitted\n", encoding="utf-8")
            changed_runtime = self.load_runtime(runner_copy)
            with self.assertRaises(changed_runtime.FomStop) as ctx:
                self.run_fom(changed_runtime, mission_path, root)
            self.assertIn("EXECUTION_MATERIAL_DIFFERS_FROM_HEAD", str(ctx.exception))
            self.assertNotEqual(first["status"], "IDEMPOTENT_REPLAY")

    def test_changed_mission_material_does_not_reuse_old_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, mission, runner_copy, runtime = self.setup_repo(root)
            first = self.run_fom(runtime, mission_path, root)
            mission["review_note"] = "mission bytes changed"
            self.commit_mission(root, mission_path, mission)
            second = self.run_fom(runtime, mission_path, root)
            self.assertEqual(second["status"], "SUCCESS")
            self.assertNotEqual(first["run_id"], second["run_id"])

    def test_changed_fixture_material_does_not_reuse_old_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, mission, runner_copy, runtime = self.setup_repo(root)
            first = self.run_fom(runtime, mission_path, root)
            fixture = root / mission["input_path"]
            payload = json.loads(fixture.read_text(encoding="utf-8"))
            payload["items"].append({"id": "C", "qty": 3})
            fixture.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            mission["expected_output_sha256"] = runtime.sha256_text(runtime.canonical_json(payload))
            mission_path.write_text(json.dumps(mission, indent=2) + "\n", encoding="utf-8")
            self.git(root, "add", ".")
            self.git(root, "commit", "-qm", "change fixture and expected result")
            runtime = self.load_runtime(runner_copy)
            second = self.run_fom(runtime, mission_path, root)
            self.assertEqual(second["status"], "SUCCESS")
            self.assertNotEqual(first["run_id"], second["run_id"])

    def test_live_main_movement_stops_without_caller_override(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy, runtime = self.setup_repo(root)
            self.git(root, "checkout", "-q", "main")
            (root / "main-moved.txt").write_text("moved\n", encoding="utf-8")
            self.git(root, "add", "main-moved.txt")
            self.git(root, "commit", "-qm", "move main")
            self.git(root, "checkout", "-q", "feature")
            with self.assertRaises(runtime.FomStop) as ctx:
                self.run_fom(runtime, mission_path, root)
            self.assertIn("STALE_BASE_SHA", str(ctx.exception))

    def test_current_main_reference_verification_survives_main_advance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, mission, runner_copy, runtime = self.setup_repo(root)
            mission["base_sha_policy"] = "CURRENT_MAIN"
            mission["base_sha"] = "CURRENT_MAIN"
            self.commit_mission(root, mission_path, mission)
            first = self.run_fom(runtime, mission_path, root)
            self.git(root, "checkout", "-q", "main")
            (root / "main-moved.txt").write_text("post-merge main\n", encoding="utf-8")
            self.git(root, "add", "main-moved.txt")
            self.git(root, "commit", "-qm", "advance main after merge")
            self.git(root, "checkout", "-q", "feature")
            second = self.run_fom(runtime, mission_path, root)
            self.assertEqual(second["status"], "SUCCESS")
            self.assertNotEqual(first["run_id"], second["run_id"])

    def test_current_main_policy_requires_explicit_sentinel(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, mission, runner_copy, runtime = self.setup_repo(root)
            mission["base_sha_policy"] = "CURRENT_MAIN"
            self.commit_mission(root, mission_path, mission)
            with self.assertRaises(runtime.FomStop) as ctx:
                self.run_fom(runtime, mission_path, root)
            self.assertIn("CURRENT_MAIN_BASE_POLICY_REQUIRES_EXPLICIT_SENTINEL", str(ctx.exception))

    def test_missing_write_permission_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, mission, runner_copy, runtime = self.setup_repo(root)
            mission["permissions_allowed"].remove("WRITE_EVIDENCE_LOCAL")
            self.commit_mission(root, mission_path, mission)
            with self.assertRaises(runtime.FomStop) as ctx:
                self.run_fom(runtime, mission_path, root)
            self.assertIn("MISSING_REQUIRED_REFERENCE_PERMISSION", str(ctx.exception))

    def test_output_root_escape_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy, runtime = self.setup_repo(root)
            with self.assertRaises(runtime.FomStop) as ctx:
                self.run_fom(
                    runtime,
                    mission_path,
                    root,
                    output_root=root / "outside-evidence",
                )
            self.assertIn("OUTPUT_ROOT_OUTSIDE_REPO_EVIDENCE", str(ctx.exception))

    def test_evidence_root_symlink_escape_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, _, runtime = self.setup_repo(root)
            outside = root.parent / (root.name + "-outside-evidence")
            outside.mkdir()
            try:
                (root / "evidence").symlink_to(outside, target_is_directory=True)
                with self.assertRaises(runtime.FomStop) as ctx:
                    self.run_fom(runtime, mission_path, root)
                self.assertIn("EVIDENCE_ROOT_ESCAPES_REPO", str(ctx.exception))
            finally:
                if outside.exists():
                    shutil.rmtree(outside)

    def test_trace_tamper_stops_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy, runtime = self.setup_repo(root)
            first = self.run_fom(runtime, mission_path, root)
            trace = Path(first["output_dir"]) / "trace.jsonl"
            trace.write_text(trace.read_text(encoding="utf-8") + "{}\n", encoding="utf-8")
            with self.assertRaises(runtime.FomStop) as ctx:
                self.run_fom(runtime, mission_path, root)
            self.assertIn("EVIDENCE_INTEGRITY_MISMATCH", str(ctx.exception))

    def test_handoff_tamper_stops_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy, runtime = self.setup_repo(root)
            first = self.run_fom(runtime, mission_path, root)
            handoff_path = Path(first["output_dir"]) / "handoff.json"
            handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
            handoff["status"] = "TAMPERED"
            handoff_path.write_text(json.dumps(handoff) + "\n", encoding="utf-8")
            with self.assertRaises(runtime.FomStop) as ctx:
                self.run_fom(runtime, mission_path, root)
            self.assertIn("EVIDENCE_INTEGRITY_MISMATCH", str(ctx.exception))

    def test_runtime_emits_execution_material_provenance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy, runtime = self.setup_repo(root)
            first = self.run_fom(runtime, mission_path, root)
            provenance = json.loads(
                (Path(first["output_dir"]) / "provenance.json").read_text(encoding="utf-8")
            )
            self.assertTrue(provenance["generated_by_runtime"])
            self.assertEqual(provenance["runtime_head_sha"], self.git(root, "rev-parse", "HEAD"))
            self.assertEqual(provenance["base_sha_policy"], "PINNED")
            self.assertEqual(provenance["declared_base_sha"], provenance["base_sha_observed"])
            self.assertEqual(len(provenance["execution_material_fingerprint"]), 64)
            for key in ("runner", "mission", "fixture"):
                entry = provenance["execution_material"][key]
                self.assertEqual(len(entry["git_blob_sha"]), 40)
                self.assertEqual(len(entry["file_sha256"]), 64)

    def test_controlled_failure_leaves_no_final_side_effect(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy, runtime = self.setup_repo(root)
            output = root / "evidence/test-fom"
            with self.assertRaises(runtime.FomStop):
                self.run_fom(
                    runtime,
                    mission_path,
                    root,
                    simulate_failure_before_commit=True,
                )
            if output.exists():
                visible = [p for p in output.iterdir() if not p.name.startswith(".")]
                self.assertEqual(visible, [])

    def test_forbidden_permission_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, mission, runner_copy, runtime = self.setup_repo(root)
            mission["permissions_allowed"].append("LIVE_DB_WRITE")
            self.commit_mission(root, mission_path, mission)
            with self.assertRaises(runtime.FomStop) as ctx:
                self.run_fom(runtime, mission_path, root)
            self.assertIn("FORBIDDEN_PERMISSION_REQUEST", str(ctx.exception))

    def test_undeclared_source_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, mission, runner_copy, runtime = self.setup_repo(root)
            mission["sources_required"] = []
            self.commit_mission(root, mission_path, mission)
            with self.assertRaises(runtime.FomStop) as ctx:
                self.run_fom(runtime, mission_path, root)
            self.assertIn("INPUT_NOT_DECLARED_AS_REQUIRED_SOURCE", str(ctx.exception))

    def test_incomplete_evidence_pack_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy, runtime = self.setup_repo(root)
            first = self.run_fom(runtime, mission_path, root)
            (Path(first["output_dir"]) / "result.json").unlink()
            with self.assertRaises(runtime.FomStop) as ctx:
                self.run_fom(runtime, mission_path, root)
            self.assertIn("INCOMPLETE_EVIDENCE_PACK", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
