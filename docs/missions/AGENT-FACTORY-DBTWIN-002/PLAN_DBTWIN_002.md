# PLAN_DBTWIN_002 — Documento-mestre da missão AGENT-FACTORY-DBTWIN-002

**Projeto:** 02 — Stein Agent Factory (Fábrica de Agentes)
**Missão:** AGENT-FACTORY-DBTWIN-002 — **PREPARAR** a Fase 02, **sem executá-la**
**Pacote:** planejamento canônico modular (schema-only)
**Data:** 01/08/2026
**Status da missão:** PLANEJAMENTO. Nenhuma execução autorizada.
**Formato oficial da Fase 02:** schema-only; fonte autoritativa pendente (PEND-1)

> Este é o documento-mestre e a **fonte única de estado** da missão DBTWIN-002.
> Ele indexa os demais documentos do pacote e é **mapa**, não substitui o
> conteúdo detalhado.
>
> **Precedência (corrige P1-02):** a ordem de autoridade está em
> `ESTRUTURA_CANONICA.md §2`. Quando um documento de nível inferior contradiz
> este plano, a divergência gera **obrigação de corrigir o plano-mestre** para
> refletir a fonte correta — o mapa errado se corrige, não se ignora. A
> formulação anterior ("o satélite prevalece sobre o resumo") ficava com um
> mestre que podia estar errado sem ser atualizado; substituída.

---

## 0. Aviso de escopo (topo, inegociável)

- A missão é **exclusivamente de planejamento**.
- **Nenhuma execução** de fluxo está autorizada nesta sessão: sem versionamento canônico, sem Docker, sem Supabase, sem rede remota, sem #7730, sem dado real.
  - **Desvio registrado:** um `git init` local temporário foi executado para checagem auxiliar de referências e **revertido em seguida** (sem commit/remote/push). Não é o versionamento canônico do Gate 02-A; fica registrado, não apagado.
- Comandos futuros aparecem no pacote **apenas como proposta controlada**, nunca como ação realizada.
- A **Fase 02 não inicia**. Nenhuma ação do agente a inicia. Os gates humanos são de Denis; o agente não os presume.
- **Fase 01 não é reaberta.** Não se reexecuta Docker, não se repropõe correção já aprovada.

---

## 1. Objetivo da DBTWIN-002

Produzir o pacote de planejamento que torna a Fase 02 **executável com segurança no futuro**, sob origem schema-only, entregando: contrato, Gate Humano, versionamento Git, especificação da origem schema-only, política de isolamento/rede, estratégia de auditoria técnica, plano de validação da semântica Supabase, fixtures sintéticas e matriz de rastreabilidade.

**Formulação central da fábrica:**
> Copiar fielmente a arquitetura e o comportamento do produto; reconstruir os cenários com dados sintéticos próprios e relevantes.

---

## 2. Estado atual (reconstruído do handoff DBTWIN-001)

- A documentação histórica descreve a Fase 01 Sintética como **CANDIDATA** e
  menciona `stein-db-twin v0.3-phase01`. Isso é evidência documental, não prova de
  custódia: o pacote-fonte original v0.3-phase01 ainda não foi localizado.
- A única fonte técnica importada é `v0.2`, classificada como
  `IMPORTED_UNAUDITED_LEGACY_SOURCE`, sob custódia e não autorizada para execução.
- Ciclo mecânico local 100% sintético executado fim a fim (preflight → self-test → sanitização → start → restore → validação → alteração destrutiva → reset → fingerprint → destroy), modo Synthetic, `postgres:16-alpine`, **sem alegação de paridade**, bind em `127.0.0.1:55439`.
- Reset restaura estado bit a bit: inicial = final ≠ destrutivo. Zero acesso a banco remoto; zero containers remanescentes. Houve pull público da imagem (rede total ≠ zero).
- Infra da estação validada (WSL2, Docker Desktop/Engine/Compose, VT-x, reorganização de disco) — **fato de infraestrutura**, fora do "resultado técnico provado" do ciclo.
- **Laboratório destruído**, porta 55439 sem listener, nenhum container ativo.

**Nível de evidência (definição oficial, fonte única no handoff):**
```
coerência documental  ≠  reprodução de execução  ≠  auditoria de código
```
O PASS da Fase 01 é **coerência documental**, não corretude de código verificada.

---

## 3. Premissas

- **P1.** Formato oficial = schema-only (estrutural + comportamental); fonte autoritativa pendente (PEND-1). `Testbank.sql`/dump completo fora do fluxo (ver `governance/decisions/current/DECISAO_SUBSTITUTIVA_SCHEMA_ONLY.md`).
- **P2.** Dados de teste = fixtures sintéticas próprias, determinísticas, versionáveis. Nenhuma derivada de cliente real.
- **P3.** M17: executor local roda comandos mecânicos; Denis decide gates; Denis não é barramento de comandos.
- **P4.** M18 governa substituições internas; limites externos (LGPD, provedores, segurança inseparável) permanecem.
- **P5.** Versionar o pacote no repositório é **condição #1** e anterior a qualquer execução da Fase 02.

---

## 4. Limites inegociáveis

1. Dado real, dump de HOMOLOG, conexão Supabase, produção e aplicação da #7730 **proibidos** até autorização humana específica e explícita.
2. Fase 02 **não autorizada** a iniciar.
3. Fase 01 **não reaberta**; Docker **não reexecutado**; correções aprovadas **não repropostas**.
4. Sem melhoria oportunista de schema/RLS/grants durante reprodução — **primeiro fidelidade, depois evolução** (em missão própria).

---

## 5. Entregáveis do pacote (mapa dos documentos)

| # | Entregável | Documento | Responsabilidade |
|---|---|---|---|
| 1 | Rastreabilidade da decisão humana | `governance/decisions/current/DECISAO_SUBSTITUTIVA_SCHEMA_ONLY.md` + `governance/decisions/history/2026-07-31_DECISAO_DUMP_COMPLETO__ORIGINAL.md` + `governance/decisions/history/2026-08-01_STATUS_SUBSTITUICAO_DUMP_COMPLETO.md` | Original bytes intactos + marcador de status; nova decisão canônica |
| 1b | Árvore canônica + precedência | `ESTRUTURA_CANONICA.md` | Árvore única, precedência documental, completude |
| 2 | Documento-mestre | `PLAN_DBTWIN_002.md` (este) | Índice, estado, premissas, limites, mapa |
| 3 | Contrato da Fase 02 | `CONTRATO_FASE_02.md` | Escopo, entradas/saídas, invariantes, aceite, parada |
| 4 | Gate Humano da Fase 02 | `gates/GATE_HUMANO_FASE_02.md` | Decisão de prontidão/segurança; sem reescolher origem |
| 5 | Versionamento Git | `VERSIONAMENTO_GIT.md` | Repo, commit-base, ignorados, delta |
| 6 | Origem schema-only | `ORIGEM_SCHEMA_ONLY.md` | Objetos incluídos e excluídos |
| 7 | Isolamento e rede | `docs/governance/policies/POLITICA_ISOLAMENTO_REDE.md` | Controles estruturais + STOP GATES |
| 8 | Auditoria técnica | `ESTRATEGIA_AUDITORIA.md` | Código, E2E, cells_masked, matriz de evidência |
| 9 | Semântica Supabase | `VALIDACAO_SUPABASE.md` | Roles/RLS/funções/JWT/tenant/etc. |
| 10 | Fixtures sintéticas | `FIXTURES_SINTETICAS.md` | Catálogo de cenários próprios |
| 11 | Matriz de rastreabilidade | `MATRIZ_RASTREABILIDADE.md` | Risco ↔ condição ↔ requisito ↔ doc ↔ evidência ↔ Gate |
| 12 | Dependência dos artefatos da Fase 01 | `MATRIZ_DEPENDENCIA_FASE01.md` | Se legado bloqueia schema-only (bloqueio até inspeção) |
| 13 | Contratos de evidência | `specs/EVIDENCE_MANIFEST_SPEC.md`, `SCHEMA_INVENTORY_SPEC.md`, `FINGERPRINT_SPEC.md` | Manifesto, inventário, fingerprint reproduzíveis |
| 14 | Fonte do schema (gabarito) | `specs/SCHEMA_SOURCE_MANIFEST.md` | Formato vs. fonte; fonte pendente |
| 15 | Custódia dos artefatos | `specs/PACKAGE_IMPORT_MANIFEST.md` | Importar com hash ≠ executar |

---

## 6. Dependências

- **D1.** Existência e acesso ao repositório `denistein2/AgentFactory` (execução Git fica para depois da aprovação).
- **D2.** Definição da **fonte oficial do schema-only** — ver `ORIGEM_SCHEMA_ONLY.md`, item de decisão necessária (como extrair schema sem dados e sem tocar HOMOLOG de escrita).
- **D3.** Resolução formal da porta 54329 (reserva WinNAT) — pendência carregada da Fase 01.
- **D4.** Disponibilidade parcial dos artefatos: a fonte v0.2 contém
  `sanitize_v2.py`, `columns.json` e scripts 01–04. O pacote original
  v0.3-phase01 e os scripts 00 e 05–10 continuam ausentes.

---

## 7. Riscos (resumo; detalhe nos documentos próprios)

- **R1.** `columns.json` está sob custódia, mas não foi auditado nem cruzado com
  `cells_masked=24`; a dependência no schema-only também não foi decidida.
- **R2.** PII/segredo residual mesmo em schema-only (comentários, defaults, literais em funções/policies).
- **R3.** Bloqueio remoto atual é só guard de ambiente, não controle estrutural.
- **R4.** Semântica Supabase (RLS/JWT/`SECURITY DEFINER`/`search_path`) não reproduzível por restauração ingênua de schema.
- **R5.** Porta 54329 não provada neste host.
- **R6.** Tentação de "melhorar" schema durante a cópia — proibida por contrato.
- **R7.** Na fonte v0.2: `-WithData` contradiz schema-only;
  `source_project_ref` está hardcoded; o self-test usa referências realistas à
  Dolce; o residual scan cobre PII limitada; `jsonb`/texto livre está aberto; o
  restore pode deixar estado parcial; o seed é skeleton com `ROLLBACK`.

---

## 8. Sequência futura proposta (não executada — corrige P0-01)

A sequência anterior era **circular**: pedia reprodução do E2E (execução) *antes*
de aprovar o Gate, enquanto proibia execução antes do Gate. Agora há **dois
gates** e a reprodução E2E fica **depois** do 02-B.

```
decisão schema-only  (feita)
→ pacote documental coerente  (esta revisão)
→ GATE 02-A  (preparação: estático/sem container)
   • versionar documentação (commit-base) — condição #1
   • reconciliar o pacote original v0.3-phase01 quando localizado, com custódia/hashes
   • auditoria ESTÁTICA de código (sanitize_v2/columns.json/00–10)
   • preencher MATRIZ_DEPENDENCIA_FASE01 por inspeção
   • decidir fonte autoritativa do schema (SCHEMA_SOURCE_MANIFEST)
   • construir fixtures como arquivos
   • especificar isolamento estrutural + contratos de evidência
→ baseline e hashes fixados
→ GATE 02-B  (execução: sobe container)
   • extrair schema-only da fonte decidida (leitura, inspeção offline)
   • provar isolamento estrutural em preflight
   • carregar fixtures; rodar cenários; REPRODUZIR E2E (nível definido)
   • coletar evidências (manifesto/fingerprint/inventário); destruir laboratório
→ auditoria pós-execução
```

Cada passo sujeito ao gate correspondente. **Reprodução E2E é execução** e
pertence ao 02-B (fronteira 02-A estrita, decidida por Denis). Dados reais
permanecem proibidos em todo o trajeto; pertencem a missão separada de incidente.

---

## 9. Pendências e decisões necessárias (não preenchidas por suposição)

- **PEND-1.** Método oficial de extração do schema-only sem tocar escrita em HOMOLOG — **decisão necessária**.
- **PEND-2A.** Localização/custódia de `columns.json` — **RESOLVIDA**.
- **PEND-2B.** Auditoria técnica de `columns.json` — **ABERTA**.
- **PEND-2C.** Cruzamento `cells_masked=24 × columns.json` — **ABERTA**.
- **PEND-2D.** Dependência de `columns.json` no schema-only — **ABERTA**.
- **PEND-3.** Destino do porto canônico (54329 vs. 55439 vs. outro) — **decisão necessária**.
- **PEND-4.** Escopo exato de grants/roles reproduzíveis vs. simulados no Supabase — **hipótese a validar** (ver `VALIDACAO_SUPABASE.md`).
