# CHANGELOG — denistein2/AgentFactory

## [Unreleased] — ORG-001

Esta versão se torna `factory/v1.0.0-foundation` somente após merge humano. A
missão não cria tag.

### 2026-08-02 — reconciliação R4 da importação v0.2

- Confirmado o arquivo-fonte `stein-db-twin-v0.2.tar.gz`, SHA-256
  `9f678ef7c423ca022dd6c95631e315ed1351485c0dd3b1c9b833a4b5b69fe732`.
- Confirmadas 24 entradas no TAR, das quais 15 são arquivos-fonte.
- Reextração temporária comparada integralmente com `package/stein-db-twin/`.
- `package/stein-db-twin/README.md` restaurado byte a byte a partir do TAR.
- `.gitignore` mantido como a única transformação de integração: libera apenas
  `seeds/seed_7730.sql`, que é sintético; os hashes de origem e atual constam no
  manifesto de importação.
- `_IMPORT_STATUS.md` registrado como arquivo criado na integração.
- Fonte importada reclassificada como `IMPORTED_UNAUDITED_LEGACY_SOURCE`, versão
  técnica `v0.2`, sob custódia e não autorizada para execução.
- Pacote-fonte original `v0.3-phase01` permanece ausente; existe somente evidência
  documental sobre ele.
- PEND-2 desmembrada: 2A resolvida; 2B, 2C e 2D abertas. PEND-3 permanece aberta.
- Inventário reconciliado para 90 arquivos totais e 89 registros, excluindo o
  próprio `INVENTORY_BASELINE.csv`.
- Governança de PR atualizada: branch/validação/commit/push de branch/Draft PR
  permitidos ao agente; merge humano; push direto em `main` proibido.

### Pendências técnicas registradas, não corrigidas

- `-WithData` contradiz o fluxo schema-only; `source_project_ref` está hardcoded;
  o self-test contém referências realistas à Dolce; o residual scan cobre PII
  limitada; `jsonb`/texto livre permanece aberto; restore pode deixar estado
  parcial; `seed_7730.sql` é skeleton com `ROLLBACK`; PEND-3 segue aberta.

### Ausências confirmadas

- pacote original `v0.3-phase01`;
- scripts 00 e 05–10;
- `artifacts/phase01`;
- fixtures e manifests completos;
- evidências E2E e fingerprints da Fase 01.

### Não executado

Nenhum Docker, Supabase, `pg_dump`, banco remoto, HOMOLOG ou produção. Nenhum
push, PR, merge ou tag foi realizado nesta reconciliação local.
