# AGENTSPEC-JARVIS-001 — Jarvis / ChatGPT scoped executor

> Protocol: AGENTSPEC-001
> AgentSpec ID: AGENTSPEC-JARVIS-001
> Version: v0.1
> Validated at: 2026-09-27
> Human gate owner: Denis Stein
> Status: AGENT_READY_WITH_SCOPED_ALLOWLIST

## 1. Identity and purpose

- Agent/executor: Jarvis / ChatGPT
- Provider: OpenAI
- Model reported in this session: GPT-5.6 Sol
- Primary role: project orchestration, readback, governance-safe GitHub/Drive execution
- Repository: `denistein2/AgentFactory`
- Mission pattern: branch-scoped P2 writes; main merge human-only

Explicit non-goals:
- production deployment;
- live DB mutation;
- secret handling;
- autonomous main merge;
- destructive cleanup.

## 2. Surface inventory

| Surface | Access | Class | Evidence |
|---|---|---|---|
| GitHub read | YES | P0 | live Issue/PR/tree readback |
| GitHub branch create/write | YES | P2 | prior PR #14 + current mission branch |
| GitHub Draft PR | YES | P2 | connector capability |
| GitHub merge | HUMAN ONLY | P3 | governance |
| Google Drive read | YES | P0 | Brain preflight |
| Google Drive scoped write | YES | P2 | Brain/project sync history |
| Local Python validation | YES | P1 | FOM V0 test execution |
| Live DB | NO | P4 for this mission | explicitly denied |
| Deploy / production | NO | P4 | explicitly denied |
| Secrets | NO | P4 | explicitly denied |

## 3. Scoped permissions for FACTORY-FOM-001

P0:
- read Brain, repo, Issue #5, governance, AgentSpec, CI/checks.

P1:
- create disposable local test directories;
- execute Python standard-library tests;
- delete only disposable test staging created by this mission.

P2:
- write files only to `session/2026-09-27/fom-001`;
- commit/push mission artifacts;
- open/update Draft PR;
- checkpoint Issue #5.

P3 STOP:
- merge;
- write main;
- live DB;
- deploy;
- secrets;
- production;
- destructive external action.

## 4. Calibration evidence

- repository identity: PASS
- GitHub read: PASS
- Drive read: PASS
- branch-scoped write: authorized by selected Action Deck A
- local validation: exercised by FOM tests
- correct stop before P3: merge remains human

## 5. Known limitations

- This AgentSpec does not prove generic tool contracts from Issue #8.
- Browser automation is not part of this FOM V0.
- Database access is explicitly unavailable for this mission.

## 6. Final readiness

`AGENT_READY_WITH_SCOPED_ALLOWLIST`

Scope: FACTORY-FOM-001 only.
