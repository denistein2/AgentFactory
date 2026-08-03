# ESTRUTURA_CANONICA — Árvore única e precedência documental

**Missão:** AGENT-FACTORY-DBTWIN-002
**Status:** planejamento. Define a árvore canônica ÚNICA do pacote e a ordem de precedência entre documentos.
**Data:** 01/08/2026

> Corrige P1-01 (paths divergentes entre plano/README e estratégia Git) e
> P1-02 (hierarquia de autoridade contraditória). Esta é a **única** árvore
> válida; todos os links relativos do pacote seguem-na.

---

## 1. Árvore canônica única

```
AgentFactory/                                  # raiz do repositório denistein2/AgentFactory
├─ README.md
├─ .gitignore
├─ governance/
│  ├─ M17_FRONTEIRA_EXECUTOR.md                # canônico do projeto (a incluir; ver P2-05)
│  ├─ M18_DECISAO_HUMANA_SUBSTITUTIVA.md       # canônico do projeto (a incluir; ver P1-03)
│  └─ decisions/
│     ├─ current/
│     │  └─ DECISAO_SUBSTITUTIVA_SCHEMA_ONLY.md
│     └─ history/
│        ├─ 2026-07-31_DECISAO_DUMP_COMPLETO__ORIGINAL.md   # bytes intactos do original
│        └─ 2026-08-01_STATUS_SUBSTITUICAO_DUMP_COMPLETO.md # marcador de status (só referencia)
├─ missions/
│  ├─ DBTWIN-001/
│  │  └─ HANDOFF_DBTWIN_001.md                 # canônico da 001 (a incluir; ver P2-05)
│  └─ DBTWIN-002/
│     ├─ PLAN_DBTWIN_002.md                    # documento-mestre / índice / estado
│     ├─ ESTRUTURA_CANONICA.md                 # este arquivo
│     └─ docs/
│        ├─ CONTRATO_FASE_02.md
│        ├─ GATE_HUMANO_FASE_02.md             # contém Gate 02-A e Gate 02-B
│        ├─ VERSIONAMENTO_GIT.md
│        ├─ ORIGEM_SCHEMA_ONLY.md
│        ├─ POLITICA_ISOLAMENTO_REDE.md
│        ├─ ESTRATEGIA_AUDITORIA.md
│        ├─ VALIDACAO_SUPABASE.md
│        ├─ FIXTURES_SINTETICAS.md
│        ├─ MATRIZ_RASTREABILIDADE.md
│        ├─ MATRIZ_DEPENDENCIA_FASE01.md       # P0-06: dependência dos artefatos legados
│        └─ specs/
│           ├─ EVIDENCE_MANIFEST_SPEC.md       # P0-08
│           ├─ SCHEMA_INVENTORY_SPEC.md        # P0-08
│           ├─ FINGERPRINT_SPEC.md             # P0-02 / P0-08
│           ├─ SCHEMA_SOURCE_MANIFEST.md       # P0-04 (gabarito; fonte pendente)
│           └─ PACKAGE_IMPORT_MANIFEST.md      # P1-14 (cadeia de custódia)
└─ package/
   └─ stein-db-twin/                           # scripts 00–10, sanitize_v2.py, columns.json (após auditoria/custódia)
```

> **Nota sobre este pacote de planejamento:** os arquivos entregues nesta sessão
> correspondem aos de `missions/DBTWIN-002/` e às decisões em
> `governance/decisions/`. Os itens marcados "a incluir" (M17, M18, HANDOFF,
> `.gitignore`, pacote `stein-db-twin`) são pré-condições de completude, não
> conteúdo produzível por suposição — ver classificação em P2-05 abaixo.

---

## 2. Precedência documental (corrige P1-02)

Em qualquer divergência, vale a ordem abaixo (do mais forte ao mais fraco):

```
1. Governança canônica M17 / M18
2. Decisões humanas atuais (governance/decisions/current/)
3. Gate humano preenchido e vinculado a commit
4. Contrato da missão (CONTRATO_FASE_02.md)
5. Plano-mestre (PLAN_DBTWIN_002.md)
6. Especificações técnicas (docs/ e docs/specs/)
7. Matriz e relatórios
```

**Regra de correção obrigatória:** quando um documento de nível inferior
contradiz o plano-mestre, a divergência **não** é resolvida ignorando o
plano-mestre — ela gera **obrigação de atualizar o plano-mestre** para refletir
a fonte correta. O plano-mestre é mapa; um mapa errado se corrige, não se
abandona.

> Isto substitui a formulação anterior do plano ("o documento-satélite prevalece
> sobre o resumo"), que transformava o mestre numa fonte que podia estar errada
> sem ser atualizada.

---

## 3. Classificação de completude dos documentos ausentes (P2-05)

| Documento | Classe |
|---|---|
| `.gitignore` | obrigatório antes do Gate 02-A |
| `M17_FRONTEIRA_EXECUTOR.md` | obrigatório antes do Gate 02-A (canônico existente, a incluir no repo) |
| `M18_DECISAO_HUMANA_SUBSTITUTIVA.md` | obrigatório antes do Gate 02-A (canônico existente, a incluir no repo) |
| `HANDOFF_DBTWIN_001.md` | obrigatório antes do Gate 02-A (canônico existente, a incluir no repo) |
| `2026-07-31_DECISAO_DUMP_COMPLETO__ORIGINAL.md` (bytes intactos) | obrigatório antes do Gate 02-A |
| `SCHEMA_SOURCE_MANIFEST.md` preenchido | obrigatório antes do Gate 02-B |
| pacote `stein-db-twin` sob custódia | obrigatório antes do Gate 02-B |
| `columns.json` | **condicional** (ver regra abaixo) |

## 4. Validação de referências de caminho

Antes de qualquer commit (Gate 02-A em diante), rodar **validação de referências
de caminho** contra esta árvore. Referência que não resolve é falha de
pré-condição, não detalhe editorial. (Os documentos usam **referências textuais**
entre crases, não links Markdown; o relatório de validação as classifica em:
referência válida, arquivo declarado mas ausente, caminho inválido, referência
não concreta, link Markdown real.)

## 5. Regra canônica de `columns.json` (padrão único — corrige P0-REV-04)

Vale em **todos** os documentos do pacote:

```
Enquanto a MATRIZ_DEPENDENCIA_FASE01 estiver inconclusiva:
  columns.json permanece BLOQUEANTE.

Se a inspeção confirmar dependência do fluxo schema-only:
  columns.json é OBRIGATÓRIO antes do Gate 02-B.

Se a inspeção provar ausência de dependência:
  columns.json é reclassificado como PENDÊNCIA HISTÓRICA da Fase 01;
  NÃO bloqueia a DBTWIN-002.
```
