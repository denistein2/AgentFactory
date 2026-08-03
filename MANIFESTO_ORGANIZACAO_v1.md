# MANIFESTO_ORGANIZACAO_v1 — Proveniência

**Data:** 2026-08-02  
**Missão:** AGENT-FACTORY-ORG-001-R4  
**Estado:** ORG-001 staging

## Pacotes de organização analisados

| Pacote | SHA-256 | Veredito |
|---|---|---|
| `files.zip` | `43e06549b73a46c19b57f26beeccfb44682e9d56d4a520fddd6791189e7260e4` | satélites pós-auditoria |
| `files2.zip` | `aba2835c6fb1ca27a4c9b934bcdab5bcfa5a33e9b16ab55b4182691ba814d177` | duplicata funcional de `files.zip` |
| `files3.zip` | `8bb81d0f6633b9771c98396c8a160b52bdbf96f33e5506b7b1da91e95c634a6f` | histórico de 31/07, superado |
| `files4.zip` | `ad70f6743dd02f44789817817672ca4a6ab01b37a9362c518825dfffb745c660` | auditorias, M17, handoff, prompt e Gate 02-A |
| `files5.zip` | `f6b368404d149ba4f7c96423dc2d2ab5c7b85d6518aa04b86a7d394fdf248b8d` | protocolos e skeletons |

Esses ZIPs são transporte/evidência e não entram no Git. Para envio ao Drive,
registrar nome, SHA-256 e URL.

## Custódia da fonte técnica importada

| Campo | Valor |
|---|---|
| Arquivo recebido | `stein-db-twin-v0.2.tar.gz` |
| SHA-256 | `9f678ef7c423ca022dd6c95631e315ed1351485c0dd3b1c9b833a4b5b69fe732` |
| Entradas no TAR | 24 |
| Arquivos-fonte | 15 |
| Destino | `package/stein-db-twin/` |
| Arquivo criado na integração | `package/stein-db-twin/_IMPORT_STATUS.md` |
| Classificação | `IMPORTED_UNAUDITED_LEGACY_SOURCE` |
| Versão técnica importada | `v0.2` |
| `v0.3-phase01` | evidência documental; pacote-fonte pendente |

Treze arquivos chegaram e permanecem byte-idênticos. O README foi restaurado
byte a byte a partir do TAR. O `.gitignore` é a única transformação mantida, com
hash-fonte e hash-atual registrados em
`evidence/hashes/MODULE_IMPORT_2026-08-02.csv`.

## Inventário atual

`evidence/hashes/INVENTORY_BASELINE.csv` contém SHA-256 completos.

- arquivos na árvore: **90**;
- arquivos inventariados: **89**;
- exclusão deliberada: o inventário não inclui a si próprio.
