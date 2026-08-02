[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string[]]$Roots = @(
        "C:\SteinAgentFactory",
        "$env:USERPROFILE\Downloads"
    ),

    [Parameter(Mandatory = $false)]
    [string]$OutputDirectory = "C:\SteinAgentFactory\_inventory",

    [Parameter(Mandatory = $false)]
    [switch]$IncludeHidden
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-SafeFileHash {
    param([Parameter(Mandatory = $true)][string]$Path)

    try {
        return (Get-FileHash -LiteralPath $Path -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant()
    }
    catch {
        return $null
    }
}

function Get-RelativePathSafe {
    param(
        [Parameter(Mandatory = $true)][string]$BasePath,
        [Parameter(Mandatory = $true)][string]$TargetPath
    )

    try {
        return [System.IO.Path]::GetRelativePath($BasePath, $TargetPath)
    }
    catch {
        return $TargetPath
    }
}

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$runDir = Join-Path $OutputDirectory $timestamp
New-Item -ItemType Directory -Path $runDir -Force | Out-Null

$errors = New-Object System.Collections.Generic.List[string]
$records = New-Object System.Collections.Generic.List[object]

foreach ($root in $Roots) {
    if (-not (Test-Path -LiteralPath $root)) {
        $errors.Add("ROOT_NOT_FOUND`t$root")
        continue
    }

    $rootFull = (Resolve-Path -LiteralPath $root).Path

    $getChildParams = @{
        LiteralPath = $rootFull
        File        = $true
        Recurse     = $true
        ErrorAction = "SilentlyContinue"
    }

    if ($IncludeHidden) {
        $getChildParams["Force"] = $true
    }

    $files = Get-ChildItem @getChildParams

    foreach ($file in $files) {
        try {
            $hash = Get-SafeFileHash -Path $file.FullName
            if (-not $hash) {
                $errors.Add("HASH_FAILED`t$($file.FullName)")
            }

            $records.Add([pscustomobject]@{
                Root              = $rootFull
                RelativePath      = Get-RelativePathSafe -BasePath $rootFull -TargetPath $file.FullName
                FullPath          = $file.FullName
                Name              = $file.Name
                Extension         = $file.Extension.ToLowerInvariant()
                SizeBytes         = $file.Length
                CreatedUtc        = $file.CreationTimeUtc.ToString("o")
                LastWriteUtc      = $file.LastWriteTimeUtc.ToString("o")
                SHA256            = $hash
                IsArchive         = $file.Extension -match '^\.(zip|tar|gz|tgz|7z|rar)$'
                HasWindowsCopyTag = $file.BaseName -match '\(\d+\)$'
                Classification    = "UNCLASSIFIED"
                ProposedDestination = ""
                Notes             = ""
            })
        }
        catch {
            $errors.Add("FILE_FAILED`t$($file.FullName)`t$($_.Exception.Message)")
        }
    }
}

$inventoryCsv = Join-Path $runDir "inventory.csv"
$inventoryJson = Join-Path $runDir "inventory.json"
$duplicatesCsv = Join-Path $runDir "duplicate-groups.csv"
$summaryJson = Join-Path $runDir "summary.json"
$treeTxt = Join-Path $runDir "tree.txt"
$errorsLog = Join-Path $runDir "errors.log"

$records |
    Sort-Object Root, RelativePath |
    Export-Csv -LiteralPath $inventoryCsv -NoTypeInformation -Encoding UTF8

$records |
    Sort-Object Root, RelativePath |
    ConvertTo-Json -Depth 5 |
    Set-Content -LiteralPath $inventoryJson -Encoding UTF8

$duplicateRows = New-Object System.Collections.Generic.List[object]
$groups = $records |
    Where-Object { $_.SHA256 } |
    Group-Object SHA256 |
    Where-Object Count -gt 1

$groupNumber = 0
foreach ($group in $groups) {
    $groupNumber++
    foreach ($item in $group.Group) {
        $duplicateRows.Add([pscustomobject]@{
            DuplicateGroup = $groupNumber
            SHA256          = $group.Name
            Count           = $group.Count
            SizeBytes       = $item.SizeBytes
            FullPath        = $item.FullPath
            Name            = $item.Name
        })
    }
}

$duplicateRows |
    Sort-Object DuplicateGroup, FullPath |
    Export-Csv -LiteralPath $duplicatesCsv -NoTypeInformation -Encoding UTF8

$treeLines = New-Object System.Collections.Generic.List[string]
foreach ($root in $Roots) {
    $treeLines.Add("ROOT: $root")
    if (Test-Path -LiteralPath $root) {
        Get-ChildItem -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue |
            Sort-Object FullName |
            ForEach-Object {
                $kind = if ($_.PSIsContainer) { "DIR " } else { "FILE" }
                $treeLines.Add("$kind`t$($_.FullName)")
            }
    }
    $treeLines.Add("")
}
$treeLines | Set-Content -LiteralPath $treeTxt -Encoding UTF8

$summary = [ordered]@{
    generated_at_utc         = (Get-Date).ToUniversalTime().ToString("o")
    roots                    = $Roots
    output_directory         = $runDir
    total_files              = $records.Count
    total_bytes              = ($records | Measure-Object SizeBytes -Sum).Sum
    archive_files            = ($records | Where-Object IsArchive).Count
    windows_copy_tag_files   = ($records | Where-Object HasWindowsCopyTag).Count
    duplicate_hash_groups    = $groups.Count
    duplicate_file_instances = $duplicateRows.Count
    hash_failures            = ($errors | Where-Object { $_ -like "HASH_FAILED*" }).Count
    errors                   = $errors.Count
}
$summary |
    ConvertTo-Json -Depth 5 |
    Set-Content -LiteralPath $summaryJson -Encoding UTF8

$errors | Set-Content -LiteralPath $errorsLog -Encoding UTF8

Write-Host ""
Write-Host "Inventário somente leitura concluído."
Write-Host "Saída: $runDir"
Write-Host "Arquivos: $($records.Count)"
Write-Host "Grupos de duplicatas por SHA-256: $($groups.Count)"
Write-Host "Erros: $($errors.Count)"
Write-Host ""
Write-Host "Nenhum arquivo de origem foi movido, renomeado ou apagado."
