# FACTORY_LOGBOOK — Current-state index + timeline

**Função:** reconstruir estado sem transformar histórico em verdade atual.  
**Status:** candidato canônico até merge humano do Draft PR #4.

## Snapshot verificado

```yaml
last_verified_at: 2026-08-21T15:23:47-03:00
verified_ref: main
verified_sha: 918387376620f6985baeb14965c7245131114b49
observer: ChatGPT / OpenAI / GPT-5.6 Sol
verifier: same-session GitHub connector readback
issue: 3
draft_pr: 4
```

### Estado

- `main` existe em `918387376620f6985baeb14965c7245131114b49`.
- ORG-001 foi mergeado via PR #1 em 2026-08-03.
- Issue #2 (`GOVERNANCE-FIELD-REPORT-001`) terminou `COMPLETED`; o objeto auditado foi `REPROVADO` para expansão de autonomia.
- Issue #3 (`GOVERNANCE-RESET-FACTORY-001`) recebeu Gate Humano para correção mínima.
- Draft PR #4 está aberto na branch `session/2026-08-21/governance-reset-factory-001`; **a correção ainda não é canônica na main**.
- DBTWIN-002 continua `Gate 02-A NÃO APROVADO`; o reset de governança não inicia Fase 02.

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

## Claims stale identificados na base auditada

| Fonte | Claim antigo | Estado em 2026-08-21 | Tratamento no Draft PR #4 |
|---|---|---|---|
| `README.md` | `BLOCKED_BASE_BRANCH`, `main` ausente | falso | corrigido |
| `docs/missions/AGENT-FACTORY-DBTWIN-002/ESTRUTURA_CANONICA.md` | “única árvore válida” com paths `governance/`/`missions/` na raiz | não corresponde à árvore real | corrigido para árvore mission-local observada |
| `docs/missions/AGENT-FACTORY-DBTWIN-002/PLAN_DBTWIN_002.md` e `VERSIONAMENTO_GIT.md` | exemplos/path textuais derivados da árvore antiga | históricos de planejamento; não resolvem current-state global | subordinados ao índice atual + ESTRUTURA corrigida; conteúdo técnico não reaberto |

## Timeline mínima

### 2026-08-02 — ORG-001/R5
Baseline organizacional, custódia v0.2, Draft PR #1 e registro de sessão. Claims de contagem/estado dessa data são históricos até nova verificação.

### 2026-08-03 — merge PR #1
`main` passa a existir com a fundação organizacional. Qualquer documento que continue dizendo `BLOCKED_BASE_BRANCH` torna-se stale para current-state.

### 2026-08-20 — field report ERP
ERP revela classe de falha: missão pode executar corretamente contra documentação stale/ambígua. AgentFactory Issue #2 aberta em read-only.

### 2026-08-21 — auditoria #2
`main` revalidada em `918387...`; dois P0 de current-state confirmados. Issue #2 fechada como `COMPLETED`, objeto `REPROVADO`.

### 2026-08-21 — Gate #3
Denis aprova escopo mínimo de correção em branch/Draft PR. Não autoriza merge, DBTWIN-002, Docker, Supabase, produção ou dados reais.

### 2026-08-21 — Draft PR #4
Correção documental preparada. O PR permanece draft e requer revisão/merge humano; `main` continua inalterada até esse Gate.

## Regra de atualização

Nova sessão só altera este snapshot quando revalida a fonte/ref. Não copiar “estado atual” de um handoff antigo sem observação presente.
