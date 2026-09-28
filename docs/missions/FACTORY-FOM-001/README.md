# FACTORY-FOM-001 — Reference Mission V0

## State

`HARDENING_AD`

Issue: #5  
Base main observed for this hardening mission: `76a8e408de092163c61dfa6e7b8304a8dcedba0e`

## Objective

Prove the smallest Agent Factory loop from Mission intake to evidence-backed session close without production, network, live database, secrets, deploy or merge.

## Reference operation

Synthetic JSON fixture → canonical JSON → SHA-256 → expected hash verification → atomic evidence pack.

Expected result SHA-256:

`dc5833c97d2d9c6172451bde78b37f95d0e2002e1b965e60f4e308710d38c0f2`

## Commands

```bash
python -m unittest tools/fom/test_fom_v0.py -v

python tools/fom/run_fom_v0.py \
  --mission docs/missions/FACTORY-FOM-001/MISSION_REFERENCE_SYNTHETIC.json \
  --repo-root . \
  --output-root evidence/fom
```

The caller no longer injects `--observed-base-sha`. The runner resolves `main` directly from Git.

## Hardening A + D

The post-merge adversarial audit found six gaps. This hardening addresses them:

- live main is resolved by the runtime;
- `WRITE_EVIDENCE_LOCAL` is mandatory because the runtime writes evidence;
- output root is constrained under `repo/evidence`;
- replay hashes trace/handoff/provenance as part of evidence integrity;
- runtime emits runner/Mission/fixture execution provenance;
- dedicated GitHub Actions workflow runs unit tests + Reference Mission + replay and uploads CI evidence.

## STOP tests

The unit suite covers:

- live main movement → stale-base STOP;
- forbidden permission → STOP;
- missing required write permission → STOP;
- output root escape → STOP;
- undeclared source → STOP;
- incomplete evidence pack → STOP;
- trace tamper → STOP;
- handoff tamper → STOP;
- controlled failure before atomic commit → zero final side effects;
- exact replay → `IDEMPOTENT_REPLAY`;
- runtime provenance emitted for runner/Mission/fixture.

## CI

Workflow:

`.github/workflows/fom-v0.yml`

CI must show the FOM unit suite and Reference Mission passing before this hardening is ready for Human Gate.

## Historical V0 evidence

The first reproduced V0 run remains historical evidence:

`evidence/fom/fom-bac732f1891f1dc09ce7/`

The hardening does not rewrite that historical run.

## Does not prove

- generic tool registry from #8;
- DB Twin;
- browser automation;
- multi-model capability routing;
- production safety;
- ERP readiness.
