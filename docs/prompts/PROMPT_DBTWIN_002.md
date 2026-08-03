# PROMPT — Retomada — AGENT-FACTORY-DBTWIN-002

Cole o texto abaixo como mensagem de abertura da próxima sessão. O handoff canônico (`HANDOFF_DBTWIN_001.md`) deve estar no contexto do projeto.

---

```
Você está operando no projeto 02 — Stein Agent Factory.

A missão AGENT-FACTORY-DBTWIN-001 encerrou a Fase 01 Sintética como CANDIDATA,
com governança preservada, e aguarda apenas o Gate Humano formal. O handoff
canônico está anexo (HANDOFF_DBTWIN_001.md); trate-o como fonte única.

Estado atual:
- Docker Desktop, WSL2, Docker Engine e Compose operacionais na estação (infra).
- Evidência documental declara v0.3-phase01/PHASE_01_CANDIDATE; o pacote-fonte
  original não está sob custódia. A única fonte importada é v0.2, não auditada.
- Nenhum dado real; nenhuma conexão com HOMOLOG, Supabase ou produção.
- Nenhuma alegação de paridade; nenhuma autocertificação.

Princípio permanente (definição oficial do nível de evidência):

    coerência documental  ≠  reprodução de execução  ≠  auditoria de código

A aprovação da Fase 01 foi verificação de consistência documental — NÃO
reprodução de execução nem auditoria de código. Não trate PASS anterior como
corretude de código verificada.

Limites inegociáveis nesta sessão:
1. Dado real, dump de HOMOLOG, conexão Supabase, produção e aplicação da #7730
   permanecem PROIBIDOS até autorização humana específica e explícita.
2. A Fase 02 NÃO está autorizada a iniciar. Nenhuma ação minha a inicia.
   Denis decide os gates humanos; eu não os presumo.
3. NÃO reabrir a Fase 01. NÃO reexecutar Docker. NÃO repropor correções já
   aprovadas.

Fronteira M17: o executor local roda todos os comandos mecânicos; Denis decide
apenas os gates humanos futuros e não serve de barramento de comandos.

Antes de qualquer proposta técnica, faça nesta ordem:
1. Reconstrua mentalmente o estado da missão a partir do handoff.
2. Explique o estado atual da fábrica em suas próprias palavras.
3. Confirme explicitamente que compreendeu os limites da Fase 01 e desta sessão.

Somente depois, produza o planejamento da AGENT-FACTORY-DBTWIN-002, cujo objetivo
é PREPARAR a Fase 02 sem executá-la. Entregáveis exclusivamente de planejamento:
- contrato da Fase 02;
- Gate Humano da Fase 02;
- estratégia de auditoria (inclui reprodução independente do E2E e cruzamento
  de cells_masked contra columns.json);
- estratégia de versionamento Git (repo, commit-base, ignorados, evidência de
  delta) — esta é a condição #1 e o ponto de partida sugerido;
- definição da origem oficial do schema;
- política de rede que prove bloqueio remoto além de guards de ambiente;
- plano de validação de roles, RLS, funções, triggers, extensões, search_path,
  auth/JWT e semântica Supabase.

Não executar a Fase 02. Não usar dados reais. Não conectar em HOMOLOG nem em
produção. Aguardar decisão humana para qualquer avanço de escopo.

Se algo no handoff estiver ambíguo ou faltando, pergunte antes de assumir.
```
