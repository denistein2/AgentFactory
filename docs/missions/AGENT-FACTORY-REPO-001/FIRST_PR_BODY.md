# chore(repo): establish AgentFactory foundation

## Objetivo

Estabelecer a baseline organizacional da Stein Agent Factory. Não conclui a
DBTWIN-002 nem aprova Gate 02-A ou Gate 02-B.

## Alterações

- árvore canônica de governança, missões, evidências, ferramentas e templates;
- fonte técnica v0.2 importada em `package/stein-db-twin/`, sob custódia como
  `IMPORTED_UNAUDITED_LEGACY_SOURCE`;
- cadeia de custódia do TAR e hashes individuais reconciliados;
- inventário com 90 arquivos totais e 89 registros, excluindo a si próprio;
- governança de Draft PR autônomo com merge exclusivamente humano.

## Evidências e validações

- `MANIFESTO_ORGANIZACAO_v1.md`;
- `evidence/hashes/MODULE_IMPORT_2026-08-02.csv`;
- `evidence/hashes/INVENTORY_BASELINE.csv`;
- `evidence/reports/BROKEN_REFERENCES.md`.

## Riscos e pendências

- pacote original `v0.3-phase01` ausente;
- PEND-1, PEND-2B, PEND-2C, PEND-2D e PEND-3 abertas;
- scripts 00 e 05–10, `artifacts/phase01`, fixtures/manifests completos e
  evidências E2E/fingerprints da Fase 01 ausentes;
- fonte v0.2 não auditada integralmente e não autorizada para execução.

## Gate

- [ ] CI verde
- [ ] Sem segredos
- [ ] Sem dados reais
- [ ] Referências classificadas
- [ ] Revisão humana
