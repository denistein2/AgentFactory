# AGASALHO-001 — Protocolo de Onboarding de Capacidade, Permissões e Envelope de Execução de Agentes

> Status: CANDIDATO CANÔNICO
> Data de criação: 2026-09-18
> Dono de governança: Denis Stein
> Projeto canônico: Stein Agent Factory
> Issue dona: #8 — RUNTIME-TOOL-CONTRACTS-001
> Codinome interno: **AGASALHO**

## 1. Por que este protocolo existe

Um agente novo não deve receber uma missão real antes de existir uma visão explícita de quais superfícies ele consegue acessar, quais ferramentas possui, o que é read-only, o que altera apenas estado local e reversível, quais escritas versionadas pertencem ao retorno normal da missão, quais ações exigem Gate Humano e quais capacidades estão indisponíveis ou não comprovadas.

O objetivo é impedir que o humano vire operador de teclado para aprovar observações triviais, sem afrouxar gates para consequências materiais.

**Regra:** antes da primeira missão de um agente, validar o envelope do agente. Se o envelope estiver incompleto, completar documentação e calibração antes de disparar trabalho material.

## 2. Princípio central

**O agente deve chegar agasalhado à missão.**

"Agasalhar" um agente significa construir sua cobertura operacional antes do uso real: identidade, capacidades, ferramentas, permissões, limites, padrões de comando, persistência de evidência e gates.

O AGASALHO não aumenta permissões automaticamente. Ele torna explícito o que já está autorizado, o que pode ser autorizado com segurança e onde a decisão humana continua obrigatória.

## 3. Trigger obrigatório

Executar AGASALHO quando ocorrer qualquer um destes casos:

1. entrada de um agente/executor novo no time;
2. mudança relevante de modelo, runtime, CLI, plugin, MCP ou ferramenta;
3. mudança de credenciais/permissões do executor;
4. nova superfície externa disponível, como GitHub, Drive, banco, deploy, e-mail ou navegador;
5. repetição de prompts de permissão que transforme o humano em gargalo;
6. descoberta de que o agente está sem acesso necessário para a missão;
7. mudança material no contrato de segurança ou nos Human Gates.

## 4. Gate pré-missão

Antes de qualquer missão material, responder:

> **Este agente já possui um envelope de capacidades e permissões compatível com esta missão?**

Resultados permitidos:

- `AGENT_READY` — envelope suficiente; missão pode ser disparada.
- `AGENT_READY_WITH_SCOPED_ALLOWLIST` — precisa apenas de allowlist temporária/conversation-scoped já documentada.
- `AGENT_NOT_READY_MISSING_PERMISSION_MAP` — inventário insuficiente; não disparar missão.
- `AGENT_NOT_READY_MISSING_TOOL_ACCESS` — ferramenta/superfície necessária indisponível.
- `AGENT_NOT_READY_AMBIGUOUS_GATE` — não está claro se determinada ação é observação, escrita reversível ou consequência material.
- `HUMAN_DECISION_REQUIRED` — a missão depende de autorização que não pode ser pré-delegada.

## 5. Artefato obrigatório por agente

Cada agente deve possuir um contrato próprio derivado de:

`templates/AGENT_CAPABILITY_PERMISSION_ENVELOPE.md`

Nome recomendado:

`docs/agents/<AGENT_NAME>/AGENT_<AGENT_NAME>_CAPABILITY_PERMISSION_ENVELOPE.md`

O contrato deve ser versionado, datado e atualizado quando a superfície operacional mudar.

## 6. Inventário mínimo do agente

Registrar identidade operacional, modelo/runtime quando relevante, cliente/CLI/aplicação, máquina/ambiente quando isso alterar capacidades, projetos/repositórios autorizados, data da calibração, responsável humano pelo gate e leitura obrigatória.

Mapear separadamente Git local, GitHub, Google Drive, filesystem, banco local/twin, homolog, produção, CI, deploy, navegador/cloud browser, comunicação, plugins/MCPs e sistemas de terceiros relevantes.

Nunca assumir que acesso a uma superfície implica acesso a outra.

## 7. Taxonomia obrigatória de permissão

### P0 — OBSERVE / READ_ONLY

Não altera estado relevante.

Exemplos: status, log, show, diff, rev-parse, rev-list, merge-base, merge-tree em simulação, listagem de branches/worktrees, leitura de Issue/PR/Actions, arquivos, artefatos e queries estritamente read-only em ambiente autorizado.

**Regra:** não criar Human Gate para P0.

### P1 — SAFE_LOCAL / REVERSIBLE_LOCAL

Altera apenas estado local do executor de forma controlada e reversível.

Exemplos: fetch de refs, materialização de branch remota conhecida, criação de worktree da missão, instalação local reproduzível de dependências, cache/build local e remoção da worktree temporária criada pela própria missão após prova de limpeza.

**Regra:** pode ser pré-autorizado pelo contrato do agente; não equivale a autorização de escrita em sistemas compartilhados.

### P2 — MISSION_SCOPED_WRITE

Escrita compartilhada explicitamente prevista pela missão e governança.

Exemplos: artefato de retorno, commit/push na branch da missão, abertura/atualização de PR, comentário de checkpoint na Issue, sincronização de artefato no Drive e correção mecânica estritamente delimitada e pré-autorizada.

**Regra:** precisa estar descrita no envelope/na missão; não herda autoridade para mudanças semânticas.

### P3 — HUMAN_GATE / CONSEQUENCE

Ação com efeito canônico, externo, operacional, sensível ou difícil de reverter.

Exemplos típicos: merge em `main`, deploy, escrita em banco vivo, DDL/migration apply, secrets/credenciais, configuração externa sensível, decisão fiscal/financeira/comercial, inventário físico, exclusão destrutiva e assinatura de aceite humano.

**Regra:** parar e pedir uma decisão concreta.

### P4 — FORBIDDEN / UNAVAILABLE

Capacidade proibida por governança, não disponível no executor ou ainda não comprovada.

Nunca simular capacidade inexistente.

## 8. Matriz de comandos e padrões

O envelope do agente deve listar famílias previsíveis de comandos/ferramentas, e não apenas exemplos isolados.

Exemplo:

- `git diff ...` → P0;
- `git merge-base ...` → P0;
- `git fetch origin <known-ref>` → P1;
- `git commit` em branch da missão para artefato previsto → P2;
- `git push` da branch da missão → P2;
- merge de PR → P3.

Evitar allowlists baseadas em comandos compostos enormes que mudam a cada execução.

## 9. Runtime prompt não é Human Gate

Um runtime pode exibir diálogo técnico de permissão mesmo para uma operação P0. Isso não converte automaticamente a operação em decisão humana.

Quando seguro e suportado:

- usar regra estreita e temporária por família de comando;
- preferir escopo da conversa/sessão;
- não persistir permissões globais amplas por padrão;
- registrar no contrato do agente quais famílias geram prompt no runtime.

## 10. Calibração inicial obrigatória

Antes da primeira missão real, executar uma missão curta de calibração para provar, quando aplicável:

1. identidade do repositório;
2. leitura de branch/HEAD/status;
3. leitura de Issue/PR;
4. leitura de CI/checks;
5. acesso ao Drive/artefatos;
6. capacidade de criar branch/worktree isolada, quando prevista;
7. capacidade de rodar validações locais;
8. capacidade de persistir um artefato de teste em branch não canônica, se P2 fizer parte do contrato;
9. capacidade de parar corretamente antes de P3.

A calibração não deve tocar produção nem exigir uma missão de negócio real.

## 11. Definition of Ready do agente

Um agente só recebe missão material quando:

- contrato próprio existe;
- ferramentas/superfícies foram inventariadas;
- permissões P0-P4 foram classificadas;
- Human Gates estão explícitos;
- comandos read-only recorrentes estão mapeados;
- writes de retorno estão definidos;
- artefato de retorno e caminhos canônicos estão definidos;
- comportamento em erro/drift está definido;
- evidência de calibração existe;
- lacunas não resolvidas estão registradas;
- resultado final é `AGENT_READY` ou `AGENT_READY_WITH_SCOPED_ALLOWLIST`.

## 12. Regra de arqueologia

Nunca reescrever silenciosamente a história operacional de um agente.

Quando o envelope mudar, atualizar versão/data, registrar motivo, preservar decisão anterior quando material, apontar qual incidente/aprendizado motivou a mudança e manter vínculo com Issue/PR/handoff/evidência.

O histórico de permissões é parte da memória da fábrica.

## 13. Cross-project propagation

Quando o aprendizado for reutilizável em outros projetos:

1. atualizar o protocolo canônico na Stein Agent Factory;
2. criar ponte para a `00_INBOX` de cada projeto impactado;
3. o projeto receptor decide como incorporar o protocolo à sua governança local;
4. não duplicar decisões divergentes sem necessidade;
5. registrar onde o contrato do agente daquele projeto passa a viver.

## 14. Incidente fundador — 2026-09-18

Durante a integração do executor Antigravity no ERP Food Control, o agente demonstrou boa utilidade operacional e baixo custo de execução, mas o runtime interrompia repetidamente operações de observação com prompts de permissão.

O gargalo não era uma decisão de segurança material. Era ausência de um envelope operacional suficientemente explícito para o agente/runtime.

O aprendizado foi transformado em contrato: distinguir Human Gate de prompt técnico, mapear famílias P0-P4, prever allowlists estreitas e temporárias, registrar comportamento de worktree/refspec, preservar artefatos antes de resets e obrigar o próximo agente a passar pelo AGASALHO antes da primeira missão.

Este incidente é tratado como marco fundador do protocolo.

## 15. Frase operacional

**Nenhum agente novo recebe missão antes de saber exatamente o que pode observar, o que pode preparar, o que pode escrever e onde precisa parar.**
