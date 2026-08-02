# Template de missão para agente executor no Banco Gêmeo

Este é o molde que substitui o "Denis vira barramento". O agente recebe a conexão do
clone e trabalha sozinho, devolvendo só artefatos + decisões.

```text
# MISSÃO <ID> — <TEMA> — EXECUÇÃO NO BANCO GÊMEO

Banco de trabalho (clone descartável, escrita TOTAL liberada):
  postgresql://postgres:local_only_not_secret@localhost:54329/erp_agent_<ID>

Você (agente) tem liberdade total NESTE banco: SELECT/INSERT/UPDATE/DELETE/DDL/rollback.
Ele é descartável — se quebrar, Denis reroda o restore. NÃO peça a Denis para rodar
queries: rode você mesmo na conexão acima.

PROIBIDO (fail-closed):
  - qualquer conexão ao HOMOLOG (bucphzinpsndsagonwiq) ou produção;
  - git commit / push / PR;
  - tratar resultado do clone como prova final (o clone congela no dump; RLS/JWT são
    simulados, não reais — ver divergências no README).

Simular tenant quando precisar de RLS:
  BEGIN; SET LOCAL request.jwt.claims = '{"app_metadata":{"tenant_id":"<uuid>"},"role":"authenticated"}'; ... ROLLBACK;

ENTREGÁVEIS:
  1. artefatos em docs/<data>/ (desenho, contrato de regressão, decisões humanas);
  2. migration proposta em scripts/<data>/ (NÃO aplicada em lugar nenhum além do clone);
  3. evidência: o que rodou no clone, antes/depois, resultado dos testes.

PARADA:
  Ao concluir: listar artefatos + resumo + decisões humanas pendentes. PARAR.
  A migration só vai ao HOMOLOG pelas mãos de Denis, após Claude auditar e Denis aprovar no STOP GATE.
```

## Como isto mata o barramento humano

Antes: agente pede query → Denis abre Supabase → executa → cola → agente pede outra.
Agora: agente abre o clone local → roda tudo que precisa → devolve migration + evidência.
Denis toca 1x: aplica a migration final no HOMOLOG depois do STOP GATE.
