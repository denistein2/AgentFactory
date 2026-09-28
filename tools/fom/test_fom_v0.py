#!/usr/bin/env python3
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

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
        return mission_path, mission, runner_copy

    def run_fom(self, mission_path, root, runner_copy, **kwargs):
        return fom.run_fom(
            mission_path=mission_path,
            repo_root=root,
            output_root=kwargs.pop("output_root", Path("evidence/test-fom")),
            runner_path=runner_copy,
            **kwargs,
        )

    def commit_mission(self, root: Path, mission_path: Path, mission: dict):
        mission_path.write_text(json.dumps(mission, indent=2) + "\n", encoding="utf-8")
        self.git(root, "add", str(mission_path.relative_to(root)))
        self.git(root, "commit", "-qm", "mutate mission")

    def test_success_and_idempotent_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy = self.setup_repo(root)
            first = self.run_fom(mission_path, root, runner_copy)
            second = self.run_fom(mission_path, root, runner_copy)
            self.assertEqual(first["status"], "SUCCESS")
            self.assertEqual(second["status"], "IDEMPOTENT_REPLAY")
            self.assertEqual(first["run_id"], second["run_id"])

    def test_live_main_movement_stops_without_caller_override(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy = self.setup_repo(root)
            self.git(root, "checkout", "-q", "main")
            (root / "main-moved.txt").write_text("moved\n", encoding="utf-8")
            self.git(root, "add", "main-moved.txt")
            self.git(root, "commit", "-qm", "move main")
            self.git(root, "checkout", "-q", "feature")
            with self.assertRaises(fom.FomStop) as ctx:
                self.run_fom(mission_path, root, runner_copy)
            self.assertIn("STALE_BASE_SHA", str(ctx.exception))

    def test_missing_write_permission_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, mission, runner_copy = self.setup_repo(root)
            mission["permissions_allowed"].remove("WRITE_EVIDENCE_LOCAL")
            self.commit_mission(root, mission_path, mission)
            with self.assertRaises(fom.FomStop) as ctx:
                self.run_fom(mission_path, root, runner_copy)
            self.assertIn("MISSING_REQUIRED_REFERENCE_PERMISSION", str(ctx.exception))

    def test_output_root_escape_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy = self.setup_repo(root)
            with self.assertRaises(fom.FomStop) as ctx:
                self.run_fom(
                    mission_path,
                    root,
                    runner_copy,
                    output_root=root / "outside-evidence",
                )
            self.assertIn("OUTPUT_ROOT_OUTSIDE_REPO_EVIDENCE", str(ctx.exception))

    def test_trace_tamper_stops_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy = self.setup_repo(root)
            first = self.run_fom(mission_path, root, runner_copy)
            trace = Path(first["output_dir"]) / "trace.jsonl"
            trace.write_text(trace.read_text(encoding="utf-8") + "{}\n", encoding="utf-8")
            with self.assertRaises(fom.FomStop) as ctx:
                self.run_fom(mission_path, root, runner_copy)
            self.assertIn("EVIDENCE_INTEGRITY_MISMATCH", str(ctx.exception))

    def test_handoff_tamper_stops_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy = self.setup_repo(root)
            first = self.run_fom(mission_path, root, runner_copy)
            handoff_path = Path(first["output_dir"]) / "handoff.json"
            handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
            handoff["status"] = "TAMPERED"
            handoff_path.write_text(json.dumps(handoff) + "\n", encoding="utf-8")
            with self.assertRaises(fom.FomStop) as ctx:
                self.run_fom(mission_path, root, runner_copy)
            self.assertIn("EVIDENCE_INTEGRITY_MISMATCH", str(ctx.exception))

    def test_runtime_emits_execution_material_provenance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy = self.setup_repo(root)
            first = self.run_fom(mission_path, root, runner_copy)
            provenance = json.loads(
                (Path(first["output_dir"]) / "provenance.json").read_text(encoding="utf-8")
            )
            self.assertTrue(provenance["generated_by_runtime"])
            for key in ("runner", "mission", "fixture"):
                entry = provenance["execution_material"][key]
                self.assertEqual(len(entry["git_blob_sha"]), 40)
                self.assertEqual(len(entry["file_sha256"]), 64)

    def test_controlled_failure_leaves_no_final_side_effect(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy = self.setup_repo(root)
            output = root / "evidence/test-fom"
            with self.assertRaises(fom.FomStop):
                self.run_fom(
                    mission_path,
                    root,
                    runner_copy,
                    simulate_failure_before_commit=True,
                )
            if output.exists():
                visible = [p for p in output.iterdir() if not p.name.startswith(".")]
                self.assertEqual(visible, [])

    def test_forbidden_permission_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, mission, runner_copy = self.setup_repo(root)
            mission["permissions_allowed"].append("LIVE_DB_WRITE")
            self.commit_mission(root, mission_path, mission)
            with self.assertRaises(fom.FomStop) as ctx:
                self.run_fom(mission_path, root, runner_copy)
            self.assertIn("FORBIDDEN_PERMISSION_REQUEST", str(ctx.exception))

    def test_undeclared_source_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, mission, runner_copy = self.setup_repo(root)
            mission["sources_required"] = []
            self.commit_mission(root, mission_path, mission)
            with self.assertRaises(fom.FomStop) as ctx:
                self.run_fom(mission_path, root, runner_copy)
            self.assertIn("INPUT_NOT_DECLARED_AS_REQUIRED_SOURCE", str(ctx.exception))

    def test_incomplete_evidence_pack_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _, runner_copy = self.setup_repo(root)
            first = self.run_fom(mission_path, root, runner_copy)
            (Path(first["output_dir"]) / "result.json").unlink()
            with self.assertRaises(fom.FomStop) as ctx:
                self.run_fom(mission_path, root, runner_copy)
            self.assertIn("INCOMPLETE_EVIDENCE_PACK", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
