# AGENTSPEC-001 — Agent Specification Protocol

> Status: CANDIDATO CANÔNICO
> Data de criação: 2026-09-20
> Dono de governança: Denis Stein
> Projeto canônico: Stein Agent Factory
> Issue dona: #8 — RUNTIME-TOOL-CONTRACTS-001
> Origem histórica: AGASALHO-001 (2026-09-18)
> Termo canônico: **AgentSpec**

## 1. Definição

**AgentSpec** é a especificação persistente de um agente/executor.

Ela define, de forma versionada e auditável:

- identidade operacional;
- objetivo e fronteira de responsabilidade;
- capacidades;
- ferramentas;
- superfícies acessíveis;
- permissões P0–P4;
- writes autorizados;
- Human Gates;
- regras de branch/worktree;
- contrato de retorno de artefatos;
- evidência mínima;
- comportamento em erro/drift;
- calibração;
- limitações conhecidas.

Uma AgentSpec não é uma Mission.

**AgentSpec define o executor. Mission define o trabalho temporário.**

## 2. Relação com SPECs do produto

A fábrica passa a distinguir explicitamente:

- **System/Product SPEC** — contrato persistente do comportamento esperado do software;
- **AgentSpec** — contrato persistente do comportamento e da autoridade do executor;
- **Issue** — unidade rastreável de trabalho/problema/evolução;
- **Mission** — instrução operacional limitada para uma execução;
- **Evidence** — prova verificável do que foi observado ou executado;
- **Audit/Review** — verificação crítica;
- **Verdict/Human Gate** — decisão de progressão.

Fluxo recomendado:

`System SPEC → Issue/Plan → Mission → Evidence → Audit → Verdict/Human Gate`

A Mission deve declarar qual AgentSpec governa o executor quando houver uma aplicável.

## 3. Origem histórica — AGASALHO-001

AGASALHO-001 nasceu em 18/09/2026 durante a integração do Antigravity no ERP Food Control.

O problema real era duplo:

1. operações triviais/read-only eram interrompidas por prompts técnicos do runtime;
2. writes e consequências materiais precisavam de fronteiras mais explícitas.

O AGASALHO formalizou capacidades, permissões P0–P4, calibração e Human Gates.

Em 20/09/2026, após a adoção oficial de **SPEC** como linguagem de engenharia nos projetos Stein Technology, o conceito foi promovido para **AgentSpec**.

AGASALHO permanece como codinome e artefato histórico de origem. O termo operacional/canônico passa a ser AgentSpec.

## 4. Trigger obrigatório

Criar ou revalidar a AgentSpec quando ocorrer qualquer um destes casos:

1. entrada de um agente/executor novo;
2. mudança relevante de modelo, runtime, CLI, plugin, MCP ou ferramenta;
3. mudança de credenciais/permissões;
4. nova superfície externa disponível;
5. repetição de prompts de permissão que transforme o humano em gargalo;
6. descoberta de acesso necessário ausente;
7. mudança material no contrato de segurança;
8. mudança de Human Gates;
9. mudança no padrão de artefatos/retorno;
10. mudança de projeto que exija overlay específico.

## 5. Gate pré-missão

Antes de qualquer missão material, responder:

> **Existe uma AgentSpec vigente e compatível com esta missão?**

Resultados permitidos:

- `AGENT_READY`
- `AGENT_READY_WITH_SCOPED_ALLOWLIST`
- `AGENT_NOT_READY_MISSING_SPEC`
- `AGENT_NOT_READY_MISSING_PERMISSION_MAP`
- `AGENT_NOT_READY_MISSING_TOOL_ACCESS`
- `AGENT_NOT_READY_AMBIGUOUS_GATE`
- `HUMAN_DECISION_REQUIRED`

Somente `AGENT_READY` ou `AGENT_READY_WITH_SCOPED_ALLOWLIST` liberam a missão material.

## 6. Convenção de nomenclatura

Protocolo geral:

`AGENTSPEC-001`

Especificação de agente:

`AGENTSPEC-<AGENT>-<NNN>`

Exemplos:

- `AGENTSPEC-ANTIGRAVITY-001`
- `AGENTSPEC-CODEX-001`
- `AGENTSPEC-ASTRA-001`
- `AGENTSPEC-CONTENT-001`

Path recomendado:

`docs/agents/<AGENT_NAME>/AGENTSPEC_<AGENT_NAME>_<NNN>.md`

Template canônico:

`templates/AGENTSPEC_TEMPLATE.md`

## 7. Taxonomia obrigatória de permissão

### P0 — OBSERVE / READ_ONLY

Não altera estado relevante.

Exemplos: status, log, show, diff, rev-parse, rev-list, merge-base, merge-tree em simulação, leitura GitHub/Drive, arquivos, artefatos e queries estritamente read-only em ambiente autorizado.

**Regra:** P0 não cria Human Gate por si só.

### P1 — SAFE_LOCAL / REVERSIBLE_LOCAL

Altera apenas estado local e reversível do executor.

Exemplos: fetch de refs, materialização de branch conhecida, worktree temporária, dependências reproduzíveis, cache/build local.

**Regra:** pode ser pré-autorizado pela AgentSpec.

### P2 — MISSION_SCOPED_WRITE

Escrita compartilhada explicitamente prevista pela Mission e permitida pela AgentSpec.

Exemplos: artefato de retorno, commit/push em branch de missão, abertura/atualização de PR, checkpoint em Issue, mirror controlado no Drive.

**Regra:** P2 não herda autoridade para mudança semântica fora do escopo.

### P3 — HUMAN_GATE / CONSEQUENCE

Ação canônica, externa, sensível ou difícil de reverter.

Exemplos: merge em main, deploy, escrita em banco vivo, DDL/migration apply, secrets, configuração sensível, decisão fiscal/financeira/comercial, exclusão destrutiva, aceite humano.

**Regra:** parar e solicitar decisão concreta.

### P4 — FORBIDDEN / UNAVAILABLE

Capacidade proibida, indisponível ou ainda não comprovada.

Nunca simular capacidade inexistente.

## 8. Inventário mínimo da AgentSpec

Cada AgentSpec deve declarar:

- Agent/executor;
- modelo/runtime quando relevante;
- cliente/CLI;
- host/ambiente quando alterar capacidades;
- projetos/repositórios autorizados;
- leitura obrigatória;
- Git local;
- GitHub;
- Google Drive;
- filesystem;
- banco local/twin;
- homolog;
- produção;
- CI;
- deploy;
- navegador/cloud browser;
- comunicação;
- plugins/MCPs;
- sistemas de terceiros.

Acesso a uma superfície nunca implica acesso automático a outra.

## 9. Runtime prompt não é Human Gate

Um prompt técnico do runtime pode existir mesmo em operação P0/P1.

Isso não transforma automaticamente a ação em decisão humana.

Quando seguro e suportado:

- preferir allowlist estreita;
- preferir escopo da conversa/sessão;
- evitar permissões globais amplas;
- mapear famílias de comandos;
- registrar limitações do provider/runtime.

**Princípio:** verificação é autônoma; consequência é gated.

## 10. Branch/worktree e proteção de estado

A AgentSpec deve declarar:

- branch canônica;
- naming de mission branch;
- política de worktree;
- comportamento em refspec restrito;
- como preservar trabalho inesperado;
- autoridade de limpeza;
- proibição de reset destrutivo sem preservação/evidência.

## 11. Artifact Return Contract

A AgentSpec deve definir o contrato de retorno padrão:

- relatório obrigatório;
- paths;
- provenance;
- commit/push permitido;
- Drive daily/canonical;
- Issue/PR checkpoint;
- evidência mínima;
- formato de verdict.

A Mission pode restringir esse contrato, mas não ampliá-lo silenciosamente.

## 12. Calibração

Antes da primeira missão real, provar quando aplicável:

1. identidade do repositório;
2. leitura de branch/HEAD/status;
3. leitura de Issue/PR;
4. leitura de CI/checks;
5. acesso a Drive/artefatos;
6. worktree/branch isolada;
7. validações locais;
8. scoped artifact write, se P2 fizer parte da AgentSpec;
9. stop correto antes de P3.

A calibração não deve tocar produção.

## 13. Definition of Ready

Uma AgentSpec está pronta quando:

- identidade e escopo existem;
- superfícies foram inventariadas;
- P0–P4 estão classificados;
- Human Gates estão explícitos;
- famílias recorrentes estão mapeadas;
- writes de retorno estão definidos;
- comportamento em erro/drift existe;
- calibração existe;
- limitações estão registradas;
- resultado é `AGENT_READY` ou `AGENT_READY_WITH_SCOPED_ALLOWLIST`.

## 14. Versionamento e arqueologia

AgentSpec é contrato vivo e versionado.

Mudanças materiais devem registrar:

- versão/data;
- motivo;
- incidente/evidência;
- permissões adicionadas/removidas;
- Human Gates alterados;
- impacto sobre Missions existentes.

Não reescrever silenciosamente a história.

## 15. Base AgentSpec e overlay de projeto

Quando o mesmo executor opera em múltiplos projetos:

- manter uma AgentSpec base para capacidades gerais;
- permitir overlay/restrição por projeto;
- a regra mais restritiva prevalece;
- a Mission referencia a AgentSpec/overlay efetivamente usado.

Isso evita duplicação divergente sem assumir que todo projeto possui a mesma superfície ou autoridade.

## 16. Cross-project propagation

Aprendizado reutilizável deve:

1. atualizar AGENTSPEC-001 na Stein Agent Factory;
2. gerar comunicação para a INBOX dos projetos impactados;
3. permitir que cada projeto incorpore overlay local;
4. preservar provenance da mudança;
5. não criar forks silenciosos do contrato.

## 17. Frase operacional

**Nenhum agente recebe missão material sem uma especificação explícita do que pode observar, preparar, escrever e onde deve parar.**
