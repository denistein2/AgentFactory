# [STATUS] Substituição da decisão do dump completo

**Natureza:** marcador de status. **Não** contém o corpo da decisão original.
**Data:** 01/08/2026
**Regra aplicável:** M18 — Decisão Humana Substitutiva e Não Reabertura (§3, §7)

> Este arquivo **apenas referencia** o original e declara seu estado atual.
> Ele **não** reproduz o corpo da decisão original e **não** afirma que o
> conteúdo integral está "abaixo". O corpo integral vive, com bytes intactos,
> no arquivo de histórico identificado pelo hash abaixo.

---

## 1. Referência ao original (bytes intactos)

| Campo | Valor |
|---|---|
| Arquivo original | `governance/decisions/history/2026-07-31_DECISAO_DUMP_COMPLETO__ORIGINAL.md` |
| SHA-256 do original | `8ab01b15a05322bb2c81a5419b9090e981d3f89c968b1b4641c9f8d4ed7e2162` |
| Estado | **SUBSTITUÍDA**, preservada no histórico, bytes intactos |
| Não editar | O corpo original permanece imutável; qualquer necessidade de correção nasce em decisão nova, nunca por reescrita do histórico |

## 2. Decisão que prevalece

| Campo | Valor |
|---|---|
| Substituída por | `governance/decisions/current/DECISAO_SUBSTITUTIVA_SCHEMA_ONLY.md` |
| Data da substituição | 01/08/2026 |
| Responsável | Denis Stein |
| Motivo | Refinamento do propósito da fábrica: o gêmeo permanente é estrutural e comportamental, não portador de dados operacionais reais. O dump completo deixa de ser origem principal e deixa de ser trilha paralela. |
| Efeito preservado | Uso futuro de dados reais não é proibido para sempre; migra para missão separada de suporte/reprodução de incidente, com autorização e controles próprios. |
| Efeito revogado | `Testbank.sql` como origem principal; schema-only como mero fallback. |

## 3. Resolução da ambiguidade de canonicidade (P0-03)

O arquivo original, lido isoladamente, ainda contém em seu corpo a expressão
"Registrada e canônica" — que era verdadeira **à época (31/07/2026)**. Como o
corpo é imutável, essa frase **não** é editada. A canonicidade atual é resolvida
**estruturalmente**, não por reescrita:

1. a **única** decisão canônica vigente é a que está em
   `governance/decisions/current/` — por definição de diretório;
2. o original vive **exclusivamente** em `history/` e nunca em `current/`;
3. este marcador, datado posteriormente, declara o original como substituído;
4. a precedência documental (`ESTRUTURA_CANONICA.md §2`) coloca
   "decisões humanas atuais" acima de qualquer histórico.

Assim, mesmo fora do contexto do README, a posição na árvore (`current/` vs.
`history/`) resolve qual decisão vale, sem depender de editar o texto histórico.
