# ORIGEM_SCHEMA_ONLY — Definição da origem oficial da Fase 02

**Formato oficial:** schema-only, gêmeo **estrutural e comportamental** (JÁ DECIDIDO)
**Fonte autoritativa:** **PENDENTE de decisão humana (PEND-1)** — ver `specs/SCHEMA_SOURCE_MANIFEST.md`
**Status:** especificação de planejamento. Nenhuma extração executada.
**Data:** 01/08/2026 (revisão pós-auditoria)

> Schema-only aqui **não** significa "apenas tabelas". Significa reproduzir a
> arquitetura e o comportamento do produto **sem dados operacionais reais**.
>
> **Correção P0-04:** "schema-only" define o **formato**, não a **fonte**. Quatro
> decisões distintas — fonte autoritativa, versão, método, artefato — vivem no
> gabarito `specs/SCHEMA_SOURCE_MANIFEST.md`. A fonte **não** está definida e
> **não** será preenchida por suposição.

---

## 1. Objetos INCLUÍDOS (conforme existirem no produto)

| Categoria | Objetos |
|---|---|
| Estrutura de dados | tabelas, colunas, tipos, domains, **enums** |
| Integridade | primary keys, foreign keys, unique, check constraints, `NOT NULL`, defaults |
| Desempenho/identidade | índices, `sequences`, identity/serial |
| Consultas derivadas | views, **materialized views** |
| Lógica | funções, **RPCs**, procedures |
| Reação | triggers e trigger functions |
| Segurança de linha | **RLS** habilitada + **policies** |
| Permissões | grants e permissões relevantes por role |
| Ambiente | **extensões** e dependências necessárias |
| Contratos | relações e contratos entre objetos (ordem de criação, dependências) |

## 2. Objetos e conteúdos EXCLUÍDOS

| Excluído | Motivo |
|---|---|
| Dados operacionais reais (linhas de negócio) | Substituídos por fixtures sintéticas |
| Fichas técnicas, produtos, clientes reais (Roger/Kellen/etc.) | Proibição canônica |
| `auth.users`, sessões, identidades | Semântica de Auth: reproduzir, não clonar |
| Segredos, chaves, JWT secrets, service_role | Nunca copiados |
| Roles internas do Supabase e objetos de sistema não reproduzíveis diretamente | Simular/mapear, não clonar |
| Storage real, buckets com conteúdo | Fora de escopo desta missão |
| Comentários/defaults/literais que carreguem PII | **Quarentena** (ver §2.1) — não remoção silenciosa |

> **Alerta R2 (repetido):** schema-only reduz, mas não zera, o risco de PII/
> segredo. A **inspeção offline somente-leitura** é pré-condição obrigatória
> antes de qualquer uso do material de schema.

### 2.1 PII × fidelidade: procedimento de quarentena (corrige P0-05)

Havia contradição: "remover comentários/defaults/literais com PII" colidia com
"nenhuma limpeza silenciosa; só registrar". Remover um comentário é inócuo, mas
remover um **default** ou um **literal dentro de função/policy** altera a
semântica reproduzida. Substituição por **quarentena**:

1. **detectar** o item com possível PII/segredo;
2. **classificar** (comentário inócuo vs. default/literal com efeito semântico);
3. **interromper** (STOP) — não prosseguir silenciosamente;
4. **registrar** o objeto afetado;
5. **decidir explicitamente** entre:
   - excluir o objeto do gêmeo e **declarar perda de fidelidade**;
   - substituir por **valor sintético semanticamente equivalente**;
   - corrigir a fonte em **missão própria**;
   - cancelar a extração.

Nenhuma alteração é silenciosa. A escolha entre (a)–(d) é registrada como achado,
coerente com "primeiro fidelidade, depois evolução".

## 3. Fonte e método de extração — DECISÃO NECESSÁRIA (PEND-1)

As quatro decisões (fonte autoritativa, versão, método, artefato) vivem em
`specs/SCHEMA_SOURCE_MANIFEST.md` e **não** são preenchidas por suposição. As
opções candidatas de método (Op-A `pg_dump --schema-only`; Op-B migrations
versionadas; Op-C introspecção de catálogo) estão lá, cada uma obrigada a provar:
(1) ausência de linhas de dado na saída; (2) captura de RLS/policies/grants/
funções/triggers; (3) nenhum toque de **escrita** na origem.

**Vinculado ao Gate:** A-PC6 (gabarito pronto) e B-PC4 (fonte definida).

## 4. Critério de completude do gêmeo estrutural

O gêmeo é considerado estruturalmente completo quando um **inventário de objetos** extraído da origem bate, objeto a objeto, com o reconstruído localmente — diferença de inventário é STOP (`CONTRATO_FASE_02` STOP-5). O inventário é evidência versionável (sem dados).

## 5. Fronteira "fidelidade antes de evolução"

Nenhuma normalização, correção de constraint, reescrita de policy ou "limpeza" de schema ocorre nesta missão. Divergências encontradas são **registradas**, não corrigidas — correção pertence a missão de evolução própria.
