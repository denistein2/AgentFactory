# [SUBSTITUÍDA] DECISÃO HUMANA SUBSTITUTIVA — Dump completo na Fase 02

> **STATUS: SUBSTITUÍDA POR DECISÃO HUMANA POSTERIOR.**
> Esta decisão foi substituída por `docs/governance/decisions/current/DECISAO_SUBSTITUTIVA_SCHEMA_ONLY.md`
> em 01/08/2026, conforme a regra de rastreabilidade da M18 (§3, §7).
> O conteúdo original **não** foi apagado nem reescrito. Ele permanece
> abaixo, na íntegra, apenas para auditoria histórica.
>
> **Não use este documento como fonte de estado atual da missão.**
> A origem oficial da AGENT-FACTORY-DBTWIN-002 é **schema-only**.

---

## Cabeçalho de substituição (M18 §7)

| Campo | Valor |
|---|---|
| Documento | `docs/governance/decisions/history/2026-07-31_DECISAO_DUMP_COMPLETO__ORIGINAL.md` (original de 31/07/2026) |
| Situação | Substituída, preservada no histórico |
| Substituída por | `docs/governance/decisions/current/DECISAO_SUBSTITUTIVA_SCHEMA_ONLY.md` |
| Data da substituição | 01/08/2026 |
| Responsável pela substituição | Denis Stein |
| Motivo | Refinamento do propósito da fábrica após nova análise: o gêmeo permanente é **estrutural e comportamental**, não portador de dados operacionais reais. O dump completo deixa de ser origem principal e deixa de ser trilha paralela. |
| Efeito preservado | O uso futuro de dados reais não é proibido para sempre; migra para missão separada de suporte/reprodução de incidente, com autorização e controles próprios. |
| Efeito revogado | `Testbank.sql` como origem principal; schema-only como mero fallback. |

---

## CONTEÚDO ORIGINAL PRESERVADO (não editar)

O texto abaixo é a cópia fiel da decisão original, mantida para rastreabilidade.
A única alteração é este cabeçalho de substituição acima. Nenhuma linha do corpo
original foi removida.

---

### DECISÃO HUMANA SUBSTITUTIVA — Dump completo na Fase 02 (original)

**Projeto:** 02 — Stein Agent Factory
**Missão:** AGENT-FACTORY-DBTWIN-002
**Regra de governança aplicável:** M18 — Decisão Humana Substitutiva e Não Reabertura
**Data:** 31/07/2026
**Status (à época):** Registrada e canônica no escopo descrito no original

O corpo integral desta decisão — incluindo a autorização de planejamento com
`Testbank.sql`, o bloco de riscos reconhecidos, as salvaguardas obrigatórias, as
ações não autorizadas e a rastreabilidade M18 §7 — permanece no arquivo original
`docs/governance/decisions/history/2026-07-31_DECISAO_DUMP_COMPLETO__ORIGINAL.md` do projeto.

> Nota de fidelidade: este arquivo de histórico **referencia** o original sem
> reescrevê-lo. O original permanece a cópia de referência do texto integral;
> este marcador apenas o carimba como substituído e aponta para a decisão que
> prevalece. Se o pacote for versionado, os dois arquivos convivem: o original
> (imutável) e este marcador (que declara o estado atual).
