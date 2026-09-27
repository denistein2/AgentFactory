---
session_id: 2026-09-27-CURRENT-STATE-FOM-SYNC
project: Agent Factory
status: CONTEXT_SYNCHRONIZED
base_ref: main
base_sha: e5ac0c0a8c84583b072b25df6c553189fdda782d
human_owner: Denis Stein
evidence_strength: DOCUMENT_COHERENCE_PLUS_LIVE_GIT
---

# SESSION — Conversation → Project / Drive / Brain sync — 2026-09-27

## Evento técnico confirmado

- PR #12 foi mergeada por Denis.
- Nova main: `e5ac0c0a8c84583b072b25df6c553189fdda782d`.
- AgentSpec agora está presente em main.
- Não havia PRs abertas no preflight desta sincronização.

## Dor de origem — HUMAN_DECISION

A Agent Factory nasceu em parte para remover Denis do papel de barramento humano entre IA e banco: copiar queries, consultar schema repetidamente e devolver resultados manualmente.

Objetivo: remover trabalho mecânico sem retirar compreensão, evidência e Human Gate de consequências materiais.

## Direção AI First — HUMAN_DECISION

A Factory deve:
- reduzir tempo de desenvolvimento;
- automatizar trabalho repetitivo;
- acelerar evolução do produto;
- produzir evidência;
- permitir que IA trabalhe com issues, implementação, auditoria, testes e futuramente smoke tests no navegador;
- manter Denis em System Design, QA, direção de produto e relação com cliente.

Não deve virar laboratório infinito.

## Banco / DB Twin / ambiente efêmero

Direção aprovada conceitualmente:
- produção não é ambiente padrão de tentativa/erro;
- banco gêmeo / schema-only / ambiente isolado deve proteger produção;
- execução preferencialmente efêmera e reproduzível;
- padrão desejado: criar → executar → coletar evidência → destruir ambiente.

Implementação continua sujeita aos Gates do DBTWIN/FOM.

## Schema Context Pack V0

Artefato já existe no Drive como WORKING_DRAFT.

Papel:
- schema machine-readable;
- tables/columns/PK/FK/views/functions/triggers/enums/RLS;
- provenance, freshness e fingerprint;
- sem row data/secrets/PII;
- recorte por missão.

Posicionamento:
**componente candidato do bootstrap/contexto do FOM, não projeto paralelo.**

Brain guarda significado e ponte; Git/migrations/database observada seguem como fontes técnicas.

Primeiro alvo candidato: ERP Food Control.

## Produto de cliente

A Factory deve amadurecer para receber repo/schema/contexto de produto de terceiros e reproduzir o ambiente de forma segura e auditável. Isso é caso core de maturidade, não edge case.

## Outras frentes

- Arqueologia do computador local: higiene de fundação; não abrir novo produto.
- LeadGen/Laia: hipótese estacionada até o LeadGen voltar ao foco e ser testada de forma controlada.
- Portfólio: preferir um pulso diário verificável por projeto ativo, não porcentagens arbitrárias.

## Prioridade atual

1. sincronizar estado pós-PR #12;
2. #11 somente como current-state/roadmap sync mínimo;
3. entrar na #5 FOM;
4. provar missão sintética/reversível ponta a ponta;
5. puxar #6–#10 conforme gargalos reais.

Schema Context Pack e DB Twin devem servir o FOM, não competir com ele.

## DOES_NOT_PROVE

Este registro não prova:
- DB Twin executado;
- extractor do Schema Context Pack pronto;
- FOM operacional;
- smoke tests automatizados;
- produção autorizada;
- Laia adequado ao LeadGen.

## Next Gate

Merge humano do patch de current-state desta sessão.
Depois: missão própria para Issue #5.
