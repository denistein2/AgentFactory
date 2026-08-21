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

Esses padrões foram preparados por `GOVERNANCE-RESET-FACTORY-001`; tornam-se governança da `main` somente após merge humano do PR correspondente.

## 4. Princípios permanentes

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

## 5. DBTWIN-002

- Gate 02-A — preparação estática, não aprovado.
- Gate 02-B — execução/container, indisponível até 02-A e pré-condições.
- Esta governança não autoriza Docker, Supabase, HOMOLOG, produção ou dado real.

## 6. Protocolos

- `docs/governance/PROTOCOLO_EXCHANGE_01.md` — transferência Drive↔Local sintética.
- `docs/governance/PROTOCOLO_CROSSAUDIT_01.md` — dupla construção/auditoria cruzada; caro e não padrão.
- `SESSION_CLOSE_PROTOCOL.md` — fechamento de sessão e Draft PR.

Protocolos específicos podem nomear produtos/agentes para um experimento, mas não substituem a heurística genérica de routing.

## 7. Fronteira Git

Sessão que altera o projeto usa branch de sessão, validação, commit/push da branch e Draft PR. Push direto em `main` é proibido. **Merge é exclusivamente humano.**

Políticas legadas em `package/stein-db-twin/` permanecem subordinadas a esta governança raiz.
