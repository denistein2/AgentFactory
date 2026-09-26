# ESTRUTURA_CANONICA — Paths do pacote DBTWIN-002 no repositório atual

**Missão:** AGENT-FACTORY-DBTWIN-002  
**Lifecycle:** `ACTIVE_MISSION`  
**Última reconciliação de paths:** 2026-08-21  
**Base observada:** `main @ 918387376620f6985baeb14965c7245131114b49`

> Este documento é canônico **somente para a organização interna do pacote DBTWIN-002**. Ele não define a árvore global da Factory e não resolve sozinho current-state. Para isso: `GOVERNANCE.md` + `docs/governance/FACTORY_LOGBOOK.md`.

## 1. Paths reais relevantes

```text
AgentFactory/
├─ README.md
├─ GOVERNANCE.md
├─ SESSION_CLOSE_PROTOCOL.md
├─ docs/
│  ├─ governance/
│  │  ├─ M17_FRONTEIRA_EXECUTOR.md
│  │  ├─ M18_DECISAO_HUMANA_SUBSTITUTIVA.md
│  │  ├─ decisions/
│  │  │  ├─ current/DECISAO_SUBSTITUTIVA_SCHEMA_ONLY.md
│  │  │  ├─ history/2026-07-31_DECISAO_DUMP_COMPLETO__ORIGINAL.md
│  │  │  ├─ history/2026-08-01_STATUS_SUBSTITUICAO_DUMP_COMPLETO.md
│  │  │  └─ pending/
│  │  └─ policies/POLITICA_ISOLAMENTO_REDE.md
│  └─ missions/
│     ├─ AGENT-FACTORY-DBTWIN-001/HANDOFF_DBTWIN_001.md
│     └─ AGENT-FACTORY-DBTWIN-002/
│        ├─ README.md
│        ├─ PLAN_DBTWIN_002.md
│        ├─ ESTRUTURA_CANONICA.md
│        ├─ CONTRATO_FASE_02.md
│        ├─ VERSIONAMENTO_GIT.md
│        ├─ ORIGEM_SCHEMA_ONLY.md
│        ├─ ESTRATEGIA_AUDITORIA.md
│        ├─ VALIDACAO_SUPABASE.md
│        ├─ FIXTURES_SINTETICAS.md
│        ├─ MATRIZ_RASTREABILIDADE.md
│        ├─ MATRIZ_DEPENDENCIA_FASE01.md
│        ├─ gates/GATE_HUMANO_FASE_02.md
│        ├─ gates/pending/
│        └─ specs/
│           ├─ EVIDENCE_MANIFEST_SPEC.md
│           ├─ SCHEMA_INVENTORY_SPEC.md
│           ├─ FINGERPRINT_SPEC.md
│           ├─ SCHEMA_SOURCE_MANIFEST.md
│           └─ PACKAGE_IMPORT_MANIFEST.md
└─ package/stein-db-twin/
```

A árvore antiga que colocava `governance/` e `missions/` diretamente na raiz é **SUPERSEDED como descrição de path**. Ela permanece recuperável no histórico Git; não deve ser usada para resolver arquivos atuais.

## 2. Precedência

A precedência global vem de `GOVERNANCE.md`:

```text
M17/M18
→ decisões atuais
→ Gate
→ contrato
→ plano-mestre
→ especificações
→ matriz/relatório
```

Este arquivo resolve **path do pacote**, não substitui conteúdo normativo de nível superior.

## 3. Completude observada

Presentes na base observada:

- `.gitignore`;
- M17/M18;
- `HANDOFF_DBTWIN_001.md`;
- decisão atual schema-only + histórico original/marcador;
- pacote `package/stein-db-twin/` sob custódia v0.2;
- `columns.json` sob custódia conforme `_IMPORT_STATUS.md`.

Continuam pendentes nos termos técnicos da DBTWIN-002: fonte autoritativa schema-only, auditorias/artefatos indicados no `PLAN_DBTWIN_002.md` e demais PENDs. Esta reconciliação de path não resolve essas pendências.

## 4. Regra de `columns.json`

```text
Enquanto MATRIZ_DEPENDENCIA_FASE01 estiver inconclusiva:
  columns.json permanece BLOQUEANTE.

Se inspeção confirmar dependência do schema-only:
  obrigatório antes do Gate 02-B.

Se inspeção provar ausência de dependência:
  reclassificar como pendência histórica da Fase 01;
  não bloquear DBTWIN-002.
```

## 5. Validação de referência

Referência textual deve resolver contra o path real da ref auditada. Se o documento precisar mencionar um path histórico/proposto, deve rotulá-lo como histórico/proposto; não apresentá-lo como árvore atual.
