# FACTORY_LOGBOOK — Current-state index + timeline

**Função:** reconstruir estado sem transformar histórico em verdade atual.
**Status:** CANONICAL em `main` desde a PR #4.

## Snapshot externo revalidado

```yaml
last_verified_at: 2026-09-27T08:48:00-03:00
verified_ref: main
verified_sha: e5ac0c0a8c84583b072b25df6c553189fdda782d
observer: ChatGPT / OpenAI / GPT-5.6 Sol
verifier: GitHub connector live readback
issue_3: CLOSED
pr_4: MERGED
pr_12: MERGED
agentspec: CURRENT_IN_MAIN
next_doc_sync: issue_11
next_runtime_axis: issue_5
```

### Estado

- `main` observada em `e5ac0c0a8c84583b072b25df6c553189fdda782d`.
- PR #4 mergeada; Issue #3 encerrada.
- PR #12 mergeada em 2026-09-27; AgentSpec agora existe em `main`.
- Issue #11 vira sincronização documental mínima de current-state/roadmap.
- Issue #5 vira o próximo eixo de produto/runtime: definir e provar o FOM.
- Schema Context Pack V0 permanece `WORKING_DRAFT` e é componente candidato do bootstrap/contexto do FOM.
- DBTWIN-002 continua com Gate 02-A não aprovado; nenhum twin/container foi executado por este sync.


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

### 2026-09-27 — merge PR #12 / AgentSpec em main
PR #12 mergeada por Human Gate. `main` observada em `e5ac0c0a8c84583b072b25df6c553189fdda782d`. AgentSpec deixa de ser candidato e passa a contrato vigente em `main`.

### 2026-09-27 — retorno ao produto / FOM
Decisão humana: a Agent Factory deve reduzir o ciclo de desenvolvimento e executar trabalho repetitivo com segurança, sem virar laboratório infinito.

Direções:
- banco vivo não é ambiente padrão de tentativa/erro;
- DB Twin/ambiente efêmero é a direção de segurança para missões sensíveis a banco;
- criar ambiente → executar → coletar evidência → destruir ambiente é o padrão desejado;
- Schema Context Pack V0 serve o bootstrap/contexto do FOM;
- Brain guarda significado e ponte; schema técnico real permanece em fonte viva;
- produto de cliente é caso core de maturidade;
- arqueologia local é higiene de fundação, não novo projeto;
- LeadGen/Laia ficam fora do foco imediato.

## Regra de atualização

Nova sessão só altera este snapshot quando revalida a fonte/ref. Não copiar “estado atual” de handoff antigo sem observação presente.
