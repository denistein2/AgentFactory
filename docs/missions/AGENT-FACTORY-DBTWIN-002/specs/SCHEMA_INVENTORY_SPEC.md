# SCHEMA_INVENTORY_SPEC — Contrato do inventário de objetos

**Status:** minuta de especificação (planejamento). Nenhuma introspecção executada.
**Data:** 01/08/2026

> Corrige parte de P0-08 e P1-12. O inventário é a evidência versionável (sem
> dados) que prova completude estrutural do gêmeo — a base do critério "inventário
> bate objeto a objeto" do `CONTRATO_FASE_02`.

---

## 1. Objetos inventariados

Por objeto: `schema`, `tipo` (table/view/matview/function/rpc/trigger/enum/
sequence/index/constraint/policy/extension/role-grant), `nome`, `assinatura`
(quando aplicável), `dependências`, e `hash da definição DDL canonicalizada`.

## 2. Fronteira de estado (P1-12)

Distinção obrigatória entre **definição** e **estado operacional**:

| Objeto | Incluído | Excluído |
|---|---|---|
| Materialized view | definição (DDL) | conteúdo materializado |
| Sequence | definição (DDL) | valor corrente |
| Tabela | estrutura (DDL) | linhas de dado (vêm de fixtures) |

Inicialização local de matviews e sequences é determinada **pelas fixtures**,
não herdada de estado real.

## 3. Critério de completude

O gêmeo é estruturalmente completo quando o inventário extraído da fonte
autoritativa bate **objeto a objeto** com o reconstruído localmente. Diferença de
inventário é **STOP** (`CONTRATO_FASE_02` STOP-5).

## 4. Pendências

- **SI-1.** Depende da fonte autoritativa (`SCHEMA_SOURCE_MANIFEST.md`, PEND-1).
- **SI-2.** Método de canonicalização de DDL comum ao `FINGERPRINT_SPEC`.
