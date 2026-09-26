# AgentFactory — Stein Agent Factory

Repositório de governança, planejamento e código sob custódia da **Stein Agent Factory**.

> **Responsável pelos Gates e pelo merge:** Denis Stein.  
> **Regra permanente:** `coerência documental ≠ reprodução de execução ≠ auditoria de código`.

## Estado atual verificado

```text
last_verified_at: 2026-08-21T15:18:00-03:00
verified_main: 918387376620f6985baeb14965c7245131114b49
main: EXISTE
ORG-001: MERGEADO via PR #1
Issue #2: COMPLETED; objeto de governança REPROVADO para expansão de autonomia
Issue #3: HUMAN GATE APROVADO; correção preparada em branch de sessão
DBTWIN-002: Gate 02-A NÃO APROVADO; Gate 02-B indisponível
merge desta correção: NÃO AUTORIZADO automaticamente
```

O bloco acima substitui como estado atual as declarações antigas `BLOCKED_BASE_BRANCH` / `main ausente`. A contagem `90 arquivos / 89 inventariados` pertence à baseline ORG-001 de 2026-08-02 e não deve ser tratada como contagem atual sem nova verificação.

## Como resolver “o que vale agora”

A Factory separa duas perguntas:

1. **Autoridade semântica:** `GOVERNANCE.md` → M17/M18 → decisões em `docs/governance/decisions/current/` → Gate → contrato → plano → specs/matrizes.
2. **Identidade/estado atual:** ref Git observada + path real + lifecycle + `last_verified_at`, conforme `docs/governance/FACTORY_LOGBOOK.md` e `docs/governance/PROVENANCE_STANDARD.md`.

Um handoff, snapshot, documento histórico ou arquivo que diga “canônico” no próprio corpo **não se torna current por isso**. A posição, o lifecycle e a última verificação precisam concordar.

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

1. `README.md`
2. `GOVERNANCE.md`
3. `docs/governance/FACTORY_LOGBOOK.md`
4. `docs/governance/PROVENANCE_STANDARD.md`
5. `docs/governance/MISSION_MANIFEST_STANDARD.md`
6. `docs/governance/AGENT_ROUTING_HEURISTIC.md`
7. M17/M18 e decisões `current/`
8. somente então o pacote da missão relevante

## DBTWIN-002 — estado preservado

A correção de governança **não** executa nem reabre tecnicamente DBTWIN-002.

- PEND-1: fonte autoritativa do schema-only — aberta.
- PEND-2A: localização/custódia de `columns.json` — resolvida.
- PEND-2B/2C/2D — abertas.
- PEND-3 — aberta.
- pacote-fonte original `v0.3-phase01`, scripts 00 e 05–10, `artifacts/phase01` e evidências E2E/fingerprints continuam conforme o estado documental anterior, sem nova alegação de custódia.

Nenhum dump, dado real, PII ou segredo deve entrar nesta árvore.
