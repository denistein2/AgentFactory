---
session_id: 2026-09-27-FACTORY-FOM-001-HARDENING-AD
mission_id: FACTORY-FOM-001-HARDENING-AD
issue: 5
status: IMPLEMENTED_AWAITING_CI
base_ref: main
base_sha: 76a8e408de092163c61dfa6e7b8304a8dcedba0e
human_decision: ACTION_DECK_A_PLUS_D
---

# SESSION — FOM-001 Hardening A + D

## Trigger

Denis selected Action Deck **A + D** after the post-merge adversarial audit of PR #15.

## A — minimal hardening

Implemented scope:

1. current-state bootstrap resolves `main` from Git itself;
2. caller-supplied observed SHA was removed from the CLI/runtime contract;
3. runtime requires `WRITE_EVIDENCE_LOCAL` before writing evidence;
4. output root is constrained under `repo/evidence`;
5. replay validates integrity hashes for manifest, trace, result, handoff and provenance;
6. runtime emits provenance for runner, Mission and fixture and verifies the bytes match the runtime HEAD.

## D — GitHub-hosted CI

Added `.github/workflows/fom-v0.yml` with:

- full-history checkout;
- FOM unit suite;
- Reference Mission execution;
- idempotent replay assertion;
- uploaded evidence artifact.

## Scope boundaries

Not executed or authorized:
- DB Twin;
- live DB;
- production;
- deploy;
- secrets;
- browser smoke automation;
- #6–#10 implementation;
- merge.

## Gate

CI/readback must succeed before the branch can be presented as ready for Human Gate.
