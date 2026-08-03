# HANDOFF — AGENT-FACTORY-DBTWIN-001 — Fase 01 Sintética

**Projeto:** 02 — Stein Agent Factory (Fábrica de Agentes)
**Missão:** AGENT-FACTORY-DBTWIN-001
**Pacote declarado historicamente:** stein-db-twin v0.3-phase01 — evidência
documental; pacote-fonte original ainda não localizado. A fonte hoje importada é v0.2.
**Data:** 31/07/2026
**Status:** CANDIDATA — encerramento da Fase 01 Sintética recomendado pelos auditores, aguardando Gate Humano formal.
**Autorização para dado real / HOMOLOG / Supabase / produção / #7730 / Fase 02:** NÃO.

> Registro canônico único. Substitui qualquer versão anterior de handoff desta missão. O bloco do Gate Humano e a tríade de nível de evidência são fonte única: não devem ser recopiados de forma divergente em outros documentos.

---

## 0. Marco da Stein Agent Factory

Esta foi a primeira missão real executada pela Stein Agent Factory. Antes mesmo da conclusão da Fase 01, a fábrica demonstrou valor operacional ao:

- identificar gargalos de infraestrutura na estação de trabalho;
- instalar e validar WSL2 e Docker Desktop;
- validar Docker Engine e Docker Compose;
- confirmar virtualização Intel VT-x;
- detectar SSD de 128 GB saturado com HD de 1 TB praticamente vazio, registrando a reorganização como melhoria permanente;
- impedir que problemas de infraestrutura fossem confundidos com problemas do Banco Gêmeo, sem tocar no ERP.

Com isso, a separação entre **Produto → Agentes → Conteúdo** deixou de ser arquitetura conceitual e passou a ter validação operacional. Este é o primeiro caso de sucesso interno da fábrica e serve de referência para as próximas missões.

*Nota de precisão:* os itens acima são fatos de infraestrutura da estação. Eles não integram o "resultado técnico provado" do ciclo do Banco Gêmeo (seção 1) e não devem ser lidos como tal.

---

## 1. O que foi provado — nível: coerência documental

- Ciclo mecânico local 100% sintético: preflight → self-test → sanitização → start → restore → validação → alteração destrutiva → reset → fingerprint → destroy.
- Modo Synthetic; imagem `postgres:16-alpine` **sem alegação de paridade**.
- Bind provado em `127.0.0.1:55439`.
- Fixtures adversariais (tabela e coluna não classificadas) falharam como esperado (`EXPECTED_FAIL`), sem gravar artefato ou manifesto parcial.
- Reset restaura o estado bit a bit:
  - inicial = `1966329b15089b5473094043fb2ade6b6f880ee66e61b259bfc67f61b035f219`
  - destrutivo = `87a9fe6cdfac815b1eb3eb2b0e5129cbbef3767728ad9c5a3d3bc1f3c7c6292c`
  - final = `1966329b15089b5473094043fb2ade6b6f880ee66e61b259bfc67f61b035f219`
  - relação: inicial ≠ destrutivo = final
- `snapshot_sha256` = `9a7ddb57...6f4e81` = SHA de `safe_sanitized.sql`.
- `remote_database_accesses` = 0; envio de dados = 0; containers remanescentes = 0.
- Rede total **não** foi zero: houve pull público de `postgres:16-alpine`. Zero acesso a banco remoto ≠ zero rede — distinção preservada de propósito.

*Escopo do "provado":* o ciclo E2E foi executado via Docker/Compose com bind em loopback. WSL2 estar operacional na estação é fato de infraestrutura (seção 0); os artefatos não estabelecem que o E2E rodou especificamente sobre WSL2, e essa distinção não altera o que foi provado.

---

## 2. Natureza da auditoria — o que NÃO foi feito

Três níveis distintos, que não devem ser confundidos:

```
coerência documental  ≠  reprodução de execução  ≠  auditoria de código
```

- Foram feitas **três leituras** (GPT, Claude, Denis), **independentes entre si mas sobre o mesmo conjunto de artefatos** — não três reproduções independentes do pipeline.
- A verificação foi de **consistência** sobre artefatos e documentos finais.
- **Não** houve reprodução independente do pipeline nem revisão integral do código-fonte.
- `sanitize_v2.py`, `columns.json` e os scripts `00–10` permanecem pendentes de auditoria técnica completa.
- Onde consta PASS, significa **resultado declarado e coerente com os artefatos entregues**. Exceção: fingerprints e hashes de arquivo, conferidos por **consistência cruzada entre os artefatos entregues**.

Esta tríade é definição operacional do nível de evidência do projeto, não comentário. Integra o bloco oficial do Gate Humano.

---

## 3. Pendências carregadas para a Fase 02

- `cells_masked=24` **não** cruzado contra `columns.json` (arquivo ausente da entrega analisada).
- Porta 54329 não resolvida neste host (reserva WinNAT `54299–54398`). Topologia em 55439: provada. Topologia exata em 54329: não provada.
- Pacote sem controle de versão (`.git` ausente); sem commit-base nem evidência de delta.
- Bloqueio remoto é por guard de ambiente, não por controle de rede estrutural.
- Nenhuma prova de paridade Supabase: roles, grants, RLS, funções, triggers, extensões, `search_path`, auth/JWT/storage — todos fora de escopo até aqui.
- Ausência de FK para auth **não** prova restauração de policies/funções.

---

## 4. Condições antes da Fase 02 — ordem recomendada

1. Versionar o pacote em repositório próprio (definir repo, commit-base, artefatos ignorados, evidência de delta).
2. Auditar código dos scripts e políticas:
   - revisão de `sanitize_v2.py`;
   - revisão de `columns.json`;
   - revisão dos scripts `00–10`;
   - reprodução independente do E2E;
   - cruzamento de `cells_masked` contra a política.
3. Resolver formalmente a porta 54329 (alterar reserva WinNAT, fixar outra porta canônica, ou abandonar 54329 como requisito).
4. Definir contrato e Gate Humano formal da Fase 02.
5. Definir controle de rede e origem oficial do schema real; inventário integral de tabelas/colunas antes de qualquer snapshot com dados.
6. Manter dados reais **proibidos** até autorização humana específica.

---

## 5. Gate Humano canônico

```
GATE HUMANO — AGENT-FACTORY-DBTWIN-001

Decisão:
APROVAR A CONCLUSÃO DA FASE 01 SINTÉTICA.

Natureza desta auditoria:
- verificação de consistência sobre artefatos e documentos finais;
- não houve reprodução independente do pipeline nem revisão integral do
  código-fonte pelos auditores;
- sanitize_v2.py, columns.json e scripts 00–10 permanecem pendentes de
  auditoria técnica completa;
- os resultados marcados PASS representam resultados declarados e coerentes
  com os artefatos entregues;
- fingerprints e hashes de arquivo foram conferidos independentemente por
  consistência cruzada entre os artefatos entregues;
- pendência conhecida: cells_masked=24 não foi cruzado contra columns.json,
  ausente da entrega analisada.

Escopo da aprovação:
- laboratório local sintético;
- ciclo start/restore/validate/destroy/reset/fingerprint;
- políticas e fixtures exclusivamente fictícias;
- v0.3-phase01 como referência documental de continuidade; não tratar como
  pacote-fonte presente até sua localização e reconciliação.

Não autorizado:
- dado real;
- dump de HOMOLOG;
- conexão com Supabase;
- aplicação da #7730;
- produção;
- declaração de paridade;
- início automático da Fase 02.

Condições antes da Fase 02:
1. versionar o pacote em repositório próprio;
2. auditar o código dos scripts e políticas, incluindo:
   - revisão de sanitize_v2.py;
   - revisão de columns.json;
   - revisão dos scripts 00–10;
   - reprodução independente do E2E;
   - cruzamento de cells_masked contra a política;
3. definir contrato e gate formal da Fase 02;
4. definir controle de rede e origem do schema;
5. manter dados reais proibidos até autorização específica.
```

---

## 6. Parada

Laboratório destruído. Porta 55439 sem listener. Nenhum container ativo. Fase 02 **não** iniciada. Próxima ação exige decisão humana explícita.

---

## Próxima missão

**AGENT-FACTORY-DBTWIN-002** — preparar a Fase 02 **sem executá-la**. Produzir somente: contrato da Fase 02, Gate Humano da Fase 02, estratégia de auditoria, definição da origem oficial do schema, estratégia de versionamento Git, política de rede e plano de validação de roles/RLS/funções/extensões/auth/semântica Supabase.
