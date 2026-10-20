param(
    [switch]$Refresh,      # download all input data again (network; needed for a fresh copy of the repository)
    [switch]$Sentinel2     # rebuild Sentinel-2 composites from the cloud archive (network; long)
)
$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$pythonPath = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) {
    python -m venv (Join-Path $projectRoot '.venv')
    if ($LASTEXITCODE -ne 0) { throw 'Environment creation failed.' }
}
& $pythonPath -m pip install -r (Join-Path $projectRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }

$steps = @()
if ($Refresh) { $steps += @('download_sources.py --all', 'fetch_ext.py') }
$steps += @(
    'analyse.py',             # HOT inventory checks and archived UNDP/UNOSAT layers
    'terrain.py',             # DEM mosaic, conditioning, flow path, height above channel
    'corridor.py',            # transects: valley-floor width and flow-edge heights
    'build_buildings.py',     # common building stock with terrain attributes
    'analysis_products.py',   # harmonized damage inventory and inter-product agreement
    'analysis_terrain.py',    # local and regional models, reach envelopes
    'analysis_exposure.py',   # settlement growth, population, infrastructure exposure
    'analysis_impacts.py',    # timing, lead times, danger zones, debris, ranking
    'analysis_transport.py',  # CEMS road and bridge grading
    'analysis_landcover.py'   # pre-event land cover inside the flow extent
)
if ($Sentinel2) { $steps += 's2_change.py' }
$steps += @('analysis_s2.py', 'figures_v2.py', 'figures_si.py', 'build_references.py', 'build_manuscript_v2.py',
            'build_si.py', 'export_v2.py', 'build_document.py', 'validate_v2.py')

foreach ($scriptName in $steps) {
    Write-Output ('== ' + $scriptName)
    $parts = $scriptName -split ' '
    $scriptArgs = @(); if ($parts.Count -gt 1) { $scriptArgs = $parts[1..($parts.Count - 1)] }
    & $pythonPath (Join-Path $projectRoot ('scripts\' + $parts[0])) @scriptArgs
    if ($LASTEXITCODE -ne 0) { throw ('Failed: ' + $scriptName) }
}
Write-Output 'Rebuild complete: documents are in the paper folder.'
