# RUNBOOK — Banco Gêmeo dos Agentes

## Setup inicial (uma vez)
Pré-requisitos na máquina do Denis: Docker Desktop, `pg_dump`/`psql` (client Postgres),
`python3`. Confirmar a major version do Postgres do HOMOLOG no dashboard Supabase e
casar em `config/docker-compose.yml`.

## Fluxo por snapshot (Denis roda — 1 toque por passo, não por comando)

```
[Denis] 01_dump_homolog.ps1        → homolog_plain_DATA.sql   (PII real, privado, fora do Git)
[Denis] 02_sanitize.ps1 -InFile …  → golden_snapshot_DATA.sql (sem PII) + manifest.json
[Denis] 03_start_local.ps1         → Postgres local na porta 54329
[Denis] 04_restore_mission.ps1 -Mission 7730 -Snapshot golden_snapshot_DATA.sql
                                   → database erp_agent_7730 pronto
```

Cada script PARA no primeiro erro (checa `$LASTEXITCODE`) — nada avança sobre falha silenciosa.
O `02` roda o self-test do sanitizador antes de tocar PII, e faz varredura fail-closed de
e-mail residual depois.

## Depois: o agente trabalha SOZINHO no clone

Conexão do agente: `postgresql://postgres:local_only_not_secret@localhost:54329/erp_agent_7730`

No clone o agente tem escrita total: `SELECT/INSERT/UPDATE/DELETE/CREATE OR REPLACE/ALTER/DROP`,
testes de concorrência, rollback. Quando quebra o estado, Denis reroda o `04` e volta ao limpo.

Para simular tenant/JWT (o clone não tem GoTrue):
```sql
BEGIN;
SET LOCAL request.jwt.claims = '{"app_metadata":{"tenant_id":"20066226-9891-4a77-b3b3-80855e298b4b"},"role":"authenticated"}';
-- teste aqui
COMMIT;  -- ou ROLLBACK
```

## Fronteira que não muda

- Clone = laboratório. Agente livre.
- HOMOLOG = prova de integração. **Só Denis aplica**, 1x, após STOP GATE. Migration que
  passou no clone ainda precisa rodar aqui (M5).
- Produção = território humano com gate.

## Reset de missão
`04_restore_mission.ps1 -Mission 7730 -Snapshot …` de novo = DROP+CREATE+restore = estado limpo.

## Isolamento entre missões
Um database por missão no mesmo container: `erp_agent_7730`, `erp_agent_compras`.
Missão A nunca contamina B. Extensão natural do protocolo de worktrees para o estado do banco.
