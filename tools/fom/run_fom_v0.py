#!/usr/bin/env python3
"""Stein Agent Factory FOM v0 runner.

Minimal, synthetic, reversible runtime proof for Issue #5.
No network, live database, secrets, deploy, or merge operations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

FOM_VERSION = "0.1.0"
BLOCKED_PERMISSION_TOKENS = {
    "NETWORK",
    "LIVE_DB",
    "LIVE_DB_WRITE",
    "PRODUCTION",
    "SECRETS",
    "DEPLOY",
    "MERGE",
    "DESTRUCTIVE",
}
EXECUTORS = {
    "builtin:canonical-json-sha256": {
        "capabilities": {"canonicalize_json", "sha256"},
        "permissions": {"READ_REPO_FIXTURE", "WRITE_EVIDENCE_LOCAL"},
    }
}
REQUIRED_MISSION_FIELDS = {
    "contract_version",
    "mission_id",
    "issue",
    "base_ref",
    "base_sha",
    "requested_executor",
    "capabilities_required",
    "sources_required",
    "risk_level",
    "reversibility",
    "permissions_allowed",
    "permissions_denied",
    "human_gate",
    "input_path",
    "expected_output_sha256",
    "idempotency_key",
}


class FomStop(RuntimeError):
    """Controlled STOP: mission cannot proceed under the contract."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_mission(mission: Dict[str, Any], observed_base_sha: str) -> None:
    missing = sorted(REQUIRED_MISSION_FIELDS - mission.keys())
    if missing:
        raise FomStop(f"MISSION_INVALID_MISSING_FIELDS:{','.join(missing)}")

    if mission["contract_version"] != FOM_VERSION:
        raise FomStop("MISSION_INVALID_CONTRACT_VERSION")

    if mission["issue"] != 5:
        raise FomStop("MISSION_OUT_OF_SCOPE_ISSUE")

    if mission["base_sha"] != observed_base_sha:
        raise FomStop(
            f"STALE_BASE_SHA:mission={mission['base_sha']}:observed={observed_base_sha}"
        )

    if mission["risk_level"] != "LOW":
        raise FomStop("RISK_NOT_ALLOWED_FOR_REFERENCE_MISSION")

    denied = {str(x).upper() for x in mission["permissions_denied"]}
    allowed = {str(x).upper() for x in mission["permissions_allowed"]}
    blocked_requested = allowed & BLOCKED_PERMISSION_TOKENS
    if blocked_requested:
        raise FomStop(
            "FORBIDDEN_PERMISSION_REQUEST:" + ",".join(sorted(blocked_requested))
        )

    if not BLOCKED_PERMISSION_TOKENS.issubset(denied):
        missing_denies = sorted(BLOCKED_PERMISSION_TOKENS - denied)
        raise FomStop(
            "REFERENCE_MISSION_MUST_EXPLICITLY_DENY:" + ",".join(missing_denies)
        )

    if mission["human_gate"] != "NOT_REQUIRED_FOR_SYNTHETIC_LOCAL_RUN":
        raise FomStop("UNEXPECTED_HUMAN_GATE_CONTRACT")


def route_executor(mission: Dict[str, Any]) -> str:
    required_caps = set(mission["capabilities_required"])
    required_permissions = set(mission["permissions_allowed"])
    requested = mission["requested_executor"]

    candidates: List[str]
    if requested == "AUTO":
        candidates = sorted(EXECUTORS)
    else:
        candidates = [requested]

    for candidate in candidates:
        spec = EXECUTORS.get(candidate)
        if not spec:
            continue
        if required_caps.issubset(spec["capabilities"]) and required_permissions.issubset(
            spec["permissions"]
        ):
            return candidate

    raise FomStop("NO_ELIGIBLE_EXECUTOR")


def deterministic_run_id(mission: Dict[str, Any], input_hash: str) -> str:
    identity = "|".join(
        [
            mission["mission_id"],
            mission["idempotency_key"],
            mission["base_sha"],
            input_hash,
            FOM_VERSION,
        ]
    )
    return "fom-" + sha256_text(identity)[:20]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_fom(
    mission_path: Path,
    repo_root: Path,
    output_root: Path,
    observed_base_sha: str,
    simulate_failure_before_commit: bool = False,
) -> Dict[str, Any]:
    mission = load_json(mission_path)
    validate_mission(mission, observed_base_sha)

    trace: List[Dict[str, Any]] = []

    def event(stage: str, status: str, **extra: Any) -> None:
        trace.append({"at": utc_now(), "stage": stage, "status": status, **extra})

    event("mission_intake", "PASS", mission_id=mission["mission_id"])
    event(
        "current_state_bootstrap",
        "PASS",
        base_ref=mission["base_ref"],
        base_sha=observed_base_sha,
    )

    executor = route_executor(mission)
    event(
        "capability_routing",
        "PASS",
        requested_executor=mission["requested_executor"],
        actual_executor=executor,
    )

    input_path = (repo_root / mission["input_path"]).resolve()
    root_resolved = repo_root.resolve()
    try:
        input_path.relative_to(root_resolved)
    except ValueError as exc:
        raise FomStop("INPUT_PATH_ESCAPES_REPO") from exc

    if not input_path.is_file():
        raise FomStop("INPUT_FIXTURE_NOT_FOUND")

    raw_input = load_json(input_path)
    canonical = canonical_json(raw_input)
    output_hash = sha256_text(canonical)
    input_file_hash = hashlib.sha256(input_path.read_bytes()).hexdigest()

    event(
        "executor_tool_use",
        "PASS",
        executor=executor,
        operation="canonical_json_sha256",
        input_ref=mission["input_path"],
        input_file_sha256=input_file_hash,
        output_sha256=output_hash,
    )

    if output_hash != mission["expected_output_sha256"]:
        event(
            "verification",
            "FAIL",
            expected=mission["expected_output_sha256"],
            actual=output_hash,
        )
        raise FomStop("EXPECTED_OUTPUT_MISMATCH")

    event(
        "verification",
        "PASS",
        expected=mission["expected_output_sha256"],
        actual=output_hash,
        human_gate="NOT_TRIGGERED_P0_P1_SYNTHETIC",
    )

    run_id = deterministic_run_id(mission, input_file_hash)
    final_dir = output_root / run_id
    summary_path = final_dir / "run_summary.json"

    if summary_path.is_file():
        existing = load_json(summary_path)
        if (
            existing.get("mission_id") == mission["mission_id"]
            and existing.get("input_file_sha256") == input_file_hash
            and existing.get("result_sha256") == output_hash
            and existing.get("status") == "SUCCESS"
        ):
            return {
                "status": "IDEMPOTENT_REPLAY",
                "run_id": run_id,
                "output_dir": str(final_dir),
                "result_sha256": output_hash,
            }
        raise FomStop("IDEMPOTENCY_CONFLICT_EXISTING_OUTPUT")

    if final_dir.exists():
        raise FomStop("PARTIAL_OUTPUT_EXISTS_STOP")

    output_root.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(
        tempfile.mkdtemp(prefix=f".{run_id}.tmp-", dir=str(output_root))
    )

    try:
        event("trace_evidence", "PASS", output_staging=str(temp_dir.name))

        manifest = {
            "fom_version": FOM_VERSION,
            "mission_id": mission["mission_id"],
            "issue": mission["issue"],
            "run_id": run_id,
            "base_ref": mission["base_ref"],
            "base_sha": observed_base_sha,
            "requested_executor": mission["requested_executor"],
            "actual_executor": executor,
            "risk_level": mission["risk_level"],
            "reversibility": mission["reversibility"],
            "permissions_allowed": mission["permissions_allowed"],
            "permissions_denied": mission["permissions_denied"],
            "started_at": trace[0]["at"],
            "evidence_strength": "EXECUTION_REPRODUCED",
            "does_not_prove": [
                "generic tool registry implemented",
                "production safety",
                "DB Twin operational",
                "browser smoke testing",
                "capability router beyond the built-in reference executor",
            ],
        }
        result = {
            "mission_id": mission["mission_id"],
            "run_id": run_id,
            "operation": "canonical_json_sha256",
            "input_ref": mission["input_path"],
            "input_file_sha256": input_file_hash,
            "canonical_json": canonical,
            "result_sha256": output_hash,
            "expected_output_sha256": mission["expected_output_sha256"],
            "verified": True,
        }

        event("artifact_result", "PASS", artifact="result.json")
        event(
            "handoff_session_close",
            "PASS",
            next_gate="HUMAN_REVIEW_OF_BRANCH_PR",
            does_not_prove=manifest["does_not_prove"],
        )

        write_json(temp_dir / "manifest.json", manifest)
        write_json(temp_dir / "result.json", result)
        with (temp_dir / "trace.jsonl").open("w", encoding="utf-8") as fh:
            for row in trace:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")

        handoff = {
            "mission_id": mission["mission_id"],
            "run_id": run_id,
            "status": "SUCCESS",
            "verdict": "REFERENCE_MISSION_E2E_REPRODUCED",
            "next_human_gate": "REVIEW_AND_MERGE_ONLY",
            "does_not_prove": manifest["does_not_prove"],
        }
        write_json(temp_dir / "handoff.json", handoff)

        summary = {
            "status": "SUCCESS",
            "mission_id": mission["mission_id"],
            "run_id": run_id,
            "input_file_sha256": input_file_hash,
            "result_sha256": output_hash,
            "finished_at": utc_now(),
            "artifacts": [
                "manifest.json",
                "trace.jsonl",
                "result.json",
                "handoff.json",
                "run_summary.json",
            ],
        }
        write_json(temp_dir / "run_summary.json", summary)

        if simulate_failure_before_commit:
            raise FomStop("SIMULATED_FAILURE_BEFORE_ATOMIC_COMMIT")

        os.replace(temp_dir, final_dir)
        return {
            "status": "SUCCESS",
            "run_id": run_id,
            "output_dir": str(final_dir),
            "result_sha256": output_hash,
        }
    except Exception:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stein Agent Factory FOM v0 reference mission.")
    parser.add_argument("--mission", required=True, type=Path)
    parser.add_argument("--repo-root", default=Path("."), type=Path)
    parser.add_argument("--output-root", default=Path("evidence/fom"), type=Path)
    parser.add_argument("--observed-base-sha", required=True)
    parser.add_argument("--simulate-failure-before-commit", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = run_fom(
            mission_path=args.mission,
            repo_root=args.repo_root,
            output_root=args.output_root,
            observed_base_sha=args.observed_base_sha,
            simulate_failure_before_commit=args.simulate_failure_before_commit,
        )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except FomStop as exc:
        print(json.dumps({"status": "STOP", "reason": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
