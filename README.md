# AgentFactory — Stein Agent Factory

Repositório de governança, planejamento e código sob custódia da **Stein Agent
Factory**. A árvore organiza a construção de *database twins* descartáveis para
testes isolados do ERP Food Control, sem introduzir dados reais e sem autorizar
acesso a HOMOLOG, Supabase remoto ou produção.

> **Responsável pelos gates e pelo merge:** Denis Stein.  
> **Regra permanente:** `coerência documental ≠ reprodução de execução ≠ auditoria de código`.

## Estado ORG-001

```text
STATUS: STAGING VALIDADO — BLOCKED_BASE_BRANCH
Arquivos na árvore: 90
Arquivos inventariados: 89 (INVENTORY_BASELINE.csv exclui a si próprio)
GitHub: nenhuma tag criada; factory/v1.0.0-foundation somente após merge humano
PR: agente pode criar branch, validar, commitar, enviar a branch e abrir/atualizar Draft PR
Merge: exclusivamente humano; push direto em main proibido
DBTWIN-002: Gate 02-A NÃO APROVADO; Gate 02-B indisponível
Bloqueio Git: repositório remoto sem heads/main; requer main mínima como base do PR
```

## O que esta baseline é — e o que não é

Esta é uma baseline organizacional com uma fonte técnica legada sob custódia. Ela
não afirma paridade do DB Twin, conclusão da DBTWIN-002, aprovação de Gate 02-A
ou 02-B, reprodução do pipeline nem auditoria técnica integral.

A fonte importada está classificada como `IMPORTED_UNAUDITED_LEGACY_SOURCE` e
**não está autorizada para execução**. Nesta reconciliação foram permitidos apenas
validação estática, compilação e `sanitize_v2.py --self-test` local.

## Verdade de versão

| Item | Versão/estado | Situação |
|---|---|---|
| Fábrica / repositório | `factory/v1.0.0-foundation` | somente após merge humano |
| Fonte técnica importada | `v0.2` | 15 arquivos sob custódia, não auditados integralmente |
| Pacote `v0.3-phase01` | evidência documental | pacote-fonte original ainda não localizado nem reconciliado |

## Estrutura

```text
AgentFactory/
├─ README.md · CHANGELOG.md · GOVERNANCE.md · SECURITY.md
├─ .github/            workflows e template de PR
├─ docs/               governança, missões, sessões, handoffs e auditorias
├─ package/stein-db-twin/   fonte v0.2 sob custódia + _IMPORT_STATUS.md
├─ evidence/           hashes, manifestos e relatórios
├─ tools/              inventário e validação
├─ templates/          missão, handoff, decisão, auditoria e PR
└─ archive/            histórico, superseded e quarentena
```

## GitHub × Drive

- **GitHub:** documentação canônica, código sob custódia, decisões, contratos,
  missões, PRs e histórico versionado.
- **Drive:** pacotes/evidências pesadas e releases. Para cada artefato destinado
  ao Drive, registrar nome, SHA-256 e URL; não copiar binários para o Git.

## Ordem de leitura

1. `GOVERNANCE.md`
2. `docs/governance/M17_FRONTEIRA_EXECUTOR.md`
3. `package/stein-db-twin/_IMPORT_STATUS.md`
4. `docs/missions/AGENT-FACTORY-DBTWIN-002/README.md`
5. `docs/missions/AGENT-FACTORY-DBTWIN-002/PLAN_DBTWIN_002.md`

## Pendências canônicas

- **PEND-1:** fonte autoritativa do schema-only.
- **PEND-2A — RESOLVIDA:** `columns.json` localizado e mantido sob custódia.
- **PEND-2B — ABERTA:** auditoria técnica de `columns.json`.
- **PEND-2C — ABERTA:** cruzamento `cells_masked=24 × columns.json`.
- **PEND-2D — ABERTA:** dependência de `columns.json` no fluxo schema-only.
- **PEND-3 — ABERTA:** porta 54329 no código legado versus 55439 na governança.
- Pacote-fonte original `v0.3-phase01`, scripts 00 e 05–10,
  `artifacts/phase01`, fixtures/manifests completos e evidências E2E/fingerprints
  da Fase 01 continuam ausentes.

Nenhum dump, dado real ou segredo deve entrar nesta árvore.
