# run_webapp.ps1 — helper to create venv, install deps and run the Flask app
# Usage: Open PowerShell, cd to this folder and run: .\run_webapp.ps1

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

Write-Host "Working directory: $scriptDir"

# Ensure python is available
try {
    & python --version > $null 2>&1
} catch {
    Write-Error "Python is not found on PATH. Install Python and retry."
    exit 1
}

$venvPath = Join-Path $scriptDir ".venv"
$pythonExe = Join-Path $venvPath "Scripts\python.exe"
$pipExe = Join-Path $venvPath "Scripts\pip.exe"

if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
} else {
    Write-Host "Virtual environment already exists."
}

if (-not (Test-Path $pythonExe)) {
    Write-Error "Expected venv python at $pythonExe but it doesn't exist."
    exit 1
}

Write-Host "Upgrading pip and installing requirements (if present)..."
& $pythonExe -m pip install --upgrade pip
if (Test-Path "$scriptDir\requirements.txt") {
    & $pipExe install -r "$scriptDir\requirements.txt"
} else {
    Write-Host "No requirements.txt found — skipping pip install."
}

# Set env vars for this process
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"

Write-Host "Starting Flask app (http://127.0.0.1:5000) — press Ctrl+C to stop"
& $pythonExe -m flask run --host=127.0.0.1 --port=5000
