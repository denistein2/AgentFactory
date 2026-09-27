#!/usr/bin/env python3
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
MODULE_PATH = HERE.parent / "run_fom_v0.py"
spec = importlib.util.spec_from_file_location("run_fom_v0", MODULE_PATH)
fom = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(fom)

BASE_SHA = "758478192a79728a653736e48fa35078cce0d6f4"

class FomV0Tests(unittest.TestCase):
    def make_fixture(self, root: Path):
        fixture = root / "fixture.json"
        fixture.write_text(
            json.dumps({"b": 2, "a": 1}, ensure_ascii=False),
            encoding="utf-8",
        )
        canonical = fom.canonical_json({"b": 2, "a": 1})
        mission = {
            "contract_version": "0.1.0",
            "mission_id": "TEST-FOM-REF",
            "issue": 5,
            "base_ref": "main",
            "base_sha": BASE_SHA,
            "requested_executor": "AUTO",
            "capabilities_required": ["canonicalize_json", "sha256"],
            "sources_required": ["fixture.json"],
            "risk_level": "LOW",
            "reversibility": "FULL",
            "permissions_allowed": ["READ_REPO_FIXTURE", "WRITE_EVIDENCE_LOCAL"],
            "permissions_denied": [
                "NETWORK", "LIVE_DB", "LIVE_DB_WRITE", "PRODUCTION",
                "SECRETS", "DEPLOY", "MERGE", "DESTRUCTIVE"
            ],
            "human_gate": "NOT_REQUIRED_FOR_SYNTHETIC_LOCAL_RUN",
            "input_path": "fixture.json",
            "expected_output_sha256": fom.sha256_text(canonical),
            "idempotency_key": "TEST-FOM-REF:v1",
        }
        mission_path = root / "mission.json"
        mission_path.write_text(json.dumps(mission), encoding="utf-8")
        return mission_path, mission

    def test_success_and_idempotent_replay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _ = self.make_fixture(root)
            output = root / "evidence"
            first = fom.run_fom(mission_path, root, output, BASE_SHA)
            second = fom.run_fom(mission_path, root, output, BASE_SHA)
            self.assertEqual(first["status"], "SUCCESS")
            self.assertEqual(second["status"], "IDEMPOTENT_REPLAY")
            self.assertEqual(first["run_id"], second["run_id"])
            self.assertEqual(len([p for p in output.iterdir() if p.is_dir()]), 1)

    def test_controlled_failure_leaves_no_final_side_effect(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _ = self.make_fixture(root)
            output = root / "evidence"
            with self.assertRaises(fom.FomStop):
                fom.run_fom(
                    mission_path, root, output, BASE_SHA,
                    simulate_failure_before_commit=True,
                )
            if output.exists():
                visible = [p for p in output.iterdir() if not p.name.startswith(".")]
                self.assertEqual(visible, [])
            retry = fom.run_fom(mission_path, root, output, BASE_SHA)
            self.assertEqual(retry["status"], "SUCCESS")

    def test_forbidden_permission_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, mission = self.make_fixture(root)
            mission["permissions_allowed"].append("LIVE_DB_WRITE")
            mission_path.write_text(json.dumps(mission), encoding="utf-8")
            output = root / "evidence"
            with self.assertRaises(fom.FomStop) as ctx:
                fom.run_fom(mission_path, root, output, BASE_SHA)
            self.assertIn("FORBIDDEN_PERMISSION_REQUEST", str(ctx.exception))
            self.assertFalse(output.exists())

    def test_stale_base_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _ = self.make_fixture(root)
            with self.assertRaises(fom.FomStop) as ctx:
                fom.run_fom(mission_path, root, root / "evidence", "deadbeef")
            self.assertIn("STALE_BASE_SHA", str(ctx.exception))

    def test_incomplete_evidence_pack_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, _ = self.make_fixture(root)
            output = root / "evidence"
            first = fom.run_fom(mission_path, root, output, BASE_SHA)
            self.assertEqual(first["status"], "SUCCESS")
            (Path(first["output_dir"]) / "result.json").unlink()
            with self.assertRaises(fom.FomStop) as ctx:
                fom.run_fom(mission_path, root, output, BASE_SHA)
            self.assertIn("INCOMPLETE_EVIDENCE_PACK", str(ctx.exception))

    def test_undeclared_source_stops(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mission_path, mission = self.make_fixture(root)
            mission["sources_required"] = []
            mission_path.write_text(json.dumps(mission), encoding="utf-8")
            with self.assertRaises(fom.FomStop) as ctx:
                fom.run_fom(mission_path, root, root / "evidence", BASE_SHA)
            self.assertIn("INPUT_NOT_DECLARED_AS_REQUIRED_SOURCE", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
