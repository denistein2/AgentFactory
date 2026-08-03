# 01_dump_homolog.ps1 v0.2 — dump do HOMOLOG. SÓ o dump remoto exige Denis.
# Por padrão SCHEMA-ONLY (golden padrão = estrutura + seed sintético, risco PII zero).
# -WithData só para snapshot-de-caso, e AINDA passa pela sanitização obrigatória.
param([switch]$WithData)
$ErrorActionPreference = "Stop"
if (-not $env:SUPABASE_DB_URL) { throw "STOP: defina `$env:SUPABASE_DB_URL (nunca hardcode senha)." }
$date = Get-Date -Format "yyyy-MM-dd"
$outDir = "C:\Users\aebac\Documents\backups_erp\twin"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
if ($WithData) {
    $outFile = Join-Path $outDir "homolog_CASE_plain_$date.sql"
    Write-Warning "🚩 -WithData: dump COM dados reais. OBRIGATORIO passar por 02_sanitize ANTES de qualquer uso."
    pg_dump --dbname="$env:SUPABASE_DB_URL" --format=plain --no-owner --no-privileges --schema=public --file="$outFile"
} else {
    $outFile = Join-Path $outDir "homolog_SCHEMA_$date.sql"
    pg_dump --dbname="$env:SUPABASE_DB_URL" --format=plain --no-owner --no-privileges --schema=public --schema-only --file="$outFile"
}
if ($LASTEXITCODE -ne 0) { throw "STOP: pg_dump falhou (exit=$LASTEXITCODE)." }
"OK: $outFile ($([math]::Round((Get-Item $outFile).Length/1KB,1)) KB)"
if ($WithData) { "PROXIMO: 02_sanitize.ps1 (OBRIGATORIO) antes de restaurar." }
else { "Schema-only: pode ir direto ao 03/04. Seed sintetico vem de seeds/seed_7730.sql." }
