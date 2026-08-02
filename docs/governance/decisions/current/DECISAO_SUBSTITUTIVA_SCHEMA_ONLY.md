# DECISÃO HUMANA SUBSTITUTIVA — Schema-only como origem oficial da DBTWIN-002

**Projeto:** 02 — Stein Agent Factory
**Missão:** AGENT-FACTORY-DBTWIN-002
**Regra de governança aplicável:** M18 — Decisão Humana Substitutiva e Não Reabertura
**Data:** 01/08/2026
**Status:** Registrada e canônica no escopo abaixo
**Substitui:** decisão do dump completo de 31/07/2026 — original em `governance/decisions/history/2026-07-31_DECISAO_DUMP_COMPLETO__ORIGINAL.md`

---

```text
DECISÃO HUMANA SUBSTITUTIVA

Responsável:
Denis Stein — responsável pelo projeto e prestador do serviço ao cliente.

Decisão:
Estabelecer o SCHEMA-ONLY como origem oficial e única do fluxo principal da
Fase 02 da AGENT-FACTORY-DBTWIN-002. O gêmeo desta missão é estrutural e
comportamental: reproduz fielmente a arquitetura e o comportamento do produto
(tabelas, tipos, enums, constraints, índices, sequences, views, materialized
views, funções, RPCs, triggers, RLS, policies, grants, extensões e os contratos
entre objetos), SEM transportar dados operacionais reais de clientes.

Os dados necessários aos testes serão fixtures sintéticas próprias:
determinísticas, relevantes, mínimas, versionáveis e adversariais quando
preciso. Nenhuma fixture será derivada de Roger, Kellen ou de qualquer cliente
real.

Regra, Gate ou decisão substituída:
A decisão do dump completo de 31/07/2026 (original preservado em history/), que autorizava o
planejamento com o dump completo Testbank.sql como origem principal e mantinha
schema-only apenas como fallback. Essa decisão fica SUBSTITUÍDA: o dump completo
deixa de ser origem principal E deixa de ser trilha paralela da Fase 02.

Escopo da substituição:
- origem oficial: schema-only do produto (definição em ORIGEM_SCHEMA_ONLY.md);
- dados de teste: fixtures sintéticas próprias (FIXTURES_SINTETICAS.md);
- fora do fluxo principal: Testbank.sql e qualquer dump com dados reais;
- repositório: denistein2/AgentFactory.

Riscos reconhecidos (apresentados pelo agente):
- schema-only reduz drasticamente o risco de PII/segredo, mas NÃO o elimina:
  comentários, defaults, dados semente embutidos em migrations, ou valores
  literais em funções/policies podem carregar informação sensível — exige
  inspeção offline mesmo em schema-only;
- reproduzir RLS/policies/grants fielmente exige cuidado para não clonar
  auth.users, sessões, identidades, segredos ou roles internas do Supabase;
- fidelidade estrutural sem dados reais pode deixar passar defeitos que só se
  manifestam com volume/estados reais — esses ficam para missão de incidente
  separada, não são objetivo desta.

Salvaguardas obrigatórias (mantidas):
- inspeção offline somente-leitura de qualquer artefato de schema antes de uso;
- nenhum dump com dados reais versionado no Git;
- credenciais e segredos fora do repositório;
- fixtures exclusivamente sintéticas e próprias;
- reprodução fiel de RLS/policies/grants SEM clonar Auth/sessões/identidades/
  segredos/roles internas;
- destino de escrita nunca é HOMOLOG real nem produção (denylist estrutural);
- primeiro fidelidade, depois evolução: nenhuma melhoria oportunista de schema,
  RLS ou grants durante a reprodução.

Ações ainda não autorizadas:
- qualquer execução nesta sessão (só planejamento);
- escrita em HOMOLOG real ou produção;
- aplicação da #7730;
- declaração de paridade sem evidência;
- uso de dados reais de cliente sob esta missão.

Fronteira futura (não proibição permanente):
O dump completo e o uso de dados reais NÃO ficam proibidos para sempre. Deixam
de ser ferramenta padrão da fábrica de evolução do produto. Caso seja necessário
reproduzir um defeito que dependa de dados reais, isso pertencerá a uma missão
separada — por exemplo AGENT-FACTORY-INCIDENT-REPRO-001 — com autorização,
isolamento, sanitização e destruição próprios, sem contaminar o laboratório
permanente.

Declaração:
O responsável declarou consciência dos riscos apresentados e, dentro da sua
autoridade sobre o projeto, esta decisão substitui a delimitação anterior no
escopo descrito.
```

---

## Rastreabilidade (M18 §7)

- **Data / responsável:** 01/08/2026 — Denis Stein.
- **Decisão anterior:** dump completo `Testbank.sql` como origem principal, schema-only como fallback (decisão do dump completo, 31/07/2026, preservada em history/).
- **Nova decisão:** schema-only como origem oficial e única do fluxo principal; dados sintéticos próprios; dump completo fora do fluxo da missão.
- **Motivo da mudança:** refinamento do propósito da fábrica — o gêmeo permanente é de **evolução do produto** (arquitetura + comportamento), distinto da **cópia de suporte/investigação** (dados/estados reais). Carregar dado real por padrão adicionaria risco, ruído e responsabilidade sem melhorar os testes.
- **Escopo afetado:** contrato, minuta de Gate, plano-mestre, especificação de origem, fixtures e matriz de rastreabilidade da Fase 02.
- **Salvaguardas mantidas:** inspeção offline, nada de dump real no Git, denylist de destino, reprodução semântica sem Auth/segredos, fidelidade antes de evolução.
- **Documentos substituídos:** decisão do dump completo (31/07/2026), marcada como substituída (não apagada): original byte-intacto em `governance/decisions/history/2026-07-31_DECISAO_DUMP_COMPLETO__ORIGINAL.md`, com marcador de status em `governance/decisions/history/2026-08-01_STATUS_SUBSTITUICAO_DUMP_COMPLETO.md`.
- **Ações executadas após a decisão:** nenhuma execução; apenas atualização documental (planejamento).

## Limite externo preservado (M18 §4)

Esta decisão prevalece sobre a governança interna do projeto. Não altera obrigações legais aplicáveis (incl. proteção de dados/LGPD), políticas obrigatórias de provedores (Supabase, GitHub, provedor do agente) nem requisitos de segurança inseparáveis da execução segura. A opção por schema-only reforça — não relaxa — esses limites.
