# Command Center Control Plane V1

**Status:** implementation candidate in PR #19  
**Owner:** Stein Agent Factory  
**Control Issue:** #20  
**Autonomy Audit Gate:** #17

## 1. Purpose

Transform the static Command Center into a live operational cockpit without collapsing trust boundaries.

The dashboard must answer:

- what is the current product focus;
- which tickets are on the critical path;
- what source produced each claim;
- whether GitHub, Brain and Drive are live, mirrored, stale or unavailable;
- whether Submarine mode is OFF, DRY-RUN, ARMED or RUNNING;
- what is waiting for independent audit / human review.

## 2. Non-negotiable trust boundary

The AgentFactory repository and current Vercel site are public.

Therefore **private Brain/Drive/project content must never be committed into the public repository or returned by a public endpoint**.

The architecture is intentionally split:

### Public surface

`GET /api/control-state`

Returns only sanitized operational information:

- AgentFactory public GitHub state;
- generic Food Control focus lanes;
- source health;
- Submarine mode;
- security/gate state.

It contains no private repository issue titles, Drive document names, Brain content or tokens.

### Private surface

`GET /api/private-state`

Fail-closed authentication:

`Authorization: Bearer <CONTROL_CENTER_BEARER>`

or:

`x-command-center-token: <CONTROL_CENTER_BEARER>`

If `CONTROL_CENTER_BEARER` is absent, the endpoint returns **503 LOCKED**.
If the supplied token is wrong, it returns **401 LOCKED**.

This endpoint can read private GitHub state only when `GITHUB_TOKEN` exists server-side.

## 3. Environment variables

### Required to unlock private API

- `CONTROL_CENTER_BEARER` — independent dashboard access secret.
- `GITHUB_TOKEN` — server-side GitHub token with minimum read permissions required for configured private repositories.

### Private repo list

- `CONTROL_PRIVATE_REPOS`
  - default: `denistein2/ERPFoodControl,denistein2/Stein-Brain`

### Optional Google Drive adapter

Drive remains **UNCONFIGURED** unless all required OAuth values are present:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REFRESH_TOKEN`
- `DRIVE_Q`

`DRIVE_Q` is mandatory by design so the backend does not accidentally index the entire Drive.

Example concept:

`trashed = false and name contains 'Stein'`

The V1 Drive adapter returns metadata/index information only. It does **not** publish file content.

## 4. Food Control focus

The private API knows the current ordered pipeline:

1. #66 — PDV retry/idempotency
2. #58 — cashier day boundary / Financeiro truth
3. #50 — financial event contract
4. #57 — cash/change contract
5. #56 — PDV acceptance
6. #63 — atomic order creation
7. #49 — delivery guard
8. Fiscal — #48 Track B
9. Purchases / inbound invoices — #48 Track D
10. Financeiro / Contábil after the canonical financial contract

Stock/production expansion is **DEFERRED**, not deleted.

No Granus runtime integration exists in this architecture. Granus only influenced roadmap focus.

## 5. Brain model

The first live Brain mirror is the **Stein-Brain GitHub repository state**, read through the private API.

A full semantic/content mirror is a later mission and must live behind private storage/authentication. It must never be generated as a public JSON artifact.

## 6. Drive model

V1 supports a private metadata index behind OAuth.

Future versions may add:

- selected-folder mirror;
- provenance hashes;
- reconciliation status;
- content extraction;
- change cursors / incremental sync.

Any content mirror must remain private.

## 7. Submarine mode

Canonical manifest:

`control/submarine-config.json`

V1 mode is **OFF** and `writeAuthority=false`.

Prepared pipeline:

`ticket → mission envelope → executor → tests → adversarial audit → evidence → Draft PR → Human Review`

Activation is blocked until #17 proves the governed-autonomy contract.

Permanent Human Gates include:

- merge;
- deploy;
- production mutation;
- live DB mutation;
- secrets;
- material scope expansion.

## 8. Claude Code / independent auditor

The Command Center may show an auditor slot, but V1 must report:

`PLANNED_NOT_CONNECTED`

until a real adapter, credentials, execution contract and evidence flow exist.

The external auditor is intended for adversarial review:

- code defects;
- security failures;
- production-safety failures;
- stale evidence;
- bypasses;
- false guarantees.

## 9. UI refresh model

The browser polls the public API and offers manual refresh.

Private telemetry is never fetched unless the operator explicitly unlocks private mode with the control token.

The UI must degrade safely:

- backend unavailable → static snapshot remains visible;
- public API degraded → provenance badge shows DEGRADED;
- private token missing → LOCKED;
- provider credentials missing → UNCONFIGURED;
- stale data → timestamp remains visible and must not be presented as live.

## 10. V1 security invariants

1. No private data in the public bundle.
2. No client-side GitHub/Google secret.
3. No write endpoint.
4. Private endpoint fails closed.
5. No Submarine write authority.
6. No autonomous merge/deploy/prod/DB/secrets.
7. Source status must distinguish LIVE from MIRROR/STALE/LOCKED.
8. Evidence > claim.

## 11. Next gate

After this V1 is reviewed:

1. merge responsive/control UI via Human Gate;
2. configure private server-side secrets in Vercel;
3. verify private API with read-only credentials;
4. add a private storage layer if full Brain/Drive content mirror is needed;
5. complete #17 adversarial audit;
6. only then design Submarine write capabilities.
