# Banco Gêmeo dos Agentes — Stein Technology

**Princípio único:** agentes têm liberdade total em ambientes descartáveis e nenhum
poder direto sobre ambientes reais.

```
Supabase HOMOLOG (bucphzinpsndsagonwiq)
   │  dump eventual (só Denis)
   ▼
backup-mestre privado (criptografado, fora do Git, só humano)
   │  sanitização (remove PII / auth / financeiro identificável)
   ▼
golden snapshot sanitizado (hash SHA-256 + manifesto)
   │  restore por missão
   ▼
clone Postgres local por missão (erp_agent_7730, erp_agent_compras, ...)
   │  agentes: SELECT/INSERT/UPDATE/DELETE/DDL/testes destrutivos/rollback
   ▼
migration revisada → Claude audita → STOP GATE → Denis aplica 1x em HOMOLOG
```

## As três camadas e quem pode o quê

| Ambiente | Agente lê | Agente escreve | Agente DDL | Quem aplica |
|---|---|---|---|---|
| clone local (descartável) | ✅ | ✅ | ✅ | agente |
| HOMOLOG (bucphzinpsndsagonwiq) | ❌ | ❌ | ❌ | **só Denis** |
| produção (futura) | ❌ | ❌ | ❌ | **só Denis, com gate** |

## Fronteira humano × robô (M17)

**Só Denis executa** (exigem a máquina Windows dele + credenciais):
1. gerar o dump do HOMOLOG (`01_dump_homolog.ps1`)
2. subir o Postgres local via Docker (`03_start_local.ps1`)
3. restaurar o golden snapshot por missão (`04_restore_mission.ps1`)
4. aplicar a migration final em HOMOLOG após o STOP GATE

**Agente executa sozinho** (dentro do clone, sem tocar HOMOLOG):
- toda coleta, toda hipótese, toda DDL de teste, toda regressão, todo rollback

O toque humano no meio do fluxo é **um** por transição, não por comando:
Denis roda 1 script → cola 1 resultado → agente continua sozinho.

## Regra de ouro

O clone é laboratório. HOMOLOG é a prova de integração. Produção é território
humano controlado. Uma migration que passou no clone **não está provada** até
rodar contra o estado real do HOMOLOG (M5: repetir gates na base exata).

## Divergências conhecidas clone × HOMOLOG (não são bugs — são limites)

- 🚩 **Auth/JWT:** o Postgres local puro não tem o GoTrue do Supabase. `current_tenant_id()`
  depende de `app_metadata.tenant_id` no JWT. No clone, simular via
  `SET LOCAL request.jwt.claims` dentro de BEGIN/COMMIT. Teste que depende de RLS/auth
  real dá resultado *indicativo*, não *definitivo* — reprovar no clone reprova; aprovar
  no clone ainda precisa do HOMOLOG.
- 🚩 **Extensões:** confirmar que o clone tem as mesmas extensões (pgcrypto para
  `gen_random_uuid`, etc.) — o `02_sanitize` valida isso.
- 🚩 **Versão do Postgres:** o clone tem que casar a major version do Supabase (o manifesto
  registra a versão; o restore falha alto se divergir).
- O clone congela no instante do dump. A Dolce continua operando no HOMOLOG. Migration
  validada em clone de terça pode encontrar dados de quinta — por isso o HOMOLOG é a prova final.

## Ordem de execução (ver docs/RUNBOOK.md)

Denis roda, em ordem: `01_dump` → `02_sanitize` → `03_start_local` → `04_restore_mission`.
Depois o agente trabalha no clone. Nada aqui toca HOMOLOG.
