# AGENTSPEC — TEMPLATE

> Protocol: AGENTSPEC-001
> Agent: <NAME>
> AgentSpec ID: AGENTSPEC-<AGENT>-<NNN>
> Version: <vN>
> Validated at: <YYYY-MM-DD HH:MM TZ>
> Human gate owner: Denis Stein
> Status: DRAFT | AGENT_READY | AGENT_READY_WITH_SCOPED_ALLOWLIST | NOT_READY

## 1. Identity and purpose

- Agent/executor:
- Model/runtime:
- Client/CLI:
- Host/environment:
- Primary role:
- Explicit non-goals:
- Projects/repositories:
- Mandatory reading:
- Mission artifact pattern:

## 2. Surface inventory

| Surface | Access | Permission class | Proof | Notes |
|---|---|---|---|---|
| Local Git | YES/NO/PARTIAL | | | |
| GitHub read | YES/NO/PARTIAL | | | |
| GitHub scoped write | YES/NO/PARTIAL | | | |
| Google Drive read | YES/NO/PARTIAL | | | |
| Google Drive scoped write | YES/NO/PARTIAL | | | |
| Local filesystem | YES/NO/PARTIAL | | | |
| CI/checks | YES/NO/PARTIAL | | | |
| Local tests/build | YES/NO/PARTIAL | | | |
| DB read-only | YES/NO/PARTIAL | | | |
| DB write | YES/NO/PARTIAL | | | |
| Deploy | YES/NO/PARTIAL | | | |
| External config/secrets | YES/NO/PARTIAL | | | |

## 3. Permission classes

### P0 — OBSERVE / READ_ONLY

- Allowed families:
- Expected runtime prompts:
- Evidence required:

### P1 — SAFE_LOCAL / REVERSIBLE_LOCAL

- Allowed local actions:
- Recovery/cleanup:

### P2 — MISSION_SCOPED_WRITE

- Allowed shared writes:
- Required Mission wording:
- Scope boundaries:

### P3 — HUMAN_GATE / CONSEQUENCE

- Exact Human Gate actions:
- Required decision input:
- Stop behavior:

### P4 — FORBIDDEN / UNAVAILABLE

- Unsupported/prohibited surfaces:
- Required fallback:

## 4. Runtime allowlist behavior

- Session-scoped rules:
- Persistent/global rules:
- Known prompt patterns:
- Compound-command caveats:
- Provider/runtime limitations:

## 5. Branch/worktree contract

- Canonical branch:
- Mission branch naming:
- Worktree rule:
- Restricted refspec behavior:
- Dirty/drifted main recovery:
- Cleanup authority:

## 6. Artifact return contract

- Required report:
- Repo path:
- Commit/push authority:
- Drive daily path:
- Drive canonical path:
- Issue/PR checkpoint:
- Required provenance:
- Allowed verdicts:

## 7. Human Gate map

| Gate ID | Trigger | Why human | Required options/context | Result |
|---|---|---|---|---|
| | | | | |

## 8. Calibration evidence

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

## 9. Known limitations / caveats

-

## 10. Project overlays

| Project | Overlay/restriction | Authority | Evidence |
|---|---|---|---|
| | | | |

## 11. Change log

| Date | Version | Change | Trigger/evidence |
|---|---|---|---|
| | | | |

## 12. Final readiness

Result:

`<AGENT_READY | AGENT_READY_WITH_SCOPED_ALLOWLIST | AGENT_NOT_READY_...>`

Exact remaining blocker:

`<NONE or blocker>`
