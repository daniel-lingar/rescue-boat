# Rescue Boat — one-command ship pipeline (verify → footers → sync → PDF → checklist)
param(
    [switch]$SkipFooters,
    [switch]$SkipSync,
    [switch]$SkipPdf,
    [switch]$SkipHub,
    [switch]$BuildPdf
)

$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
$Py = Join-Path $Root "export\ship_console.py"

$args = @()
if ($SkipFooters) { $args += "--skip-footers" }
if ($SkipSync) { $args += "--skip-sync" }
if ($SkipPdf) { $args += "--skip-pdf" }
if ($SkipHub) { $args += "--skip-hub" }
if ($BuildPdf) { $args += "--build-pdf" }

python $Py @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }