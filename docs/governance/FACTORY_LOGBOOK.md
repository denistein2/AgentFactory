# FACTORY_LOGBOOK — Current-state index + timeline

**Função:** reconstruir estado sem transformar histórico em verdade atual.  
**Status:** CANONICAL em `main` desde a PR #4.

## Snapshot externo revalidado

```yaml
last_verified_at: 2026-09-26T08:55:00-03:00
verified_ref: main
verified_sha: 8131daedf471f4c34648f5c3a3be9973ad5d9cf2
observer: ChatGPT / OpenAI / GPT-5.6 Sol
verifier: GitHub connector live readback
issue_3: CLOSED
pr_4: MERGED
pr_12: OPEN_RECONCILIATION
```

> O SHA acima é a baseline viva observada **antes do merge eventual da PR #12**. Se este arquivo for lido em uma ref posterior, a própria ref Git observada prevalece e este snapshot vira baseline histórica até novo readback.

### Estado

- `main` observada em `8131daedf471f4c34648f5c3a3be9973ad5d9cf2`.
- PR #4 foi mergeada em 2026-09-26; a governança do reset está presente em `main`.
- Issue #3 (`GOVERNANCE-RESET-FACTORY-001`) está `CLOSED / completed`.
- PR #12 (`AgentSpec`) está em reconciliação contra a main pós-PR #4; merge permanece exclusivamente humano.
- DBTWIN-002 continua `Gate 02-A NÃO APROVADO`; a reconciliação de AgentSpec não inicia Fase 02 nem runtime.

## Resolução de current-state

Para localização/lifecycle/estado operacional:

```text
ref Git observada
→ path real na ref
→ lifecycle explícito
→ last_verified_at/proveniência
→ documento de missão
→ handoff/histórico
```

Para regra normativa, usar a precedência de `GOVERNANCE.md`.

## Claims stale identificados e tratamento

| Fonte | Claim antigo | Estado | Tratamento |
|---|---|---|---|
| README pré-PR #4 | `BLOCKED_BASE_BRANCH`, `main` ausente | SUPERSEDED | substituído pela resolução de current-state da PR #4 |
| snapshot da PR #4 antes do merge | Issue #3/PR #4 ainda pendentes | HISTORICAL após 2026-09-26 | revalidado neste logbook |
| handoffs/Decision Pages pré-merge | PR #4 aberta/draft | HISTORICAL | preservar; não usar como current-state |
| PR #12 sobre base `918387...` | compatível com main antiga | STALE como base de integração | reconciliar sobre a main pós-PR #4 |

## Timeline mínima

### 2026-08-02 — ORG-001/R5
Baseline organizacional, custódia v0.2, Draft PR #1 e registro de sessão.

### 2026-08-03 — merge PR #1
`main` passa a existir com a fundação organizacional.

### 2026-08-20 — field report ERP
ERP revela a classe de falha de execução contra documentação stale/ambígua. Issue #2 aberta em read-only.

### 2026-08-21 — auditoria #2
Dois P0 de current-state confirmados. Issue #2 encerrada; objeto reprovado para expansão de autonomia.

### 2026-08-21 — Gate #3 / PR #4
Denis aprova correção mínima em branch/PR, sem autorizar merge automático, DBTWIN, Docker, Supabase, produção ou dados reais.

### 2026-09-26 — merge PR #4 / close Issue #3
PR #4 mergeada por Human Gate. `main` observada em `8131daedf471f4c34648f5c3a3be9973ad5d9cf2`; Issue #3 encerrada.

### 2026-09-26 — reconciliação PR #12
A branch AgentSpec é preservada antes da reconciliação e reaplicada sobre a main pós-PR #4. A reconciliação deve preservar current-state/provenance/routing/lifecycle e corrigir a transição AGASALHO → AgentSpec sem alegar implementação de runtime.

## Regra de atualização

Nova sessão só altera este snapshot quando revalida a fonte/ref. Não copiar “estado atual” de handoff antigo sem observação presente.
