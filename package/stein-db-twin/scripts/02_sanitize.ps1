# 02_sanitize.ps1 — sanitiza o dump-mestre e produz o GOLDEN SNAPSHOT + manifesto.
# EXECUTOR LOCAL RODA (Codex se tiver shell+Docker; senao Denis). So o 01 (dump remoto) exige Denis. Depende de python3 no PATH e de sanitizer\sanitize_v2.py.
#
# Uso:
#   .\02_sanitize.ps1 -InFile "C:\Users\aebac\Documents\backups_erp\twin\homolog_plain_2026-07-31.sql"
#
# Saída (mesma pasta twin\):
#   golden_snapshot_AAAA-MM-DD.sql   <- vai para os agentes (sem PII)
#   golden_snapshot_AAAA-MM-DD.manifest.json

param(
    [Parameter(Mandatory=$true)][string]$InFile,
    [string]$Salt = ("stein-" + (Get-Date -Format "yyyyMMdd") + "-" + [guid]::NewGuid().ToString("N").Substring(0,8))
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $InFile)) { throw "STOP: arquivo de entrada nao existe: $InFile" }

$date       = Get-Date -Format "yyyy-MM-dd"
$outDir     = Split-Path $InFile -Parent
$snapshot   = Join-Path $outDir "golden_snapshot_$date.sql"
$manifest   = Join-Path $outDir "golden_snapshot_$date.manifest.json"
$sanitizer  = Join-Path $PSScriptRoot "..\sanitizer\sanitize_v2.py"
$config     = Join-Path $PSScriptRoot "..\config\columns.json"

if (-not (Test-Path $sanitizer)) { throw "STOP: sanitize.py nao encontrado em $sanitizer" }
if (-not (Test-Path $config))    { throw "STOP: columns.json nao encontrado em $config" }

# prova que o sanitizador esta integro ANTES de confiar PII a ele (M4)
python3 $sanitizer --self-test
if ($LASTEXITCODE -ne 0) { throw "STOP: self-test do sanitizador FALHOU. Nao sanitizar com peca quebrada." }

python3 $sanitizer --in $InFile --out $snapshot --config $config --salt $Salt --manifest $manifest
if ($LASTEXITCODE -ne 0) { throw "STOP: sanitizacao falhou (exit=$LASTEXITCODE)." }

# varredura residual de PII agora e feita DENTRO do sanitizador v0.2 (regex real, fail-closed).

"OK golden snapshot: $snapshot"
"OK manifesto:       $manifest"
"Salt usado (guardar fora do Git se quiser reproduzir mascaramento): $Salt"
"PROXIMO: 03_start_local.ps1 (sobe Postgres) e 04_restore_mission.ps1 (restaura por missao)."
