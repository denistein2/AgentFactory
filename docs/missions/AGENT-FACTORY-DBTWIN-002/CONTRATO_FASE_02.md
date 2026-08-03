# CONTRATO_FASE_02 — Fase 02 do Banco Gêmeo (schema-only)

> **Correção residual (parecer):** a fonte oficial NÃO está definida; será definida em `specs/SCHEMA_SOURCE_MANIFEST.md` (PEND-1). O formato (schema-only) está definido.


**Missão:** AGENT-FACTORY-DBTWIN-002 (planejamento) → habilita a Fase 02 (execução futura)
**Origem oficial:** schema-only estrutural + comportamental
**Status:** Minuta de contrato. **Não** autoriza execução.
**Data:** 01/08/2026

> Este contrato define **o que a Fase 02 será** quando (e se) for autorizada. A
> autorização é ato humano separado, registrado no `GATE_HUMANO_FASE_02.md`.
> Nenhuma cláusula aqui inicia a Fase 02.

---

## 1. Separação de camadas (fundamental)

O contrato distingue quatro camadas que não devem colapsar:

| Camada | Quem | O quê | Nesta sessão |
|---|---|---|---|
| **Planejamento** | agente | produzir este pacote | ✅ em andamento |
| **Autorização** | Denis (humano) | decidir o Gate | ⏸ pendente, futuro |
| **Execução** | executor local | rodar comandos mecânicos aprovados | ⛔ não autorizada |
| **Auditoria** | GPT / Claude / Denis | verificar evidências pós-execução | ⏸ futuro |

---

## 2. Escopo da Fase 02

**Dentro do escopo:**
- Reproduzir localmente o gêmeo **estrutural e comportamental** do produto a partir de schema-only.
- Popular o gêmeo com **fixtures sintéticas próprias**.
- Provar comportamentos (constraints, RLS, triggers, RPCs, invariantes de domínio) contra cenários normais, de borda e adversariais.
- Produzir evidência reproduzível e versionável.

**Fora do escopo:**
- Qualquer uso de dados operacionais reais.
- Conexão de escrita a HOMOLOG ou produção.
- Declaração de paridade sem evidência.
- Aplicação da #7730.
- Melhoria/refatoração de schema, RLS ou grants (fica para missão de evolução própria).

---

## 3. Entradas

- **E1.** Schema-only do produto, extraído da **fonte oficial** definida em `ORIGEM_SCHEMA_ONLY.md` (método a decidir — PEND-1), somente-leitura, inspecionado offline antes de uso.
- **E2.** Fixtures sintéticas de `FIXTURES_SINTETICAS.md`.
- **E3.** Pacote versionado (condição #1) com commit-base.
- **E4.** Controles de isolamento/rede provados (`POLITICA_ISOLAMENTO_REDE.md`).

## 4. Saídas

- **S1.** Gêmeo local reconstruído (estrutura + comportamento), destruível.
- **S2.** Conjunto de resultados de teste por cenário (PASS/EXPECTED_FAIL) com fingerprints.
- **S3.** Evidência de isolamento (ausência de conexão remota) estrutural, não só declarativa.
- **S4.** Relatório de auditoria diferenciando os três níveis de evidência.
- **S5.** Delta versionado no repositório.

---

## 5. Atores e responsabilidades

- **Agente:** alerta, documenta, recomenda, planeja; propõe comandos; **não** executa nem inicia gates.
- **Denis (decisor):** decide gates; titular das decisões substitutivas; não é barramento de comandos (M17).
- **Executor local:** roda comandos mecânicos **apenas** dentro do escopo aprovado.
- **Auditores (GPT/Claude/Denis):** verificam evidências; leituras independentes ≠ reproduções independentes, salvo quando explicitado.

---

## 6. Invariantes (devem valer em toda a Fase 02)

- **I1.** Nenhum dado real de cliente entra no laboratório.
- **I2.** Nenhuma escrita atinge HOMOLOG real (`bucphzinpsndsagonwiq`) ou produção.
- **I3.** Bind de serviço apenas em loopback; sem exposição em interface pública.
- **I4.** Nenhum dump com dados reais é versionado.
- **I5.** Fingerprints determinísticos: mesma entrada → mesmo resultado.
- **I6.** Reprodução é fiel; nenhuma "correção" silenciosa de schema/RLS/grants.
- **I7.** Toda escrita passa por **preflight automático** e **STOP técnico
  automático** (executor); **confirmação humana** só para destrutivo/irreversível/
  expansão de escopo/mudança de destino (M18 §3) — não para toda escrita (respeita
  M17). Ver `POLITICA_ISOLAMENTO_REDE §4`.

---

## 7. Proibições explícitas

- Dado real, dump de HOMOLOG, conexão Supabase de escrita, produção, #7730, declaração de paridade sem evidência, clonagem de `auth.users`/sessões/identidades/segredos/roles internas, melhoria oportunista.

---

## 8. Critérios de aceite (da execução futura, quando autorizada)

Uma execução da Fase 02 é aceitável somente se **todos** forem verdadeiros:

- **A1.** Objetos do schema-only reconstruídos conforme `ORIGEM_SCHEMA_ONLY.md`, com inventário conferido.
- **A2.** Fixtures sintéticas carregadas de forma determinística.
- **A3.** Cenários normais passam; cenários adversariais falham como esperado, **sem estado de domínio parcial e com manifesto de evidência completo** (ver `FIXTURES_SINTETICAS §4`).
- **A4.** Isolamento de rede provado **estruturalmente** (não só por guard).
- **A5.** Evidência versionada com delta rastreável.
- **A6.** Relatório separa coerência documental, reprodução de execução e auditoria de código.
- **A7.** Nenhuma invariante da seção 6 violada.

## 9. Critérios de parada (STOP)

A execução para imediatamente e escala para decisão humana se:

- **STOP-1.** Detecção de qualquer dado real no material de origem.
- **STOP-2.** Tentativa de conexão a destino fora da allowlist.
- **STOP-3.** Necessidade de escrita em destino não confirmado.
- **STOP-4.** Divergência de fingerprint não explicada.
- **STOP-5.** Ausência de artefato exigido no momento em que é necessário (ex.: `columns.json` ausente ao cruzar `cells_masked`, **se** a `MATRIZ_DEPENDENCIA_FASE01` o marcar como usado no fluxo schema-only; ou divergência de inventário de objetos).
- **STOP-6.** Qualquer solicitação que exija ampliar escopo além do autorizado.

---

## 10. Evidências exigidas

Para cada execução: logs de preflight/self-test; inventário de objetos; hashes de fixtures; resultados por cenário com fingerprints; prova de isolamento de rede; manifesto final coerente; e o registro de qual nível de evidência cada item representa.

Formato obrigatório em `docs/specs/`: `EVIDENCE_MANIFEST_SPEC.md`,
`SCHEMA_INVENTORY_SPEC.md`, `FINGERPRINT_SPEC.md` (corrige P0-08). Sem esses
contratos, "determinístico/bit a bit/delta verificável" é declarativo.

## 11. Critérios de destruição e limpeza (P2-02)

Como critério **final** de aceite da execução, preservando o padrão positivo da
Fase 01: container removido; volume removido; rede removida; listener encerrado;
arquivos temporários removidos; credenciais efêmeras invalidadas; evidência final
de host limpo registrada no manifesto.

## 12. Proveniência e pinagem de ambiente (P2-03)

Fixar e declarar no manifesto: versão **e digest** da imagem PostgreSQL; versão
de Docker/Compose; versões das extensões; locale/timezone/collation; arquitetura;
ferramentas de dump/restore; dependências Python e checksums. Sem pinagem, o mesmo
schema pode produzir resultados diferentes entre ambientes (mina o determinismo
de I5).

## 13. Dois gates (P0-01)

Este contrato é habilitado por **dois** atos humanos separados, não um:
**Gate 02-A** (preparação, estático/sem container) e **Gate 02-B** (execução).
Ver `GATE_HUMANO_FASE_02.md`. Nenhuma cláusula deste contrato inicia qualquer
fase.
