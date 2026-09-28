---
session_id: 2026-09-27-FACTORY-FOM-001-HARDENING-AD
mission_id: FACTORY-FOM-001-HARDENING-AD
issue: 5
status: CI_PROVEN_AWAITING_HUMAN_GATE
base_ref: main
base_sha: 76a8e408de092163c61dfa6e7b8304a8dcedba0e
human_decision: ACTION_DECK_A_PLUS_D
---

# SESSION — FOM-001 Hardening A + D

## Trigger

Denis selected Action Deck **A + D** after the post-merge adversarial audit of PR #15.

## A — minimal hardening

Implemented scope:

1. FOM contract is 0.1.2; current-state bootstrap resolves repository-observed `main` from local Git refs; no network fetch is performed;
2. caller-supplied observed SHA was removed from the CLI/runtime contract;
3. runtime requires `WRITE_EVIDENCE_LOCAL` before writing evidence;
4. output root is constrained under `repo/evidence`;
5. replay validates integrity hashes for manifest, trace, result, handoff and provenance;
6. runtime validates the actual executing runner, Mission and fixture against runtime HEAD before replay, with no caller-supplied runner path, and fingerprints execution material + observed base + runtime HEAD into the run identity;
7. historical pinned and reusable `CURRENT_MAIN` Reference Mission semantics are explicit; stale-base checks remain enabled for pinned Missions.

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

Dedicated CI was proven for the prior PR head. The corrective hardening in PR #16 must pass CI on its final head before presentation to Human Gate. Merge and Issue closure remain unperformed and human-controlled.
