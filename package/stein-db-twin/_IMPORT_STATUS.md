# Importação do módulo — custódia e classificação

**Data:** 2026-08-02  
**Missão de reconciliação:** AGENT-FACTORY-ORG-001-R4  
**Classificação:** `IMPORTED_UNAUDITED_LEGACY_SOURCE`  
**Status:** sob custódia, não auditado integralmente e não autorizado para execução

## Fonte recebida

- arquivo exato: `stein-db-twin-v0.2.tar.gz`;
- SHA-256: `9f678ef7c423ca022dd6c95631e315ed1351485c0dd3b1c9b833a4b5b69fe732`;
- conteúdo: 24 entradas, sendo 15 arquivos-fonte;
- versão técnica demonstrada pela fonte: `v0.2`;
- destino: `package/stein-db-twin/`;
- arquivo adicional criado na integração: `_IMPORT_STATUS.md`.

O TAR foi listado integralmente, reextraído em área temporária e comparado com o
destino. O README foi restaurado byte a byte. O `.gitignore` é a única
transformação mantida: adiciona a exceção explícita para o skeleton sintético
`seeds/seed_7730.sql`. Hashes de origem e atuais constam em
`evidence/hashes/MODULE_IMPORT_2026-08-02.csv`.

## Verdade de versão

O código presente é **v0.2**, e não o pacote comprovado `v0.3-phase01`. Há
documentação histórica sobre `v0.3-phase01`, mas seu pacote-fonte original ainda
precisa ser localizado e reconciliado.

## PEND-2

- **PEND-2A — RESOLVIDA:** localização e custódia de `config/columns.json`.
- **PEND-2B — ABERTA:** auditoria técnica integral de `columns.json`.
- **PEND-2C — ABERTA:** cruzamento `cells_masked=24 × columns.json`.
- **PEND-2D — ABERTA:** confirmar dependência no fluxo schema-only.

PEND-2 não está integralmente encerrada.

## Políticas legadas

`policies/human-gates.json` e `policies/permissions.json` são políticas legadas da
fonte v0.2, preservadas byte a byte. Elas estão subordinadas a `GOVERNANCE.md`,
`SESSION_CLOSE_PROTOCOL.md` e `docs/governance/M17_FRONTEIRA_EXECUTOR.md`.

A governança raiz vigente permite ao agente criar branch de sessão, validar,
commitar, enviar a branch e abrir ou atualizar Draft PR. Merge é exclusivamente
humano e push direto em `main` é proibido.

## Pendências técnicas registradas — sem alegação de correção

- `-WithData` contradiz o fluxo schema-only;
- `source_project_ref` está hardcoded;
- o self-test contém referências realistas à Dolce;
- o residual scan cobre conjunto limitado de PII;
- campos `jsonb` e texto livre continuam sem cobertura demonstrada;
- o restore pode deixar estado parcial após falha;
- `seed_7730.sql` é um skeleton sintético que termina em `ROLLBACK`;
- **PEND-3** permanece aberta: o código usa 54329 e a governança registra 55439.

Esses itens pertencem à auditoria técnica posterior à fundação do repositório.
O pipeline não foi executado nem reescrito nesta missão.

## Ausências confirmadas

- pacote original `v0.3-phase01`;
- scripts 00 e 05–10;
- `artifacts/phase01`;
- fixtures e manifests completos;
- evidências E2E e fingerprints da Fase 01.

Não foram inventados substitutos. Artefatos pesados destinados ao Drive devem
ser registrados por nome, SHA-256 e URL, sem cópia para o Git.
