# 04_restore_mission.ps1 v0.2 — cria database por missão e restaura via docker cp + psql -f.
# Correções: valida $Mission (anti-injeção), template0, restore por arquivo (não pipe de texto),
# prova de identidade dupla (hash vs manifesto).
param(
    [Parameter(Mandatory=$true)][string]$Mission,
    [Parameter(Mandatory=$true)][string]$Snapshot,
    [string]$SeedFile
)
$ErrorActionPreference = "Stop"

# validação anti-injeção do identificador
if ($Mission -notmatch '^[A-Za-z0-9_]+$') { throw "STOP: Mission invalida '$Mission' (use ^[A-Za-z0-9_]+$)." }
if (-not (Test-Path $Snapshot)) { throw "STOP: snapshot nao existe: $Snapshot" }

# M2: identidade dupla (só exigida para snapshot sanitizado, que tem manifesto)
$manifest = ($Snapshot -replace '\.sql$','') + ".manifest.json"
if (Test-Path $manifest) {
    $declared = (Get-Content $manifest -Raw | ConvertFrom-Json).sha256
    $actual = (Get-FileHash $Snapshot -Algorithm SHA256).Hash.ToLower()
    if ($declared -ne $actual) { throw "STOP: hash nao bate com manifesto. declared=$declared actual=$actual" }
    "OK identidade do snapshot provada (sha256 == manifesto)."
} else {
    Write-Warning "Sem manifesto (schema-only sem sanitizacao?). Prosseguindo sem prova de hash."
}

$db = "erp_agent_$Mission"
docker exec stein-agent-db psql -U postgres -c "DROP DATABASE IF EXISTS $db WITH (FORCE);"
if ($LASTEXITCODE -ne 0) { throw "STOP: drop $db falhou." }
docker exec stein-agent-db psql -U postgres -c "CREATE DATABASE $db TEMPLATE template0;"
if ($LASTEXITCODE -ne 0) { throw "STOP: create $db falhou." }

# restore por arquivo (docker cp + psql -f), NÃO pipe de texto (evita corromper acento/encoding)
docker cp $Snapshot stein-agent-db:/tmp/snapshot.sql
if ($LASTEXITCODE -ne 0) { throw "STOP: docker cp falhou." }
docker exec stein-agent-db psql -U postgres -d $db -v ON_ERROR_STOP=1 -f /tmp/snapshot.sql
if ($LASTEXITCODE -ne 0) { throw "STOP: restore falhou (exit=$LASTEXITCODE). Base $db pode estar parcial." }

# seed sintético opcional (golden padrão = schema + seed)
if ($SeedFile) {
    if (-not (Test-Path $SeedFile)) { throw "STOP: seed nao existe: $SeedFile" }
    docker cp $SeedFile stein-agent-db:/tmp/seed.sql
    docker exec stein-agent-db psql -U postgres -d $db -v ON_ERROR_STOP=1 -f /tmp/seed.sql
    if ($LASTEXITCODE -ne 0) { throw "STOP: seed falhou." }
    "OK seed sintetico aplicado."
}
docker exec stein-agent-db psql -U postgres -d $db -c "SELECT 'restore OK', count(*) FROM information_schema.tables WHERE table_schema='public';"
"OK missao '$db' pronta na porta 127.0.0.1:54329."
"Conexao do agente: postgresql://postgres:local_only_not_secret@127.0.0.1:54329/$db"
