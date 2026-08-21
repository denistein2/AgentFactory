---
session_id: 2026-08-21-GOVERNANCE-RESET-FACTORY-001-01
mission_id: GOVERNANCE-RESET-FACTORY-001
issue: https://github.com/denistein2/AgentFactory/issues/3
started_at: 2026-08-21T15:18:00-03:00
finished_at: PENDING_POST_PR
status: READY_FOR_DRAFT_PR
branch: session/2026-08-21/governance-reset-factory-001
base_ref: main
base_sha: 918387376620f6985baeb14965c7245131114b49
commit: PENDING_POST_COMMIT
pull_request: PENDING_POST_PR
actor_type: AI_AGENT
requested_executor: ChatGPT project operator / autopilot
actual_executor: ChatGPT
provider: OpenAI
product_agent: ChatGPT
model_reported: GPT-5.6 Sol
role: governance executor
run_id: UNVERIFIED
evidence_strength: DOCUMENT_COHERENCE
does_not_prove: merge em main; correção técnica do DBTWIN; execução de banco/container
---

# SESSION — GOVERNANCE-RESET-FACTORY-001

## 1. Objetivo

Executar o escopo mínimo aprovado na Issue #3: corrigir current-state/path stale e introduzir proveniência, identidade de executor, routing e logbook mínimos, sem merge e sem executar DBTWIN-002.

## 2. Estado recebido

- `main` revalidada em `918387376620f6985baeb14965c7245131114b49`;
- Issue #2 encerrada `COMPLETED`, objeto `REPROVADO`;
- P0 confirmados: README dizia `BLOCKED_BASE_BRANCH`; ESTRUTURA_CANONICA declarava árvore global divergente da árvore real;
- field report do Drive tratado como `EXTERNAL_CONTEXT`, não autoridade automática.

## 3. Decisões/Gates

Denis aprovou **ESCOPO MÍNIMO** em 2026-08-21T15:18:00-03:00. Autorizado branch/validação/commit/push/Draft PR. Merge, deploy, DBTWIN-002, Docker, Supabase, HOMOLOG, produção, dado real/PII/segredo não autorizados.

## 4. Alterações

- README reconciliado com main existente e PR #1 mergeada;
- GOVERNANCE separa autoridade semântica de current-state;
- ESTRUTURA_CANONICA limitada ao pacote DBTWIN-002 e corrigida para paths reais;
- criado `PROVENANCE_STANDARD.md`;
- criado `MISSION_MANIFEST_STANDARD.md`;
- criado `AGENT_ROUTING_HEURISTIC.md`;
- criado `FACTORY_LOGBOOK.md`;
- SESSION_CLOSE_PROTOCOL ampliado com executor solicitado/real, provider/model, ref/SHA, timestamps, evidência e `does_not_prove`;
- README local da DBTWIN-002 passa a apontar para governança/logbook antes de resolver current-state.

## 5. Evidências e proveniência

- GitHub Issue #2 + comentário de auditoria;
- GitHub Issue #3 + Gate Humano;
- `main @ 918387376620f6985baeb14965c7245131114b49` revalidada por connector;
- árvore real de `docs/missions/`, DBTWIN-001 e DBTWIN-002 lida por connector;
- field report Drive `FIELD_REPORT_GOVERNANCE_CRASH_ERP_FOOD_CONTROL_2026-08-20.docx` apenas como contexto externo.

## 6. Validações

A concluir pós-commit: compare `main...branch`, leitura de arquivos alterados, status/CI do Draft PR e verificação de ausência de merge.

## 7. Desvios

Uma reação `eyes` foi adicionada acidentalmente ao PR #1 durante operação de ferramenta e removida imediatamente; nenhum conteúdo, review, branch ou estado do PR #1 foi alterado.

## 8. Riscos

- documentos históricos ainda contêm claims verdadeiros à época; leitores devem usar lifecycle/current-state index;
- o reset documental não demonstra correção técnica do DB Twin;
- novos padrões só se tornam canônicos na `main` após merge humano.

## 9. Pendências

- revisão humana do Draft PR;
- merge humano se aprovado;
- PENDs técnicos DBTWIN permanecem fora de escopo.

## 10. Próxima sessão

Revisar Draft PR e decidir merge. Se mergeado, revalidar `main` e atualizar o snapshot do `FACTORY_LOGBOOK` numa sessão futura somente se o SHA/estado mudar materialmente.
