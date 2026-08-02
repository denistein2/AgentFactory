# MATRIZ_RASTREABILIDADE — DBTWIN-002 (revisão pós-auditoria)

**Status:** planejamento. Lacunas abertas identificadas, não resolvidas por suposição.
**Data:** 01/08/2026 (revisão)

> Relaciona risco/condição/requisito ao documento responsável, à evidência futura
> e ao Gate correspondente (02-A/02-B). Onde não há resolução, a lacuna é
> declarada. **Corrige P2-04:** agora registra também os bloqueios estruturais que
> a versão anterior omitia.

---

## 1. Matriz principal

| Origem (risco/condição Fase 01) | Requisito Fase 02 | Documento responsável | Evidência futura esperada | Gate | Estado |
|---|---|---|---|---|---|
| Pacote sem controle de versão | Versionar com commit-base e delta | `VERSIONAMENTO_GIT.md` | Commit-base + diffs + tags | 02-A | ⏸ |
| `sanitize_v2.py` não auditado | Revisão estática | `ESTRATEGIA_AUDITORIA.md` F1 | Relatório de revisão | 02-A | ⏸ |
| Scripts `00–10` não auditados | Revisão estática | `ESTRATEGIA_AUDITORIA.md` F1 | Relatório de revisão | 02-A | ⏸ |
| `columns.json` sob custódia, não auditado | Auditar + cruzar | `PACKAGE_IMPORT_MANIFEST` + F1/F3 | Revisão + cruzamento | 02-A/02-B | ⛔ PEND-2B/2C/2D |
| E2E sem reprodução independente | Reproduzir E2E (nível definido) | `ESTRATEGIA_AUDITORIA.md` F2 | Fingerprints recomputados batem | 02-B | ⏸ |
| `cells_masked=24` não cruzado | Cruzar (se usado no schema-only) | `ESTRATEGIA_AUDITORIA.md` F3 | Mapeamento fechado | 02-B | ⛔/condicional |
| Fonte do schema indefinida | Definir fonte + versão + método | `SCHEMA_SOURCE_MANIFEST` | Manifesto preenchido, saída sem dados | 02-B | ❓ decisão |
| Bloqueio remoto só por guard | Controles estruturais | `POLITICA_ISOLAMENTO_REDE.md` | `remote_db_accesses=0` medido | 02-B | ⏸ |
| Semântica Supabase não provada | Plano operacional executável | `VALIDACAO_SUPABASE.md` | Cenários RLS/JWT/tenant passam | 02-B | ⏸ |
| Sem dados de teste próprios | Fixtures sintéticas c/ oracles | `FIXTURES_SINTETICAS.md` | Fixtures determinísticas versionadas | 02-A/02-B | ⏸ |
| Porta 54329 não provada | Porta configurável provada em preflight | `POLITICA_ISOLAMENTO_REDE.md §5.1` | Porta livre registrada no manifesto | 02-B | ❓ decisão |
| Risco de dado real por padrão | Schema-only + sem dump real | `DECISAO_SUBSTITUTIVA_SCHEMA_ONLY.md` | Origem sem linhas de dado | Contrato I1 | ✅ decidido |
| Risco de melhoria oportunista | Proibição contratual | `CONTRATO_FASE_02.md` I6 | Achados registrados, não corrigidos | Contrato | ✅ definido |
| PII residual em schema | Quarentena + STOP (não remoção) | `ORIGEM_SCHEMA_ONLY.md §2.1` | Log de quarentena com decisão explícita | 02-B | ⏸ |

## 2. Bloqueios estruturais da auditoria (novo — corrige P2-04)

| Achado auditoria | Correção | Documento | Estado |
|---|---|---|---|
| P0-01 circularidade do Gate | Split 02-A/02-B; E2E no 02-B | `GATE_HUMANO_FASE_02.md` | ✅ corrigido |
| P0-02 relação de fingerprints errada | Três relações separadas + spec | `FINGERPRINT_SPEC.md` | ✅ corrigido |
| P0-03 histórico da decisão inconsistente | Original intacto + marcador de status | `governance/decisions/history/` | ✅ corrigido |
| P0-04 formato ≠ fonte | Gabarito de fonte; fonte pendente | `SCHEMA_SOURCE_MANIFEST.md` | ✅ estrutura / ❓ decisão |
| P0-05 PII × fidelidade | Procedimento de quarentena | `ORIGEM_SCHEMA_ONLY.md §2.1` | ✅ corrigido |
| P0-06 legado bloqueia indevidamente? | Matriz de dependência (bloqueio até inspeção) | `MATRIZ_DEPENDENCIA_FASE01.md` | ⏸ inspeção |
| P0-07 rede não estrutural | Topologia/protocolos/DNS/medição | `POLITICA_ISOLAMENTO_REDE.md §2.1/§5` | ⏸ a provar |
| P0-08 evidência não especificada | Três specs de evidência | `docs/specs/` | ✅ minutado |
| P1-01 paths divergentes | Árvore canônica única | `ESTRUTURA_CANONICA.md` | ✅ corrigido |
| P1-02 precedência contraditória | Ordem de autoridade + obrigação de corrigir mestre | `ESTRUTURA_CANONICA.md §2` | ✅ corrigido |
| P1-03 M18 "já versionada" | Status a corrigir (doc canônico de Denis) | ver §4 | ❓ decisão de Denis |
| P1-05 STOP-gate × M17 | Três camadas; humano só no destrutivo | `POLITICA_ISOLAMENTO_REDE.md §4` | ✅ corrigido |
| P1-14 cadeia de custódia | Manifesto de importação | `PACKAGE_IMPORT_MANIFEST.md` | ✅ minutado |

## 3. Rastreabilidade da decisão humana

| Evento | Documento | Estado |
|---|---|---|
| Decisão do dump completo (31/07) — original | `governance/decisions/history/2026-07-31_DECISAO_DUMP_COMPLETO__ORIGINAL.md` | Substituída, bytes intactos |
| Marcador de status da substituição (01/08) | `governance/decisions/history/2026-08-01_STATUS_SUBSTITUICAO_DUMP_COMPLETO.md` | Ativo |
| Decisão schema-only (01/08) | `governance/decisions/current/DECISAO_SUBSTITUTIVA_SCHEMA_ONLY.md` | Canônica |
| Regra de substituição | `M18_DECISAO_HUMANA_SUBSTITUTIVA.md` | Canônica |
| Fronteira executor | M17 | Canônica |

## 4. Lacunas ainda abertas (sem resolução inventada)

- **GAP-1 (bloqueante):** custódia de `columns.json` resolvida (PEND-2A), mas
  auditoria, cruzamento com `cells_masked=24` e dependência no schema-only seguem
  abertas (PEND-2B/2C/2D).
- **GAP-2 (decisão):** fonte autoritativa + versão + método do schema-only (PEND-1 / `SCHEMA_SOURCE_MANIFEST`).
- **GAP-3 (decisão):** porta — fixar canônica ou adotar preflight de porta livre (P2-01).
- **GAP-4 (hipótese):** mapa role-produto → role-local (PEND-4).
- **GAP-5 (hipótese):** mecanismo concreto de egress-block na topologia WSL2/Docker/WinNAT.
- **GAP-6 (decisão):** exceção `!fixtures/**/*.sql` sem abrir brecha a dump real (+ controles ativos §4.1).
- **GAP-7 (inventário):** extensões exigidas pelo produto e disponibilidade no destino.
- **GAP-8 (inspeção):** preenchimento da `MATRIZ_DEPENDENCIA_FASE01` (P0-06) — bloqueio conservador até lá.
- **GAP-9 (decisão de Denis):** status de versionamento em `M18` (documento canônico) — ver §5.
- **GAP-10 (decisão):** nível exigido de reprodução independente do E2E (P1-06 / B-PC9).

## 5. Nota sobre documento canônico de Denis (P1-03)

`M18_DECISAO_HUMANA_SUBSTITUTIVA.md` afirma "Versionado em denistein2/AgentFactory",
enquanto todo o pacote diz que nenhum commit existe (versionamento é PC1). Como M18
é **documento canônico do responsável**, o agente **não** o reescreve por conta
própria: registra a inconsistência e **propõe** o texto de status —
"Status de versionamento: preparado para versionamento; ainda não comprovado" —
para decisão de Denis. Após o commit real, registrar commit e caminho.

## 6. Nível de evidência

Nenhum item ✅ representa **corretude de código provada**, salvo os que passarem
por F1/F2/F3. Os ✅ atuais são **decisões e definições de planejamento** ou
**correções documentais**, não execução verificada.
