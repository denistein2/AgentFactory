# GATE_HUMANO_FASE_02 — Gates 02-A (preparação) e 02-B (execução)


> **Correção residual (parecer 2026-08-02):** formato oficial = schema-only; fonte autoritativa = PENDENTE até decisão registrada no `SCHEMA_SOURCE_MANIFEST`. Onde o texto abaixo sugerir 'origem já canônica', leia-se 'formato canônico; fonte pendente'.


**Missão:** AGENT-FACTORY-DBTWIN-002
**Natureza:** minuta de Gate Humano. **Não** é aprovação. Nenhuma redação presume aprovação automática.
**Data:** 01/08/2026 (revisão pós-auditoria)
**Decisor:** Denis Stein

> **Correção P0-01 (dependência circular).** A versão anterior exigia, como
> pré-condições de um único Gate, itens que só existem *após* execução (E2E
> reproduzido, isolamento provado) — enquanto proibia execução antes do Gate.
> Isso gerava deadlock. O Gate agora é **dois**:
>
> - **Gate 02-A — Preparação (estático, sem container).**
> - **Gate 02-B — Execução (sobe container, roda o fluxo).**
>
> **Fronteira decidida por Denis (01/08/2026): 02-A é ESTRITO.** Nada que suba
> container entra no 02-A. A reprodução independente do E2E é execução e pertence
> ao 02-B (ou a autorização operacional intermediária explicitamente delimitada,
> nunca implícita).

> **O que estes Gates NÃO fazem:** não escolhem (nem reescolhem) a origem do
> schema. A origem já é canônica: **schema-only**
> (`governance/decisions/current/DECISAO_SUBSTITUTIVA_SCHEMA_ONLY.md`).

---

## PARTE A — GATE 02-A (Preparação)

### A.1 Efeito único e inequívoco (corrige P1-04)

Aprovar o **Gate 02-A** autoriza **exclusivamente** trabalho **estático e sem
container**:

- **versionar a documentação do pacote** — o commit-base é **saída (pós-condição)
  do 02-A**, não entrada. A aprovação se dá contra o **manifesto pré-Git**
  (hashes dos arquivos entregues + árvore canônica proposta); o commit é
  produzido **depois** e conferido como pós-condição (corrige P0-REV-02);
- importar os artefatos da Fase 01 **com cadeia de custódia e hashes**
  (`specs/PACKAGE_IMPORT_MANIFEST.md`) — importar ≠ executar;
- auditoria **estática** de código (`sanitize_v2.py`, `columns.json`, `00–10`):
  leitura e revisão, **sem** rodar o pipeline;
- preencher a decisão de fonte autoritativa do schema
  (`specs/SCHEMA_SOURCE_MANIFEST.md`);
- construir fixtures sintéticas **como arquivos** (sem carregá-las em banco);
- especificar isolamento estrutural e contratos de evidência.

**Gate 02-A NÃO autoriza:** subir container, `pg_dump`/`pg_restore` contra
qualquer origem, reprodução do E2E, conexão a HOMOLOG/Supabase/produção, dado
real, #7730.

### A.2 Pré-condições do Gate 02-A (todas estáticas)

| # | Pré-condição | Documento | Estado |
|---|---|---|---|
| A-PC1 | Árvore canônica única fixada; **validação de referências de caminho** ok; manifesto pré-Git com hashes | `ESTRUTURA_CANONICA.md` | ✅ definida (validar referências antes de aprovar) |
| A-PC2 | Modelo de histórico da decisão substituída coerente | `governance/decisions/history/` | ✅ corrigido |
| A-PC3 | Precedência documental definida | `ESTRUTURA_CANONICA.md §2` | ✅ definida |
| A-PC4 | Contratos de evidência especificados | `specs/EVIDENCE_MANIFEST_SPEC.md`, `FINGERPRINT_SPEC.md`, `SCHEMA_INVENTORY_SPEC.md` | ✅ minutados |
| A-PC5 | Matriz de dependência dos artefatos da Fase 01 criada | `MATRIZ_DEPENDENCIA_FASE01.md` | ⏸ criada vazia; preencher por inspeção estática |
| A-PC6 | Gabarito de fonte autoritativa do schema | `specs/SCHEMA_SOURCE_MANIFEST.md` | ❓ gabarito pronto; decisão de fonte pendente (PEND-1) |
| A-PC7 | `.gitignore` + controles de commit especificados | `VERSIONAMENTO_GIT.md` | ⏸ especificado; pre-commit a implementar |

### A.3 Opções de decisão do Gate 02-A (mutuamente exclusivas)

O decisor escolhe **uma**:

- ☐ **APROVAR 02-A** — autoriza a preparação estática descrita em A.1, contra o
  commit e hashes indicados em A.5. Não autoriza nada que suba container.
- ☐ **APROVAR 02-A COM CONDIÇÕES** — lista condições e marco de verificação.
- ☐ **DEVOLVER PARA CORREÇÃO** — lacunas materiais; retorna sem autorizar preparação.
- ☐ **REJEITAR** — não prosseguir; registrar motivo e efeito.

```
Se APROVAR COM CONDIÇÕES:
  Condições: ____________________________________
  Verificação em: _______________________________
Se DEVOLVER:
  Correções exigidas: ___________________________
Se REJEITAR:
  Motivo: _______________________________________
  Efeito: _______________________________________
```

### A.4 Eventos que invalidam a aprovação 02-A

Aprovação 02-A caduca e exige novo Gate se: mudar a árvore canônica; mudar a
decisão de origem; mudar os contratos de evidência; ou entrar artefato novo sem
custódia.

### A.5 Registro do Gate 02-A

```
GATE HUMANO — 02-A (preparação, estático/sem container)
Decisor: Denis Stein
Data: ____/____/______

ENTRADAS (conferidas ANTES de aprovar):
  Manifesto pré-Git aprovado (árvore canônica proposta): ☐
  Hashes dos documentos entregues: ______________________

DECISÃO:
Opção: ☐ Aprovar 02-A  ☐ Aprovar com condições  ☐ Devolver  ☐ Rejeitar
Pré-condições: A-PC1__ A-PC2__ A-PC3__ A-PC4__ A-PC5__ A-PC6__ A-PC7__
Validade / condição de expiração: _____________

SAÍDAS (pós-condição, preenchidas APÓS execução do 02-A):
  Commit resultante após versionamento (hash): __________
  Caminho no repositório: _______________________________
  Validação de referências de caminho: ☐ ok

Observações: __________________________________
Assinatura ou registro: _______________________
```

> O campo do **commit resultante** é preenchido **depois** do versionamento e
> conferido como pós-condição. O Gate 02-A **não** exige um commit pré-existente
> como entrada — isso era a circularidade P0-REV-02, agora removida.

---

## PARTE B — GATE 02-B (Execução)

### B.1 Efeito único e inequívoco

Aprovar o **Gate 02-B** autoriza a **execução do fluxo schema-only da Fase 02**
contra o **commit e os manifestos indicados** — subir container local, extrair
schema pela fonte já decidida, carregar fixtures, rodar cenários, reproduzir o
E2E de forma independente, coletar evidências e destruir o laboratório. **Nunca**
autoriza dado real, HOMOLOG/produção de escrita, #7730 ou paridade sem evidência.

### B.1.1 Primeira etapa operacional obrigatória — B0 (corrige P0-REV-03)

A **prova** de isolamento estrutural não pode existir integralmente antes do Gate
que autoriza produzi-la. Por isso ela não é pré-condição; é a **primeira etapa
executável** após a aprovação:

```
B0 — preflight de isolamento estrutural
```

Se **B0 falhar**: não extrai schema; não carrega fixtures; não executa o E2E;
**destrói o ambiente**; encerra a missão em **STOP**. Nenhuma etapa posterior
roda sem B0 verde. Isso evita um terceiro Gate: a prova vira condição operacional
interna do 02-B, não pré-condição documental.

### B.2 Pré-condições do Gate 02-B (só após 02-A concluído)

| # | Pré-condição | Documento | Estado |
|---|---|---|---|
| B-PC1 | Commit-base e hashes fixados (versionamento comprovado) | `VERSIONAMENTO_GIT.md` | ⏸ após 02-A |
| B-PC2 | Auditoria estática de código concluída | `ESTRATEGIA_AUDITORIA.md` F1 | ⏸ pendente |
| B-PC3 | `columns.json` recuperado e `cells_masked` cruzado — **se e somente se** a matriz de dependência marcar esses artefatos como usados no fluxo schema-only | `MATRIZ_DEPENDENCIA_FASE01.md` + `ESTRATEGIA_AUDITORIA.md` F3 | ⛔/N-A conforme matriz |
| B-PC4 | Fonte autoritativa do schema definida e método aprovado | `specs/SCHEMA_SOURCE_MANIFEST.md` | ❓ decisão (PEND-1) |
| B-PC5 | Isolamento estrutural **projetado, implementado e inspecionado estaticamente** (a *prova* ocorre em B0, primeira etapa operacional) | `POLITICA_ISOLAMENTO_REDE.md` | ⏸ projeto a implementar |
| B-PC6 | Semântica Supabase com plano operacional executável | `VALIDACAO_SUPABASE.md` | ⏸ a detalhar |
| B-PC7 | Fixtures sintéticas implementadas, com oracles e SQLSTATE | `FIXTURES_SINTETICAS.md` | ⏸ a implementar |
| B-PC8 | Porta canônica resolvida ou preflight de porta livre aprovado | `POLITICA_ISOLAMENTO_REDE.md` (P2-01) | ❓ decisão/gabarito |
| B-PC9 | Nível exigido de reprodução independente definido | `ESTRATEGIA_AUDITORIA.md §3` | ❓ decisão (P1-06) |
| B-PC10 | Plano de evidências fechado (manifesto/fingerprint/inventário) | `specs/*` | ⏸ minutado |

> Enquanto B-PC4, B-PC8, B-PC9 (decisões) e B-PC3 (condicional à matriz) não
> fecharem, o caminho natural do 02-B é **aprovar com condições** ou **devolver**.

### B.3 Grau exigido de reprodução independente (P1-06)

O Gate 02-B **deve** nomear qual nível é obrigatório:

```
Nível 1 — nova execução, ambiente limpo, mesmo pipeline (repetibilidade)
Nível 2 — executor/revisor distinto, mesmo pipeline
Nível 3 — inventário e fingerprints recalculados por implementação independente
Nível 4 — ambiente independente
```
Nível exigido: ______  (decisão do decisor — não presumida pelo agente)

### B.4 Opções de decisão do Gate 02-B (mutuamente exclusivas)

- ☐ **APROVAR 02-B** — todas as B-PC satisfeitas. Autoriza execução contra o
  commit e manifestos indicados, com confirmação humana imediata antes de cada
  ação destrutiva (M18 §3). Não autoriza dado real.
- ☐ **APROVAR 02-B COM CONDIÇÕES** — condições nomeadas + marco.
- ☐ **DEVOLVER PARA CORREÇÃO**.
- ☐ **REJEITAR**.

### B.5 Eventos que invalidam a aprovação 02-B

Caduca e exige novo Gate se mudar: o schema (fonte/versão/hash), os scripts
`00–10`, o `sanitize_v2.py`, os controles de isolamento, as fixtures ou os
contratos de evidência. Qualquer mudança de destino ou expansão de escopo
também invalida.

### B.6 Registro do Gate 02-B

```
GATE HUMANO — 02-B (execução do fluxo schema-only)
Decisor: Denis Stein
Data: ____/____/______
Commit de execução aprovado (hash): ___________
Manifestos vinculados (hashes): _______________
Nível de reprodução independente exigido: _____
Opção: ☐ Aprovar 02-B  ☐ Aprovar com condições  ☐ Devolver  ☐ Rejeitar
Pré-condições: B-PC1__ … B-PC10__
Condições de invalidação reconhecidas: ☐ sim
Observações: __________________________________
Assinatura ou registro: _______________________
```

---

## PARTE C — O que NENHUM Gate autoriza

- Dado real, dump de HOMOLOG, conexão Supabase de escrita, produção, #7730.
- Declaração de paridade sem evidência.
- Ampliação de escopo além de schema-only + fixtures sintéticas.
- Reprodução E2E sob o Gate 02-A (é execução; pertence ao 02-B).

> Sem preenchimento humano dos blocos de registro, o estado permanece
> **NÃO APROVADO** e a Fase 02 **não** é executável.
