# FOM-001 — Fluxo Operacional Mínimo da Stein Agent Factory

> Status: CURRENT_IN_MAIN / HARDENING 0.1.2
> Issue dona: #5 — FACTORY-FOM-001
> Human Gate owner: Denis Stein

## 1. Definição

Para a Agent Factory, **FOM** significa **Fluxo Operacional Mínimo**.

O FOM é o menor circuito executável capaz de receber uma Mission, reconstruir current-state suficiente, selecionar um executor elegível, executar uma ação permitida, gerar evidence/provenance, verificar o resultado, respeitar Gates e encerrar com artifact + handoff recuperáveis.

A versão 0.1.0 foi promovida a `main` via PR #15. A versão 0.1.1 foi o hardening A+D inicial; a versão 0.1.2 corrige identidade de replay e explicita as políticas de base.

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
| Current-State Bootstrap | base_ref + política e base declaradas | ref resolvida pelo Git local | SHA stale/divergente / ref não resolvida |
| Capability Routing | capabilities + permissions | executor elegível | nenhum executor elegível / permissão usada não autorizada |
| Executor / Tool Use | fixture sintética + executor | resultado determinístico | surface/permissão não autorizada |
| Trace + Evidence | eventos materiais | trace + manifest + provenance | falha de persistência / material não corresponde a HEAD |
| Verification / Gate | expected outcome + risk | PASS/STOP/GATE | mismatch ou P3 |
| Artifact / Result | resultado verificado | artifact recuperável | conflito/integridade de idempotência |
| Handoff / Session Close | evidence pack | summary + next gate | evidência incompleta |

## 4. Reference Mission V0

A missão é pequena, sintética e sem produção:

- lê JSON sintético versionado;
- canonicaliza o JSON;
- calcula SHA-256;
- compara com hash esperado;
- roteia somente para executor built-in com capabilities explícitas;
- exige permissões realmente usadas;
- grava evidence somente sob a superfície `repo/evidence`;
- persiste provenance do runtime/mission/fixture;
- recusa rede, banco vivo, produção, secrets, deploy, merge e destruição.

Isso prova o **circuito**, não a utilidade de negócio do ERP.

## 5. Current-state

O caller não fornece SHA observado como autoridade.

O runner resolve `main` no checkout local, preferindo `refs/remotes/origin/main`, depois `refs/heads/main`. Ele não faz fetch; caller/CI deve garantir que o remote ref esteja atualizado quando precisar de frescor remoto. A provenance registra esse SHA observado. Para `base_sha_policy: PINNED`, ele deve ser igual a `mission.base_sha` ou a execução para com `STALE_BASE_SHA`. Para `CURRENT_MAIN`, a Mission precisa declarar `base_sha: CURRENT_MAIN`; a resolução observada passa a ser a base de execução registrada.

`MISSION_REFERENCE_HISTORICAL_2026-09-27.json` preserva o contrato histórico fixado em `76a8e408de092163c61dfa6e7b8304a8dcedba0e` e torna-se stale quando a base observada muda. `MISSION_REFERENCE_SYNTHETIC.json` é o self-test reutilizável; usa `CURRENT_MAIN` explicitamente para continuar válido após avanço de main. A política pinned continua exercitada na suite.

## 6. Retry, idempotência e integridade

O `run_id` é determinístico por:

`mission_id + idempotency_key + base_policy + declared_base + observed_base + input_hash + runtime_head_sha + execution_material_fingerprint + FOM_VERSION`.

O fingerprint cobre os blobs Git e hashes dos bytes do runner, Mission e fixture. Esses valores são calculados e comparados ao HEAD atual antes do replay. Portanto, replay só pode reutilizar a evidência da mesma identidade de execução material e do mesmo contexto Git observado.

A publicação do evidence pack é atômica:
- artefatos são escritos em staging temporário;
- falha antes do commit remove o staging;
- rename atômico publica o diretório final;
- replay com mesma identidade só retorna `IDEMPOTENT_REPLAY` se o pack estiver completo e íntegro;
- hashes de `manifest`, `trace`, `result`, `handoff` e `provenance` são verificados;
- saída ausente, incompleta, alterada ou conflitante causa `STOP`.

## 7. Gate

A Reference Mission é LOW risk, sintética e reversível. Não requer Human Gate durante o run.

Human Gate permanece obrigatório para:
- merge;
- produção;
- banco vivo/DDL/migration apply;
- secrets;
- deploy;
- destruição real;
- ampliação canônica de autoridade.

## 8. Evidence Pack mínimo

Cada run produz:

- `manifest.json`
- `trace.jsonl`
- `result.json`
- `handoff.json`
- `provenance.json`
- `run_summary.json`

O runtime registra também a identidade Git/arquivo do runner, Mission e fixture usados na execução.

## 9. CI dedicado

`.github/workflows/fom-v0.yml` executa:
- suite unitária do FOM;
- Reference Mission;
- replay idempotente;
- upload do evidence pack como artifact.

O CI usa checkout com histórico suficiente e remote ref para resolver a `main` pelo próprio Git, sem fetch dentro do runner. Executa a Mission reutilizável `CURRENT_MAIN`; a Mission histórica pinned não é usada como health check corrente.

## 10. FOM CLOSED — Definition of Done

FOM pode ser declarado CLOSED somente quando:

- FOM está versionado em main;
- Reference Mission executa intake → close;
- current-state é observado pelo runtime, não injetado pelo caller;
- run é reproduzível;
- replay idempotente não duplica efeito e detecta tamper;
- falha controlada não deixa side effect final;
- stale base produz STOP;
- permissão proibida ou necessária ausente produz STOP;
- output root fora de `repo/evidence` produz STOP;
- runtime produz provenance da execução;
- GitHub-hosted FOM CI executa suite + Reference Mission;
- evidence pack permite reconstrução sem transcript privado;
- merge continua Human Gate;
- documentação diferencia FOM de pós-FOM.

## 11. Pós-FOM

Issues #6–#10 não entram automaticamente.

Elas são puxadas somente quando um gargalo comprovado exigir:
- #6 eval harness;
- #7 trace/evidence runtime mais amplo;
- #8 generic tool contracts;
- #9 durable context/resume;
- #10 capability router baseado em evidência.

## 12. Does not prove

Este FOM V0 não prova:
- tool registry genérico;
- multiagente;
- DB Twin;
- produção;
- browser smoke test;
- durable resume distribuído;
- capability routing entre múltiplos modelos;
- segurança do ERP Food Control.
