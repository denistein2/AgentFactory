# RESPOSTA AO PARECER GPT — ORG-001 (reconciliação)

**Data:** 2026-08-02
**Sobre:** `PARECER_TECNICO_ORG_001_CONSOLIDACAO_CLAUDE.md` (GPT)

O parecer analisou os pacotes da **1ª rodada** (`AgentFactory_v1_repo.zip`,
`MISSAO_ORG_001.md`). Vários P0 já haviam sido corrigidos na 2ª rodada; os demais
foram aplicados agora. Registro item a item, para rastreabilidade.

## Já corrigido antes do parecer (2ª rodada)
- **P0-ORG-04** (release declarado): o CHANGELOG usava uma versão sem namespace.
  Agora está `[Unreleased]`; a versão futura correta é
  `factory/v1.0.0-foundation`, somente após merge humano.
- **P0-ORG-02** (SHA truncado): inventário da 2ª rodada já trazia 64 chars completos.
- **Versão Fábrica × módulo** (STOP-04): já separada no README da 2ª rodada.

## Aceito e aplicado agora
- **P0-ORG-06:** `DECISAO_GATE_02A` movida para `missions/DBTWIN-002/gates/pending/` com banner **BLOQUEADO** (5/25 conferidos ≠ pronto).
- **P0-ORG-07:** `..._SUPERSEDED.md` movido para `archive/quarantine-index/` (redundante com original + marcador de status). Canônicos = só os dois de `history/`.
- **README dividido** (parecer 2.3): criado `missions/DBTWIN-002/README.md`; README raiz é o da Fábrica.
- **Correções residuais §3:** notas de "formato ≠ fonte" inseridas em `GATE_HUMANO_FASE_02`, `CONTRATO_FASE_02`, `VERSIONAMENTO_GIT`.
- **P0-ORG-01/03:** manifesto de proveniência agora inclui SHA-256 completo dos 5 ZIPs-fonte + nota sobre files/files2 (container difere, conteúdo idêntico).
- **P1-ORG-01:** README raiz corrigido — caminhos resolvem da raiz, ordem de HOMOLOG removida, estado ORG-001 e distinção GitHub×Drive adicionados.
- **P1-ORG-02:** `.gitignore` reforçado (backups, sqlite/db, exports, binários grandes).
- **D3 / P0-ORG-03 (workflow):** `fetch-depth: 0` + fetch de main + base fallback; permissão mínima (`contents: read`); secret scan por conteúdo; corpo do PR = SESSION real; sem auto-merge.
- **decisions/pending/** criado.
- **Relatório real de referências:** `evidence/reports/BROKEN_REFERENCES.md`,
  regenerado após a importação v0.2; `columns.json` e `sanitize_v2.py` estão presentes.

## Aceito com divergência de Denis
- **D2 (nome da pasta):** propostas alternativas foram rejeitadas. **Denis
  decidiu manter `package/stein-db-twin`** (árvore original), preservando os
  links do `PACKAGE_IMPORT_MANIFEST` e da `ESTRUTURA_CANONICA`. Aplicado.

## Aceito integralmente (política)
- **D1:** versões NOVA como base; `_conflitos_decidir/` fora do Git (vai pro Drive como evidência).
- **D3:** draft + gate humano, sem auto-merge.
- **D4:** Drive NÃO espelha o GitHub; estrutura própria (INBOX/RAW/EVIDENCE/RELEASES/…).
- **Tag:** `factory/v1.0.0-foundation` só **após merge** (decisão de Denis).
- **P0-ORG-05 (prompt Codex):** ordem corrigida para branch→validar→commit→push→draft PR→revisar→merge→tag. Ver `BOOTSTRAP_GIT.md`.

## Não aplicável / observação
- **P0-ORG-05:** o `PROMPT_CODEX_ORG_001.md` da 1ª rodada foi substituído pelo `BOOTSTRAP_GIT.md`, que já segue a ordem correta.

## Estado resultante
```
ORG-001: STAGING CANDIDATO — correções P0 aplicadas
Tag: não publicar até merge (factory/v1.0.0-foundation)
DBTWIN-002: Gate 02-A NÃO APROVADO (movido para pending/BLOQUEADO)
```
