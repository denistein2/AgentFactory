# FOM-001 — Fluxo Operacional Mínimo da Stein Agent Factory

> Status nesta branch: CANDIDATE
> Issue dona: #5 — FACTORY-FOM-001
> Human Gate owner: Denis Stein

## 1. Definição

Para a Agent Factory, **FOM** passa a significar, nesta proposta, **Fluxo Operacional Mínimo**.

A expansão é proposta porque a própria Issue #5 já registra o uso histórico de FOM como “fluxo operacional mínimo/core”. Ela só se torna canônica após merge humano desta branch.

O FOM é o menor circuito executável capaz de receber uma Mission, reconstruir current-state suficiente, selecionar um executor elegível, executar uma ação permitida, gerar evidence/provenance, verificar o resultado, respeitar Gates e encerrar com artifact + handoff recuperáveis.

## 2. Fluxo mínimo

```text
Mission Intake
→ Current-State / Context Bootstrap
→ Capability Routing
→ Executor / Tool Use
→ Trace + Evidence / Provenance
→ Verification / Gate
→ Artifact / Result
→ Handoff + Session Close
```

## 3. Contrato por etapa

| Etapa | Entrada mínima | Saída mínima | STOP |
|---|---|---|---|
| Mission Intake | manifest versionado | Mission validada | campo obrigatório ausente / escopo incorreto |
| Current-State Bootstrap | base_ref + base_sha observado | contexto com ref explícita | SHA stale/divergente |
| Capability Routing | capabilities + permissions | executor elegível | nenhum executor elegível |
| Executor / Tool Use | fixture sintética + executor | resultado determinístico | surface/permissão não autorizada |
| Trace + Evidence | eventos materiais | trace + manifest | falha de persistência |
| Verification / Gate | expected outcome + risk | PASS/STOP/GATE | mismatch ou P3 |
| Artifact / Result | resultado verificado | artifact recuperável | conflito de idempotência |
| Handoff / Session Close | evidence pack | summary + next gate | evidência incompleta |

## 4. Reference Mission V0

A primeira missão é propositalmente pequena e sem produção:

- lê um JSON sintético versionado;
- canonicaliza o JSON;
- calcula SHA-256;
- compara com hash esperado;
- roteia somente para um executor built-in com capabilities explícitas;
- grava evidence local de forma atômica;
- recusa permissões de rede, banco vivo, produção, secrets, deploy, merge e destruição.

Isso prova o **circuito**, não a utilidade de negócio do ERP.

## 5. Retry e idempotência

O `run_id` é determinístico por:

`mission_id + idempotency_key + base_sha + input_hash + FOM_VERSION`.

A publicação do evidence pack é atômica:
- artefatos são escritos em diretório temporário;
- falha antes do commit remove o staging;
- só depois ocorre rename atômico para o diretório final;
- replay com mesma identidade retorna `IDEMPOTENT_REPLAY`;
- saída existente conflitante causa `STOP`.

## 6. Gate

A Reference Mission é LOW risk, sintética e reversível. Não requer Human Gate durante o run.

Human Gate permanece obrigatório para:
- merge;
- produção;
- banco vivo/DDL/migration apply;
- secrets;
- deploy;
- destruição real;
- ampliação canônica de autoridade.

O merge desta proposta é o Gate que promove FOM-001 a canônico.

## 7. Evidence Pack mínimo

Cada run produz:

- `manifest.json`
- `trace.jsonl`
- `result.json`
- `handoff.json`
- `run_summary.json`

Campos materiais incluem `mission_id`, `run_id`, executor solicitado/real, base SHA, timestamps, permissions, hashes, verdict e `does_not_prove`.

## 8. FOM CLOSED — Definition of Done

FOM pode ser declarado CLOSED somente quando:

- FOM está versionado em main;
- a Reference Mission executa intake → close;
- o run é reproduzível;
- replay idempotente não duplica efeito;
- falha controlada não deixa side effect final;
- stale base produz STOP;
- permissão proibida produz STOP;
- evidence pack permite reconstrução sem transcript privado;
- merge continua Human Gate;
- documentação diferencia FOM de pós-FOM.

## 9. Pós-FOM

Issues #6–#10 não entram automaticamente.

Elas são puxadas quando um gargalo comprovado exigir:
- #6 eval harness;
- #7 trace/evidence runtime mais amplo;
- #8 generic tool contracts;
- #9 durable context/resume;
- #10 capability router baseado em evidência.

## 10. Does not prove

Este FOM V0 não prova:
- tool registry genérico;
- multiagente;
- DB Twin;
- produção;
- browser smoke test;
- durable resume distribuído;
- capability routing entre múltiplos modelos;
- segurança do ERP Food Control.
