---
session_id: 2026-09-27-FACTORY-FOM-001-01
mission_id: FACTORY-FOM-001
issue: 5
status: REFERENCE_MISSION_REPRODUCED_LOCAL
base_ref: main
base_sha: 758478192a79728a653736e48fa35078cce0d6f4
actor_type: AI_AGENT
requested_executor: Jarvis / ChatGPT
actual_executor: Jarvis / ChatGPT + builtin:canonical-json-sha256
provider: OpenAI
model_reported: GPT-5.6 Sol
role: FOM designer + scoped executor
evidence_strength: EXECUTION_REPRODUCED
---

# SESSION — FACTORY-FOM-001 — 2026-09-27

## 1. Trigger

Human selected Action Deck:

`A — HOT PATH: entrar na Issue #5 e iniciar o FOM`.

## 2. Brain Preflight

Brain/Drive read first.

Divergence found:
- Brain still reflected PR #14 as pre-merge.
- GitHub live showed PR #14 merged.
- live main observed: `758478192a79728a653736e48fa35078cce0d6f4`.

By Brain Contract, live Git won for current-state.

## 3. AgentSpec precondition

AGENTSPEC-001 requires a compatible executor spec before a material mission.

No executor-specific Jarvis spec was found in the repository.

P0/read-only bootstrap was used to define:

`docs/agents/JARVIS/AGENTSPEC_JARVIS_001.md`

Result:

`AGENT_READY_WITH_SCOPED_ALLOWLIST`

The scope is only FACTORY-FOM-001. Merge, deploy, live DB, secrets and production remain P3/P4.

## 4. FOM definition

Candidate expansion:

**FOM = Fluxo Operacional Mínimo**

Reason:
Issue #5 itself records the historical meaning as “fluxo operacional mínimo/core”.

Canonical promotion still depends on human merge.

Flow implemented:

`Mission Intake → Current-State Bootstrap → Capability Routing → Executor/Tool Use → Trace/Evidence → Verification/Gate → Artifact → Handoff/Close`

## 5. Reference Mission

Synthetic/reversible mission:

- input: versioned JSON fixture;
- operation: canonical JSON + SHA-256;
- expected outcome: fixed SHA-256;
- executor routing: AUTO → built-in executor;
- no network;
- no live DB;
- no secrets;
- no deploy;
- no merge;
- no production.

## 6. Local execution evidence

Unit tests:

`6/6 PASS`

Covered:
- success + idempotent replay;
- controlled failure with no final side effect;
- forbidden permission STOP;
- stale base STOP.

Controlled failure exercise:

`STOP: SIMULATED_FAILURE_BEFORE_ATOMIC_COMMIT`

Final evidence directories after failure:

`0`

Successful run:

- run_id: `fom-bac732f1891f1dc09ce7`
- result SHA-256: `dc5833c97d2d9c6172451bde78b37f95d0e2002e1b965e60f4e308710d38c0f2`
- status: `SUCCESS`

Second identical run:

`IDEMPOTENT_REPLAY`

## 7. Evidence Pack

Recoverable evidence is persisted under:

`evidence/fom/fom-bac732f1891f1dc09ce7/`

Files:
- manifest.json
- trace.jsonl
- result.json
- handoff.json
- run_summary.json

## 8. Runtime gap found

This FOM V0 does **not** need the full #6–#10 stack to prove the first circuit.

The first concrete gap discovered by governance was executor-specific AgentSpec readiness, solved narrowly for this mission.

Generic Tool Contracts (#8), broader tracing (#7), eval harness (#6), durable context (#9) and evidence-based multi-executor router (#10) remain post-FOM candidates until a real bottleneck requires them.

## 9. Next verification

Push branch → Draft PR → GitHub CI:
- existing `session-pr`;
- new `fom-v0` workflow.

Do not claim CI PASS until observed.

## 10. Does not prove

This local reproduction does not prove:
- CI reproduction;
- production readiness;
- DB Twin;
- browser smoke tests;
- generic tool registry;
- ERP Food Control correctness.

## 11. Human Gate

Merge remains exclusively human.
