# AgentFactory — Stein Agent Factory

Repositório de governança, planejamento e código sob custódia da **Stein Agent Factory**.

> **Responsável pelos Gates e pelo merge:** Denis Stein.  
> **Regra permanente:** `coerência documental ≠ reprodução de execução ≠ auditoria de código`.

## Estado atual verificado

```text
last_verified_at: 2026-09-26
verified_main: 918387376620f6985baeb14965c7245131114b49
main: EXISTE
ORG-001: MERGEADO via PR #1
Issue #2: COMPLETED; objeto de governança REPROVADO para expansão de autonomia
Issue #3: HUMAN GATE APROVADO; PR #4 READY FOR REVIEW; merge permanece humano
PR #4 head: b180ef59d34a0c839f6f461a636784e24aaa3e51 + reconciliação documental posterior desta branch
PR #12: OPEN; AgentSpec pendente de reconciliação pós-PR #4
DBTWIN-002: Gate 02-A NÃO APROVADO; Gate 02-B indisponível
merge desta correção: NÃO AUTORIZADO automaticamente
```

O bloco acima substitui como estado atual as declarações antigas `BLOCKED_BASE_BRANCH` / `main ausente`. A contagem `90 arquivos / 89 inventariados` pertence à baseline ORG-001 de 2026-08-02 e não deve ser tratada como contagem atual sem nova verificação.

## Como resolver “o que vale agora”

A Factory separa duas perguntas:

1. **Autoridade semântica:** `GOVERNANCE.md` → M17/M18 → decisões em `docs/governance/decisions/current/` → Gate → contrato → plano → specs/matrizes.
2. **Identidade/estado atual:** ref Git observada + path real + lifecycle + `last_verified_at`, conforme `docs/governance/FACTORY_LOGBOOK.md` e `docs/governance/PROVENANCE_STANDARD.md`.

Um handoff, snapshot, documento histórico ou arquivo que diga “canônico” no próprio corpo **não se torna current por isso**. A posição, o lifecycle e a última verificação precisam concordar.

## Ecossistema atual — Brain, evidência e execução

A Agent Factory opera dentro de um ecossistema maior. As camadas não são intercambiáveis:

- **Jarvis/ChatGPT:** consciência ativa, raciocínio, recuperação de contexto e coordenação de missão.
- **Stein Brain / Obsidian:** mapa navegável de contexto, relações, decisões, gates e ponte para as fontes; não substitui verdade técnica viva.
- **Google Drive:** memória documental de longo prazo, evidência persistente, handoffs e artefatos externos/pesados.
- **GitHub:** realidade técnica versionada do repositório: código, governança, issues, PRs, commits e contratos sob custódia.
- **Fontes vivas específicas do projeto:** banco, CI, runtime e ambientes observáveis prevalecem para fatos atuais quando divergirem de memória documental.

Fluxo de abertura recomendado para uma missão:

`Brain → contexto atual → fonte viva → ação → evidência → auditoria → gate`

O Brain reduz reconstrução manual de história; ele não transforma resumo de IA em prova técnica.

## Política de benchmark e capability

Benchmark externo é **sinal de descoberta/seleção**, não autorização operacional e não prova de capability no contexto Stein.

Princípios:

1. benchmarks externos, leaderboards, posts, demos e reputação geram **hipóteses**;
2. candidatos relevantes entram em missão controlada da Factory;
3. capability é registrada por **domínio/tarefa/stack/risco**, não por ranking global;
4. evidência de execução interna, reproduzível e vinculada à missão sustenta o verdict;
5. **capability ≠ authority**: permissão continua sujeita a AgentSpec, risco, reversibilidade e Human Gates.

## AgentSpec / AGASALHO — estado de transição

O conceito de envelope de capacidades/permissões nasceu como **AGASALHO-001** e evoluiu para **AgentSpec**.

Estado atual:

- AGASALHO-001 = origem histórica do conceito;
- AgentSpec = evolução proposta na **PR #12**;
- PR #12 ainda não foi mergeada na `main` e portanto **AgentSpec ainda não deve ser tratado como contrato canônico da main**;
- após o merge humano da PR #4, a PR #12 deve ser reconciliada/rebaseada sobre a nova `main` antes da decisão humana de merge;
- até lá, documentos da PR #12 descrevem uma evolução pendente, não current-state canônico.

Sequência esperada:

`PR #4 → merge humano → confirmar novo main SHA → fechar Issue #3 → reconciliar PR #12 → decisão humana sobre AgentSpec`

## DB Twin e execução isolada — direção operacional

A Factory deve reduzir o risco de agentes sobre ambientes produtivos por meio de execução isolada e reproduzível.

Direção arquitetural vigente, sem alegar implementação completa:

- banco gêmeo / schema reproduzível como alvo de teste;
- aplicação e dependências executadas em ambiente isolado/containerizado quando aplicável;
- harness de missão sobe ambiente descartável, executa, coleta evidência e destrói o ambiente;
- artefatos relevantes, hashes, logs, métricas e verdict permanecem; lixo operacional efêmero não deve virar acervo permanente;
- produção não é ambiente de experimentação da Factory;
- nenhuma automação elimina o Gate Humano onde ele for exigido.

## Schema Context Pack — direção de contexto técnico

Para missões que dependem de banco, a Factory deve receber contexto estrutural versionado e machine-readable em vez de depender de consultas manuais repetitivas.

O **Schema Context Pack** é uma direção em validação para transportar somente metadados estruturais — tabelas, colunas, PK/FK, índices, views, funções, triggers, policies/RLS, tipos, invariantes e provenance — sem linhas de dados, PII ou segredos.

A fonte de verdade continua sendo o banco/migrations/repositório observados. O pack deve carregar origem, timestamps, refs/hashes e freshness (`CURRENT`, `STALE`, `UNKNOWN`) e ser regenerado quando a fonte estrutural mudar.

## Estrutura observada no repositório

```text
AgentFactory/
├─ README.md · CHANGELOG.md · GOVERNANCE.md · SECURITY.md · SESSION_CLOSE_PROTOCOL.md
├─ .github/                         workflows e template de PR
├─ docs/
│  ├─ governance/                   regras, decisões, padrões e políticas
│  ├─ missions/                     contratos e pacotes por missão
│  ├─ sessions/                     registros cronológicos de sessão
│  ├─ handoffs/                     handoffs preservados; não são current-state por si só
│  └─ audits/
├─ package/stein-db-twin/           fonte v0.2 sob custódia
├─ evidence/                        hashes, manifestos e relatórios
├─ tools/
├─ templates/
└─ archive/                         histórico, superseded e quarentena
```

## GitHub × Drive

- **GitHub:** verdade versionada de governança, código sob custódia, decisões, contratos, missões, sessões e PRs.
- **Drive:** custódia/intercâmbio e evidência externa/pesada. Conteúdo do Drive entra como evidência a reconciliar; não vira autoridade do repo automaticamente.

## Ordem de leitura para um novo agente

1. Brain Preflight aplicável ao projeto/sessão
2. `README.md`
3. `GOVERNANCE.md`
4. `docs/governance/FACTORY_LOGBOOK.md`
5. `docs/governance/PROVENANCE_STANDARD.md`
6. `docs/governance/MISSION_MANIFEST_STANDARD.md`
7. `docs/governance/AGENT_ROUTING_HEURISTIC.md`
8. M17/M18 e decisões `current/`
9. verificar evoluções pendentes em PRs abertas quando material para a missão
10. somente então o pacote da missão relevante

## DBTWIN-002 — estado preservado

A correção de governança **não** executa nem reabre tecnicamente DBTWIN-002.

- PEND-1: fonte autoritativa do schema-only — aberta.
- PEND-2A: localização/custódia de `columns.json` — resolvida.
- PEND-2B/2C/2D — abertas.
- PEND-3 — aberta.
- pacote-fonte original `v0.3-phase01`, scripts 00 e 05–10, `artifacts/phase01` e evidências E2E/fingerprints continuam conforme o estado documental anterior, sem nova alegação de custódia.

Nenhum dump, dado real, PII ou segredo deve entrar nesta árvore.
