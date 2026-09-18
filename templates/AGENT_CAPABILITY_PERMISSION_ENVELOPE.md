# AGENT CAPABILITY & PERMISSION ENVELOPE — TEMPLATE

> Derivado de: AGASALHO-001
> Agent: <NAME>
> Version: <vN>
> Calibrated at: <YYYY-MM-DD HH:MM TZ>
> Human gate owner: Denis Stein
> Status: DRAFT | AGENT_READY | AGENT_READY_WITH_SCOPED_ALLOWLIST | NOT_READY

## 1. Identity

- Agent/executor:
- Model/runtime:
- Client/CLI:
- Host/environment:
- Projects/repositories:
- Mandatory reading:
- Mission artifact pattern:

## 2. Surface inventory

| Surface | Access | Proof | Notes |
|---|---|---|---|
| Local Git | YES/NO/PARTIAL | | |
| GitHub read | YES/NO/PARTIAL | | |
| GitHub scoped write | YES/NO/PARTIAL | | |
| Google Drive read | YES/NO/PARTIAL | | |
| Google Drive scoped write | YES/NO/PARTIAL | | |
| Local filesystem | YES/NO/PARTIAL | | |
| CI/checks | YES/NO/PARTIAL | | |
| Local tests/build | YES/NO/PARTIAL | | |
| DB read-only | YES/NO/PARTIAL | | |
| DB write | YES/NO/PARTIAL | | |
| Deploy | YES/NO/PARTIAL | | |
| External config/secrets | YES/NO/PARTIAL | | |

## 3. Permission classes

### P0 — OBSERVE / READ_ONLY

List command/tool families and expected runtime prompts.

### P1 — SAFE_LOCAL / REVERSIBLE_LOCAL

List allowed local synchronization/setup actions.

### P2 — MISSION_SCOPED_WRITE

List writes the agent may perform only when the mission invokes this contract.

### P3 — HUMAN_GATE / CONSEQUENCE

List exact actions that require Denis.

### P4 — FORBIDDEN / UNAVAILABLE

List unsupported/prohibited surfaces.

## 4. Runtime allowlist behavior

- Conversation/session-scoped rules:
- Persistent/global rules:
- Known prompt patterns:
- Compound-command caveats:
- Provider-specific limitations:

## 5. Branch/worktree contract

- Canonical branch:
- Mission branch naming:
- Worktree rule:
- Restricted refspec behavior:
- Recovery from dirty/drifted main:
- Cleanup authority:

## 6. Artifact return contract

- Required report:
- Repo path:
- Commit/push authority:
- Drive daily path:
- Drive canonical path:
- Issue/PR checkpoint:
- Required provenance fields:

## 7. Calibration evidence

| Capability | Test | Result | Evidence |
|---|---|---|---|
| Repository identity | | | |
| Git read | | | |
| GitHub read | | | |
| Drive read | | | |
| Local validation | | | |
| Branch/worktree | | | |
| Scoped artifact write | | | |
| Correct stop before P3 | | | |

## 8. Known limitations / caveats

-

## 9. Change log

| Date | Version | Change | Trigger/evidence |
|---|---|---|---|
| | | | |

## 10. Final readiness

Result:

`<AGENT_READY | AGENT_READY_WITH_SCOPED_ALLOWLIST | AGENT_NOT_READY_...>`

Exact remaining blocker, if any:

`<NONE or blocker>`
