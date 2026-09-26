# MISSION_MANIFEST_STANDARD — Identidade da missão e do executor

**Missão de origem:** GOVERNANCE-RESET-FACTORY-001  
**Issue:** #3  
**Status:** candidato canônico até merge humano

## Objetivo

Impedir que uma missão futura confunda **executor solicitado**, **executor real**, **papel**, **provider/modelo**, **permissões** e **Gate**.

## Manifesto mínimo

```yaml
mission_id:
issue:
created_at:
started_at:
finished_at:
base_ref:
base_sha:
actor_type:
requested_executor:
actual_executor:
provider:
product_agent:
model_reported:
role:
session_id:
run_id:
capabilities_required: []
sources_required: []
risk_level:
reversibility:
permissions_allowed: []
permissions_denied: []
human_gate:
evidence_strength:
does_not_prove:
```

Use `UNKNOWN/UNVERIFIED` quando o runtime ou a fonte não provar o valor.

## Executor solicitado ≠ executor real

- `requested_executor`: quem/papel foi pedido pela missão.
- `actual_executor`: quem de fato executou.
- `provider`, `product_agent` e `model_reported`: somente o que o runtime/fonte atual realmente reporta.

Uma troca de executor não é erro por si só; ocultá-la é perda de proveniência.

## Permissões

A Issue/manifesto pode restringir permissões herdadas da governança. Não pode ampliá-las silenciosamente.

Ações fora da allowlist, destrutivas/irreversíveis em alvo real, merge, deploy, produção, credenciais/dado real ou expansão de escopo voltam ao Gate Humano correspondente.

## Fechamento

O manifesto pode viver no registro `SESSION_*.md` quando uma sessão = uma missão/run. Não é obrigatório duplicar arquivo se todos os campos e a proveniência estiverem preservados.
