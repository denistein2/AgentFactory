# GOVERNANCE — Stein Agent Factory

Regras canônicas de governança. Este arquivo indexa; os documentos detalhados vivem em `docs/governance/`.

## 1. Autoridade semântica

Quando a pergunta é **qual regra/decisão governa o comportamento**, vale:

```text
M17/M18 → decisões atuais → Gate → contrato → plano-mestre → especificações → matriz/relatório
```

- **M17 — Fronteira do Executor** (`docs/governance/M17_FRONTEIRA_EXECUTOR.md`): o executor realiza operações mecânicas dentro do escopo autorizado; Denis decide Gates.
- **M18 — Decisão Humana Substitutiva** (`docs/governance/M18_DECISAO_HUMANA_SUBSTITUTIVA.md`): o agente alerta uma vez, a decisão humana posterior prevalece no escopo registrado e o histórico não é apagado.

## 2. Resolução de current-state

Autoridade semântica e estado atual são dimensões diferentes. Para claims sobre **onde está**, **qual versão existe**, **qual lifecycle vale**, **qual branch/ref foi observada** ou **se algo ainda está pendente**, resolver nesta ordem:

1. ref/commit Git explicitamente observado;
2. path real existente nessa ref;
3. lifecycle explícito (`CURRENT`, `ACTIVE_MISSION`, `HISTORICAL`, `SUPERSEDED`, `IMPORTED_UNAUDITED`, `EXTERNAL_CONTEXT`);
4. `last_verified_at` e proveniência;
5. somente depois, texto de plano, handoff ou snapshot histórico.

`docs/governance/FACTORY_LOGBOOK.md` é o índice temporal mínimo. Ele **não substitui M17/M18 nem decisões atuais**; resolve current-state e aponta a fonte verificada.

Regra crítica: **um documento não prova que continua atual apenas porque seu corpo diz “canônico”, “atual” ou “única árvore válida”.**

## 3. Padrões transversais

- `docs/governance/PROVENANCE_STANDARD.md` — proveniência mínima de claims materiais.
- `docs/governance/MISSION_MANIFEST_STANDARD.md` — identidade da missão, executor solicitado/real, timestamps, permissões e evidência.
- `docs/governance/AGENT_ROUTING_HEURISTIC.md` — seleção por capacidade/risco/reversibilidade antes de provider/modelo.
- `docs/governance/FACTORY_LOGBOOK.md` — timeline + índice de current-state.

Esses padrões foram incorporados à `main` pela PR #4 (`GOVERNANCE-RESET-FACTORY-001`) em 2026-09-26. Mudanças posteriores continuam sujeitas aos Gates aplicáveis.

## 4. AgentSpec — contrato persistente do executor

Quando esta versão estiver presente em `main`, **AGENTSPEC-001** governa a especificação persistente de identidade, capacidades, superfícies, permissões P0–P4, calibração, writes escopados e Human Gates do executor:

- `docs/governance/AGENTSPEC_001_AGENT_SPECIFICATION_PROTOCOL.md`;
- `templates/AGENTSPEC_TEMPLATE.md`.

### Regra de transição

- agentes/executores novos precisam de AgentSpec compatível antes da primeira missão material;
- executores já existentes **não ficam globalmente bloqueados retroativamente** apenas porque missões históricas ocorreram antes da adoção do protocolo;
- no próximo uso material de um executor existente, ou após mudança relevante de runtime/tooling/permissões, criar ou revalidar a AgentSpec antes do dispatch;
- observação P0 e calibração estritamente necessárias para construir/revalidar a AgentSpec podem ocorrer sob a governança vigente; isso não equivale a missão material de produto;
- missões históricas encerradas não são reabertas somente para produzir AgentSpec retroativa.

Somente `AGENT_READY` ou `AGENT_READY_WITH_SCOPED_ALLOWLIST` liberam uma missão material governada pelo protocolo.

### Does not prove

A presença de uma AgentSpec:
- não prova capability real sem evidência/calibração;
- não concede permissões além da Mission e da governança;
- não satisfaz por si só o DoD executável da Issue #8 nem substitui contratos/runtime de ferramentas;
- não autoriza merge, deploy, banco vivo, secrets ou outra consequência P3.

## 5. Princípios permanentes

1. `coerência documental ≠ reprodução de execução ≠ auditoria de código`.
2. Preservar antes de limpar.
3. Hash antes de decidir duplicidade.
4. Mesmo nome ≠ mesmo conteúdo.
5. ZIP/TAR é transporte/evidência, não fonte canônica por si só.
6. Não-erasura: substituído vai para histórico/superseded com sucessor explícito.
7. Divulgação honesta: desvios revertidos continuam registrados.
8. Fonte única por tipo de artefato.
9. `UNKNOWN`/`UNVERIFIED` é preferível a inferir identidade, modelo, horário ou estado.
10. Issue/mission contract pode **restringir** permissões herdadas; não ampliá-las silenciosamente.

## 6. DBTWIN-002

- Gate 02-A — preparação estática, não aprovado.
- Gate 02-B — execução/container, indisponível até 02-A e pré-condições.
- Esta governança não autoriza Docker, Supabase, HOMOLOG, produção ou dado real.

## 7. Protocolos

- `docs/governance/AGENTSPEC_001_AGENT_SPECIFICATION_PROTOCOL.md` — contrato persistente do executor; readiness depende de evidência/calibração.
- `docs/governance/PROTOCOLO_EXCHANGE_01.md` — transferência Drive↔Local sintética.
- `docs/governance/PROTOCOLO_CROSSAUDIT_01.md` — dupla construção/auditoria cruzada; caro e não padrão.
- `SESSION_CLOSE_PROTOCOL.md` — fechamento de sessão e Draft PR.

Protocolos específicos podem nomear produtos/agentes para um experimento, mas não substituem a heurística genérica de routing.

## 8. Fronteira Git

Sessão que altera o projeto usa branch de sessão, validação, commit/push da branch e Draft PR. Push direto em `main` é proibido. **Merge é exclusivamente humano.**

Políticas legadas em `package/stein-db-twin/` permanecem subordinadas a esta governança raiz.
