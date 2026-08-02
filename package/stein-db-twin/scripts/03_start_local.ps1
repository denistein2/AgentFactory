# 03_start_local.ps1 — sobe o Postgres local descartável (Docker).
# EXECUTOR LOCAL RODA (Codex se tiver shell+Docker; senao Denis). So o 01 (dump remoto) exige Denis. Depende de Docker Desktop rodando.
$ErrorActionPreference = "Stop"

$compose = Join-Path $PSScriptRoot "..\config\docker-compose.yml"
if (-not (Test-Path $compose)) { throw "STOP: docker-compose.yml nao encontrado." }

docker compose -f $compose up -d
if ($LASTEXITCODE -ne 0) { throw "STOP: docker compose up falhou (exit=$LASTEXITCODE)." }

# espera o Postgres aceitar conexao (fail-closed com timeout)
$maxTries = 30
for ($i = 1; $i -le $maxTries; $i++) {
    docker exec stein-agent-db pg_isready -U postgres 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        "OK Postgres local pronto na porta 54329 (db 'postgres')."
        "Conexao local: postgresql://postgres:local_only_not_secret@localhost:54329/postgres"
        "PROXIMO: 04_restore_mission.ps1 -Mission 7730 -Snapshot <golden_snapshot_...sql>"
        exit 0
    }
    Start-Sleep -Seconds 2
}
throw "STOP: Postgres nao respondeu em $($maxTries*2)s. Ver 'docker logs stein-agent-db'."
