# Sync canonical content/ to SPA mirrors (per CANONICAL_LOCK.md unlock policy step 2)
$Root = Split-Path $PSScriptRoot -Parent
$Source = Join-Path $Root "content"
$Targets = @(
    (Join-Path $Root "client\src\content"),
    (Join-Path $Root "client\public\content")
)

foreach ($target in $Targets) {
    if (-not (Test-Path $target)) {
        New-Item -ItemType Directory -Path $target -Force | Out-Null
    }
    Copy-Item -Path (Join-Path $Source "*.md") -Destination $target -Force
    Write-Host "Synced -> $target"
}