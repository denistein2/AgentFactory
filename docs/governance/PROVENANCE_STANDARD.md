# PROVENANCE_STANDARD — Proveniência mínima de claims materiais

**Missão de origem:** GOVERNANCE-RESET-FACTORY-001  
**Issue:** #3  
**Status:** candidato canônico até merge humano

## Princípio

Quanto maior a autonomia, maior deve ser a capacidade de responder: **quem disse, com base em quê, quando, sobre qual ref, quem verificou e o que isso não prova**.

Não é necessário instrumentar cada frase. O padrão se aplica a claims que mudam decisão, Gate, execução, segurança, lifecycle, identidade de artefato ou current-state.

## Campos mínimos

```yaml
source:
source_ref_or_hash:
source_created_at: UNKNOWN|<timestamp>
source_updated_at: UNKNOWN|<timestamp>
fact_observed_at:
recorded_at:
last_verified_at:
observer:
verifier:
mission_id:
issue:
base_ref:
base_sha:
evidence_strength:
does_not_prove:
```

Campos de execução, quando houver:

```yaml
actor_type:
provider:
product_agent:
model_reported:
role:
session_id:
run_id:
started_at:
finished_at:
```

## Valores desconhecidos

`UNKNOWN` = informação não disponível.  
`UNVERIFIED` = informação declarada, mas não verificada pela cadeia atual.

Nunca inferir modelo histórico, executor, autoria, timestamp ou hash ausente.

## Força da evidência

Usar apenas o nível efetivamente demonstrado:

- `DOCUMENT_COHERENCE` — documentos/fontes entregues são coerentes entre si.
- `EXECUTION_REPRODUCED` — a condição executável foi reproduzida e evidenciada.
- `CODE_AUDITED` — código relevante foi revisado/auditado no escopo declarado.
- `UNVERIFIED` — claim ainda não possui evidência suficiente.

Esses níveis não são intercambiáveis nem cumulativos automaticamente.

## Lifecycle mínimo

- `CURRENT` — vigente no escopo/ref e verificado.
- `ACTIVE_MISSION` — material de missão em andamento; não é automaticamente governança da `main`.
- `HISTORICAL` — preservado para reconstrução temporal.
- `SUPERSEDED` — substituído; sucessor deve ser apontado.
- `IMPORTED_UNAUDITED` — sob custódia, sem auditoria integral/autorização implícita.
- `EXTERNAL_CONTEXT` — Drive/ERP/outra origem a reconciliar; não promove claim ao repo sozinho.

## Regra de freshness

Um PASS ou claim histórico continua verdadeiro apenas para o estado/ref em que foi demonstrado. Mudança material posterior pode torná-lo `STALE` para o presente sem apagar sua validade histórica.

## `does_not_prove`

Todo claim material deve registrar o principal limite de interpretação. Exemplos:

- hash confere **não prova** segurança do conteúdo;
- documento coerente **não prova** execução;
- execução histórica **não prova** estado atual;
- PR Ready **não prova** merge;
- arquivo presente **não prova** autoridade.
