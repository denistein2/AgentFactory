# DBTWIN-002 — Planejamento da Fase 02 (schema-only)

**Missão:** preparar a Fase 02 sem executá-la.  
**Fonte de estado:** `PLAN_DBTWIN_002.md`.  
**Árvore e precedência:** `ESTRUTURA_CANONICA.md`.

## Estado

```text
CANDIDATO A GATE 02-A — NÃO APROVADO
Gate 02-B indisponível
Nenhuma execução da Fase 02 autorizada
```

## Formato, fonte e versão

- formato oficial futuro: schema-only;
- fonte autoritativa do schema-only: pendente (PEND-1);
- fonte técnica atualmente importada: v0.2, sob custódia como
  `IMPORTED_UNAUDITED_LEGACY_SOURCE`, não auditada integralmente e não autorizada
  para execução;
- `v0.3-phase01`: evidência documental existente; pacote-fonte original ainda a localizar.

## Conteúdo da missão

- `PLAN_DBTWIN_002.md` — documento-mestre;
- `ESTRUTURA_CANONICA.md` — árvore e precedência;
- contrato, versionamento, origem schema-only, validação Supabase, fixtures,
  auditoria e matrizes;
- `specs/` — contratos de evidência, schema, fingerprint e custódia;
- `audits/` — auditorias documentais histórica e vigente;
- `gates/pending/` — decisão 02-A bloqueada, não aprovada.

## Pendências

- PEND-1: fonte autoritativa schema-only.
- PEND-2A resolvida: `columns.json` localizado e sob custódia.
- PEND-2B aberta: auditoria técnica de `columns.json`.
- PEND-2C aberta: `cells_masked=24 × columns.json`.
- PEND-2D aberta: dependência no schema-only.
- PEND-3 aberta: porta.
- Ausentes: pacote original `v0.3-phase01`, scripts 00 e 05–10,
  `artifacts/phase01`, fixtures/manifests completos e evidências E2E/fingerprints.
