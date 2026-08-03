# PACKAGE_IMPORT_MANIFEST — cadeia de custódia

**Status:** fonte v0.2 importada sob custódia; auditoria técnica pendente  
**Data da reconciliação:** 2026-08-02  
**Classificação:** `IMPORTED_UNAUDITED_LEGACY_SOURCE`

Importar com hash não equivale a executar nem a auditar.

## Identificação do pacote

| Campo | Valor |
|---|---|
| Arquivo exato recebido | `stein-db-twin-v0.2.tar.gz` |
| SHA-256 | `9f678ef7c423ca022dd6c95631e315ed1351485c0dd3b1c9b833a4b5b69fe732` |
| Entradas do TAR | 24 |
| Arquivos-fonte | 15 |
| Versão demonstrada | `v0.2` |
| Destino | `package/stein-db-twin/` |
| Arquivo criado na integração | `_IMPORT_STATUS.md` |
| Forma de incorporação | cópia para staging existente, sem execução |
| Commit de importação | não criado nesta missão |

## Lista integral das 24 entradas do TAR

```text
stein-db-twin/
stein-db-twin/sanitizer/
stein-db-twin/sanitizer/fixtures/
stein-db-twin/sanitizer/sanitize_v2.py
stein-db-twin/config/
stein-db-twin/config/docker-compose.yml
stein-db-twin/config/columns.json
stein-db-twin/policies/
stein-db-twin/policies/human-gates.json
stein-db-twin/policies/permissions.json
stein-db-twin/README.md
stein-db-twin/scripts/
stein-db-twin/scripts/01_dump_homolog.ps1
stein-db-twin/scripts/03_start_local.ps1
stein-db-twin/scripts/04_restore_mission.ps1
stein-db-twin/scripts/02_sanitize.ps1
stein-db-twin/.gitignore
stein-db-twin/seeds/
stein-db-twin/seeds/seed_7730.sql
stein-db-twin/docs/
stein-db-twin/docs/CHANGELOG_v0.2.md
stein-db-twin/docs/RUNBOOK.md
stein-db-twin/docs/MISSION_TEMPLATE.md
stein-db-twin/manifests/
```

## Resultado da comparação dos 15 arquivos-fonte

- 13 arquivos sempre permaneceram byte-idênticos ao TAR;
- `README.md` havia sido transformado e foi restaurado byte a byte; hash-fonte e
  hash-atual agora são ambos
  `5b697bedaab6a8559431bce5065456e6415c19880c2e6d21da9d97213dbe3203`;
- `.gitignore` é a única transformação mantida:
  - hash-fonte: `ce2bfa63e17a9a76f52d63015a3703a07e1050b77087e8d1c3622a2d43f4e796`;
  - hash-atual: `c5ed29021d4f15e588206633c1875570ca74e5e567195ca0b74182b2b2538fb8`;
  - motivo: exceção explícita apenas para `seeds/seed_7730.sql`, skeleton sintético.

Os hashes fonte/atuais de todos os arquivos e o registro do arquivo criado na
integração estão em `evidence/hashes/MODULE_IMPORT_2026-08-02.csv`.

## Políticas e autorização

`human-gates.json` e `permissions.json` são políticas legadas da v0.2,
subordinadas à governança raiz atual. A fonte não está autorizada para execução.

## PEND-2

- PEND-2A localização/custódia: **RESOLVIDA**;
- PEND-2B auditoria técnica: **ABERTA**;
- PEND-2C `cells_masked=24 × columns.json`: **ABERTA**;
- PEND-2D dependência no schema-only: **ABERTA**.

## Ausências

- pacote original `v0.3-phase01`;
- scripts 00 e 05–10;
- `artifacts/phase01`;
- fixtures e manifests completos;
- evidências E2E e fingerprints da Fase 01.

Essas ausências não foram preenchidas por arquivos inventados. Artefatos para o
Drive devem ser registrados por nome, SHA-256 e URL.
