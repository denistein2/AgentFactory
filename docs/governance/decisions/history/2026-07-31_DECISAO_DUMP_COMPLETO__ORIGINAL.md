# DECISÃO HUMANA SUBSTITUTIVA — Dump completo na Fase 02

**Projeto:** 02 — Stein Agent Factory
**Missão:** AGENT-FACTORY-DBTWIN-002
**Regra de governança aplicável:** M18 — Decisão Humana Substitutiva e Não Reabertura
**Data:** 31/07/2026
**Status:** Registrada e canônica no escopo abaixo

---

```text
DECISÃO HUMANA SUBSTITUTIVA

Responsável:
Denis Stein — responsável pelo projeto e prestador do serviço ao cliente.

Decisão:
Autorizar o PLANEJAMENTO da Fase 02 com uso do dump completo Testbank.sql,
originado de HOMOLOG, sob responsabilidade do declarante. O schema-only
permanece disponível como alternativa técnica, mecanismo de diagnóstico e
fallback de restauração, não como limitação imposta ao escopo principal.

Regra, Gate ou decisão substituída:
A opção intermediária discutida na mesma sessão de limitar obrigatoriamente
o fluxo da Fase 02 a schema-only. Essa limitação fica substituída.

Escopo da substituição:
- origem: ambiente HOMOLOG sob administração do declarante (referência
  bucphzinpsndsagonwiq), usado apenas como fonte;
- arquivo: Testbank.sql (dump completo, ~675 KB);
- destino candidato: projeto Supabase descartável snoifcvsbutigphemdpf;
- destino local posterior: PostgreSQL/pgAdmin em 127.0.0.1:55439;
- repositório: denistein2/AgentFactory.

Riscos reconhecidos (apresentados pelo agente):
- Testbank.sql é dado operacional real de HOMOLOG; o tamanho sugere que
  contém linhas de dado, não apenas estrutura;
- contém cadastros de produtos e fichas técnicas de cliente (Roger/Kellen)
  que, conforme relato, não tem conhecimento deste projeto — bandeira de
  risco registrada, decisão de titularidade e de comunicação ao cliente é
  do responsável, não do agente;
- restauração e limpeza de destino são irreversíveis;
- risco de vazamento de PII/segredo caso o dump seja versionado ou o destino
  seja confundido com produção.

Salvaguardas obrigatórias (mantidas):
- inspeção offline somente-leitura do Testbank.sql como pré-condição da
  restauração;
- Testbank.sql e qualquer dump real nunca versionados no Git;
- credenciais e segredos fora do repositório;
- limpeza destrutiva do destino com confirmação explícita e evidência do
  estado anterior;
- reprodução fiel de RLS/policies/grants sem clonar auth.users, sessões,
  identidades, segredos ou roles internas do Supabase;
- destino de escrita nunca é o HOMOLOG real bucphzinpsndsagonwiq (denylist).

Ações ainda não autorizadas:
- execução da restauração nesta sessão (só planejamento);
- escrita no HOMOLOG real;
- aplicação da #7730;
- declaração de paridade sem evidência;
- melhoria/reescrita de RLS ou grants durante a cópia.

Declaração:
O responsável declarou consciência dos riscos apresentados e, dentro da sua
autoridade sobre o projeto, esta decisão substitui a delimitação anterior no
escopo descrito.
```

---

## Rastreabilidade (M18 §7)

- **Data / responsável:** 31/07/2026 — Denis Stein.
- **Decisão anterior:** fluxo limitado a schema-only (opção intermediária da sessão).
- **Nova decisão:** dump completo autorizado para planejamento; schema-only como fallback.
- **Motivo da mudança:** esclarecimento do contexto operacional e da autorização existente pelo responsável.
- **Escopo afetado:** contrato, minuta de Gate e plano da Fase 02 (PLAN_DBTWIN_002.md).
- **Salvaguardas mantidas:** inspeção offline, dump fora do Git, denylist de produção, reprodução semântica sem Auth/segredos.
- **Documentos substituídos:** cláusula de limitação a schema-only, marcada como substituída (não apagada).
- **Ações executadas após a decisão:** nenhuma execução; apenas atualização documental (planejamento).

## Limite externo preservado (M18 §4)

Esta decisão prevalece sobre a governança interna do projeto. Não altera obrigações legais aplicáveis (incl. proteção de dados), políticas obrigatórias de provedores nem requisitos de segurança inseparáveis da execução segura. A bandeira relativa aos dados do cliente permanece registro factual e item de decisão do responsável — não julgamento do agente nem opinião jurídica consumada.
