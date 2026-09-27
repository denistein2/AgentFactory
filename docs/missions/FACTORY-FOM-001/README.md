# FACTORY-FOM-001 — Reference Mission V0

## State

`ACTIVE_MISSION`

Issue: #5  
Base observed before execution: `758478192a79728a653736e48fa35078cce0d6f4`

## Objective

Prove the smallest Agent Factory loop from Mission intake to evidence-backed session close without production, network, live database, secrets, deploy or merge.

## Reference operation

Synthetic JSON fixture → canonical JSON → SHA-256 → expected hash verification → atomic evidence pack.

Expected result SHA-256:

`dc5833c97d2d9c6172451bde78b37f95d0e2002e1b965e60f4e308710d38c0f2`

## Commands

```bash
python -m unittest tools/fom/test_fom_v0.py

python tools/fom/run_fom_v0.py \
  --mission docs/missions/FACTORY-FOM-001/MISSION_REFERENCE_SYNTHETIC.json \
  --repo-root . \
  --output-root evidence/fom \
  --observed-base-sha 758478192a79728a653736e48fa35078cce0d6f4
```

## STOP tests

The unit suite proves:
- stale base SHA stops;
- forbidden permission stops;
- simulated failure before atomic commit leaves no final evidence directory;
- retry after failure succeeds;
- exact replay returns `IDEMPOTENT_REPLAY`.

## Evidence from first reproduced local run

Run ID:

`fom-bac732f1891f1dc09ce7`

Verdict:

`REFERENCE_MISSION_E2E_REPRODUCED`

Evidence path:

`evidence/fom/fom-bac732f1891f1dc09ce7/`

## Does not prove

- generic tool registry from #8;
- DB Twin;
- browser automation;
- multi-model capability routing;
- production safety;
- ERP readiness.
