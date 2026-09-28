#!/usr/bin/env python3
"""Stein Agent Factory FOM v0.1.1 hardened reference runner."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

FOM_VERSION = "0.1.2"

BLOCKED_PERMISSION_TOKENS = {
    "NETWORK", "LIVE_DB", "LIVE_DB_WRITE", "PRODUCTION",
    "SECRETS", "DEPLOY", "MERGE", "DESTRUCTIVE",
}
REQUIRED_REFERENCE_PERMISSIONS = {"READ_REPO_FIXTURE", "WRITE_EVIDENCE_LOCAL"}

EXECUTORS = {
    "builtin:canonical-json-sha256": {
        "capabilities": {"canonicalize_json", "sha256"},
        "permissions": {"READ_REPO_FIXTURE", "WRITE_EVIDENCE_LOCAL"},
    }
}

REQUIRED_MISSION_FIELDS = {
    "contract_version", "mission_id", "issue", "base_ref", "base_sha",
    "base_sha_policy",
    "requested_executor", "capabilities_required", "sources_required",
    "risk_level", "reversibility", "permissions_allowed", "permissions_denied",
    "human_gate", "input_path", "expected_output_sha256", "idempotency_key",
}

REQUIRED_EVIDENCE_FILES = {
    "manifest.json", "trace.jsonl", "result.json",
    "handoff.json", "provenance.json", "run_summary.json",
}


class FomStop(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(text_value: str) -> str:
    return hashlib.sha256(text_value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def git(repo_root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise FomStop(
            "GIT_CURRENT_STATE_UNAVAILABLE:"
            + " ".join(args)
            + ":"
            + (proc.stderr.strip() or proc.stdout.strip() or "unknown")
        )
    return proc.stdout.strip()


def resolve_git_ref(repo_root: Path, ref: str) -> str:
    if ref == "main":
        candidates = [
            "refs/remotes/origin/main^{commit}",
            "refs/heads/main^{commit}",
            "main^{commit}",
        ]
    else:
        candidates = [f"{ref}^{{commit}}"]

    errors: List[str] = []
    for candidate in candidates:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--verify", candidate],
            check=False,
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0:
            return proc.stdout.strip()
        errors.append(proc.stderr.strip() or candidate)

    raise FomStop("GIT_REF_UNRESOLVED:" + ref + ":" + " | ".join(errors))


def path_inside(root: Path, candidate: Path, stop_reason: str) -> Path:
    root = root.resolve()
    candidate = candidate.resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise FomStop(stop_reason) from exc
    return candidate


def resolve_output_root(repo_root: Path, output_root: Path) -> Path:
    repo_root = repo_root.resolve()
    evidence_root = path_inside(
        repo_root, repo_root / "evidence", "EVIDENCE_ROOT_ESCAPES_REPO"
    )
    candidate = output_root if output_root.is_absolute() else repo_root / output_root
    candidate = candidate.resolve()
    try:
        candidate.relative_to(evidence_root)
    except ValueError as exc:
        raise FomStop("OUTPUT_ROOT_OUTSIDE_REPO_EVIDENCE") from exc
    return candidate


def relative_repo_path(repo_root: Path, path: Path, stop_reason: str) -> str:
    path = path_inside(repo_root, path, stop_reason)
    return path.relative_to(repo_root.resolve()).as_posix()


def committed_blob_sha(repo_root: Path, head_sha: str, relative_path: str) -> str:
    return git(repo_root, "rev-parse", f"{head_sha}:{relative_path}")


def execution_material_entry(
    repo_root: Path, head_sha: str, path: Path, stop_reason: str
) -> Dict[str, str]:
    relative_path = relative_repo_path(repo_root, path, stop_reason)
    actual_blob = git_blob_sha(path)
    tracked_blob = committed_blob_sha(repo_root, head_sha, relative_path)
    if actual_blob != tracked_blob:
        raise FomStop("EXECUTION_MATERIAL_DIFFERS_FROM_HEAD:" + relative_path)
    return {
        "path": relative_path,
        "git_blob_sha": tracked_blob,
        "file_sha256": sha256_file(path),
    }


def validate_mission(mission: Dict[str, Any], observed_base_sha: str) -> None:
    missing = sorted(REQUIRED_MISSION_FIELDS - mission.keys())
    if missing:
        raise FomStop("MISSION_INVALID_MISSING_FIELDS:" + ",".join(missing))

    if mission["contract_version"] != FOM_VERSION:
        raise FomStop("MISSION_INVALID_CONTRACT_VERSION")
    if mission["issue"] != 5:
        raise FomStop("MISSION_OUT_OF_SCOPE_ISSUE")
    if mission["base_ref"] != "main":
        raise FomStop("REFERENCE_MISSION_BASE_REF_NOT_MAIN")
    if mission["reversibility"] != "FULL":
        raise FomStop("REFERENCE_MISSION_NOT_FULLY_REVERSIBLE")
    if mission["input_path"] not in mission["sources_required"]:
        raise FomStop("INPUT_NOT_DECLARED_AS_REQUIRED_SOURCE")
    if mission["base_sha_policy"] == "PINNED" and mission["base_sha"] != observed_base_sha:
        raise FomStop(
            f"STALE_BASE_SHA:mission={mission['base_sha']}:observed={observed_base_sha}"
        )
    if mission["base_sha_policy"] == "CURRENT_MAIN" and mission["base_sha"] != "CURRENT_MAIN":
        raise FomStop("CURRENT_MAIN_BASE_POLICY_REQUIRES_EXPLICIT_SENTINEL")
    if mission["base_sha_policy"] not in {"PINNED", "CURRENT_MAIN"}:
        raise FomStop("UNKNOWN_BASE_SHA_POLICY")
    if mission["risk_level"] != "LOW":
        raise FomStop("RISK_NOT_ALLOWED_FOR_REFERENCE_MISSION")

    denied = {str(x).upper() for x in mission["permissions_denied"]}
    allowed = {str(x).upper() for x in mission["permissions_allowed"]}

    blocked_requested = allowed & BLOCKED_PERMISSION_TOKENS
    if blocked_requested:
        raise FomStop(
            "FORBIDDEN_PERMISSION_REQUEST:" + ",".join(sorted(blocked_requested))
        )

    missing_required = sorted(REQUIRED_REFERENCE_PERMISSIONS - allowed)
    if missing_required:
        raise FomStop(
            "MISSING_REQUIRED_REFERENCE_PERMISSION:" + ",".join(missing_required)
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

    candidates = sorted(EXECUTORS) if requested == "AUTO" else [requested]

    for candidate in candidates:
        spec = EXECUTORS.get(candidate)
        if not spec:
            continue
        if required_caps.issubset(spec["capabilities"]) and required_permissions.issubset(
            spec["permissions"]
        ):
            return candidate

    raise FomStop("NO_ELIGIBLE_EXECUTOR")


def deterministic_run_id(
    mission: Dict[str, Any], input_hash: str, observed_base_sha: str, material_fingerprint: str
) -> str:
    identity = "|".join(
        [
            mission["mission_id"],
            mission["idempotency_key"],
            mission["base_sha"],
            mission["base_sha_policy"],
            observed_base_sha,
            input_hash,
            material_fingerprint,
            FOM_VERSION,
        ]
    )
    return "fom-" + sha256_text(identity)[:20]


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def evidence_hashes(directory: Path) -> Dict[str, str]:
    names = [
        "manifest.json", "trace.jsonl", "result.json",
        "handoff.json", "provenance.json",
    ]
    return {name: sha256_file(directory / name) for name in names}


def verify_existing_evidence(
    final_dir: Path,
    mission: Dict[str, Any],
    run_id: str,
    input_file_hash: str,
    output_hash: str,
) -> None:
    missing = sorted(
        name for name in REQUIRED_EVIDENCE_FILES if not (final_dir / name).is_file()
    )
    if missing:
        raise FomStop("INCOMPLETE_EVIDENCE_PACK:" + ",".join(missing))

    summary = load_json(final_dir / "run_summary.json")
    result = load_json(final_dir / "result.json")
    manifest = load_json(final_dir / "manifest.json")
    handoff = load_json(final_dir / "handoff.json")

    recorded_hashes = summary.get("evidence_sha256")
    if not isinstance(recorded_hashes, dict):
        raise FomStop("EVIDENCE_INTEGRITY_METADATA_MISSING")

    actual_hashes = evidence_hashes(final_dir)
    mismatched = sorted(
        name
        for name, actual in actual_hashes.items()
        if recorded_hashes.get(name) != actual
    )
    if mismatched:
        raise FomStop("EVIDENCE_INTEGRITY_MISMATCH:" + ",".join(mismatched))

    if not (
        summary.get("mission_id") == mission["mission_id"]
        and summary.get("input_file_sha256") == input_file_hash
        and summary.get("result_sha256") == output_hash
        and summary.get("status") == "SUCCESS"
        and result.get("run_id") == run_id
        and result.get("verified") is True
        and manifest.get("run_id") == run_id
        and handoff.get("run_id") == run_id
        and handoff.get("status") == "SUCCESS"
    ):
        raise FomStop("IDEMPOTENCY_CONFLICT_EXISTING_OUTPUT")


def run_fom(
    mission_path: Path,
    repo_root: Path,
    output_root: Path,
    simulate_failure_before_commit: bool = False,
) -> Dict[str, Any]:
    repo_root = repo_root.resolve()
    mission_path = mission_path if mission_path.is_absolute() else repo_root / mission_path
    mission_path = path_inside(repo_root, mission_path, "MISSION_PATH_ESCAPES_REPO")
    output_root = resolve_output_root(repo_root, output_root)

    mission = load_json(mission_path)
    observed_base_sha = resolve_git_ref(repo_root, mission.get("base_ref", "main"))
    runtime_head_sha = resolve_git_ref(repo_root, "HEAD")
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
        runtime_head_sha=runtime_head_sha,
        observation="git rev-parse",
    )

    executor = route_executor(mission)
    event(
        "capability_routing",
        "PASS",
        requested_executor=mission["requested_executor"],
        actual_executor=executor,
    )

    input_path = path_inside(
        repo_root,
        repo_root / mission["input_path"],
        "INPUT_PATH_ESCAPES_REPO",
    )
    if not input_path.is_file():
        raise FomStop("INPUT_FIXTURE_NOT_FOUND")

    raw_input = load_json(input_path)
    canonical = canonical_json(raw_input)
    output_hash = sha256_text(canonical)
    input_file_hash = sha256_file(input_path)

    effective_runner_path = Path(__file__).resolve()
    material = {
        "runner": execution_material_entry(
            repo_root, runtime_head_sha, effective_runner_path, "RUNNER_PATH_ESCAPES_REPO"
        ),
        "mission": execution_material_entry(
            repo_root, runtime_head_sha, mission_path, "MISSION_PATH_ESCAPES_REPO"
        ),
        "fixture": execution_material_entry(
            repo_root, runtime_head_sha, input_path, "INPUT_PATH_ESCAPES_REPO"
        ),
    }
    material_fingerprint = sha256_text(canonical_json({
        "runtime_head_sha": runtime_head_sha,
        "observed_base_sha": observed_base_sha,
        "execution_material": material,
    }))

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

    run_id = deterministic_run_id(mission, input_file_hash, observed_base_sha, material_fingerprint)
    final_dir = output_root / run_id
    summary_path = final_dir / "run_summary.json"

    if summary_path.is_file():
        verify_existing_evidence(
            final_dir, mission, run_id, input_file_hash, output_hash
        )
        return {
            "status": "IDEMPOTENT_REPLAY",
            "run_id": run_id,
            "output_dir": str(final_dir),
            "result_sha256": output_hash,
        }

    if final_dir.exists():
        raise FomStop("PARTIAL_OUTPUT_EXISTS_STOP")

    output_root.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(
        tempfile.mkdtemp(prefix=f".{run_id}.tmp-", dir=str(output_root))
    )

    try:
        event("trace_evidence", "PASS", output_staging=temp_dir.name)

        manifest = {
            "fom_version": FOM_VERSION,
            "mission_id": mission["mission_id"],
            "issue": mission["issue"],
            "run_id": run_id,
            "base_ref": mission["base_ref"],
            "base_sha_policy": mission["base_sha_policy"],
            "declared_base_sha": mission["base_sha"],
            "base_sha": observed_base_sha,
            "runtime_head_sha": runtime_head_sha,
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

        provenance = {
            "mission_id": mission["mission_id"],
            "run_id": run_id,
            "base_sha_observed": observed_base_sha,
            "base_sha_policy": mission["base_sha_policy"],
            "declared_base_sha": mission["base_sha"],
            "runtime_head_sha": runtime_head_sha,
            "execution_material_fingerprint": material_fingerprint,
            "execution_material": material,
            "generated_by_runtime": True,
            "evidence_strength": "EXECUTION_REPRODUCED",
        }
        write_json(temp_dir / "provenance.json", provenance)

        summary = {
            "status": "SUCCESS",
            "mission_id": mission["mission_id"],
            "run_id": run_id,
            "input_file_sha256": input_file_hash,
            "result_sha256": output_hash,
            "finished_at": utc_now(),
            "evidence_sha256": evidence_hashes(temp_dir),
            "artifacts": [
                "manifest.json", "trace.jsonl", "result.json",
                "handoff.json", "provenance.json", "run_summary.json",
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
    parser = argparse.ArgumentParser(description="Run hardened FOM v0 reference mission.")
    parser.add_argument("--mission", required=True, type=Path)
    parser.add_argument("--repo-root", default=Path("."), type=Path)
    parser.add_argument("--output-root", default=Path("evidence/fom"), type=Path)
    parser.add_argument("--simulate-failure-before-commit", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = run_fom(
            mission_path=args.mission,
            repo_root=args.repo_root,
            output_root=args.output_root,
            simulate_failure_before_commit=args.simulate_failure_before_commit,
        )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except FomStop as exc:
        print(json.dumps({"status": "STOP", "reason": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
