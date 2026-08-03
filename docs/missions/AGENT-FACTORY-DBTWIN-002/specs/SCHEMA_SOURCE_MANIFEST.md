# SCHEMA_SOURCE_MANIFEST — Fonte autoritativa do schema (gabarito)

**Status:** gabarito de planejamento. **Fonte autoritativa PENDENTE de decisão humana (PEND-1).**
**Data:** 01/08/2026

> Corrige P0-04. "Schema-only" define o **formato**, não a **fonte**. São quatro
> decisões distintas que estavam colapsadas. Este gabarito as separa. Nenhum
> campo é preenchido por suposição.

---

## 1. Distinção fundamental

```
Formato oficial:      schema-only   (JÁ DECIDIDO — canônico)
Fonte autoritativa:   PENDENTE      (decisão necessária — PEND-1)
Versão da fonte:      PENDENTE
Método de extração:   PENDENTE
Artefato resultante:  a produzir sob Gate 02-A/02-B
```

## 2. Gabarito a preencher (antes do Gate 02-B)

```text
SCHEMA_SOURCE_MANIFEST

Fonte autoritativa:        __________ (ex.: migrations do produto | catálogo do projeto X)
Versão/commit:             __________ (commit | migration head | release | timestamp)
Project reference:         __________ (se aplicável; NUNCA o HOMOLOG real bucphzinpsndsagonwiq como destino de escrita)
Data do snapshot:          __________
Método de extração:        __________ (pg_dump --schema-only | migrations | introspecção)
Ferramenta e versão:       __________
Hash do artefato (sha256): __________
Inventário esperado:       __________ (ref. SCHEMA_INVENTORY_SPEC)
Responsável pela leitura:  __________ (autorização de leitura da fonte)
```

## 3. Provas exigidas de qualquer método escolhido

1. ausência de linhas de dado na saída;
2. captura de RLS/policies/grants/funções/triggers;
3. nenhum toque de **escrita** na origem (leitura autorizada apenas).

## 4. Opções candidatas (nenhuma executada; decisão de Denis)

- **Op-A.** `pg_dump --schema-only` de cópia/leitura autorizada.
- **Op-B.** Migrations/definições já versionadas do produto (evita tocar HOMOLOG).
- **Op-C.** Introspecção de catálogo (`information_schema`/`pg_catalog`).

> Vinculado a A-PC6 (gabarito pronto) e B-PC4 (fonte definida) no Gate.
