# PowerShell script to setup AgroSnap for Windows

Write-Host "Setting up AgroSnap for Windows..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Node.js not found"
    }
    Write-Host "Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Node.js is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Docker is installed
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not found"
    }
    Write-Host "Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Docker is not installed or not running." -ForegroundColor Red
    Write-Host "Please install Docker Desktop for Windows from https://docker.com" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "All required tools are installed!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Cyan
Write-Host "  - Run: start.bat (Command Prompt)" -ForegroundColor White
Write-Host "  - Run: .\start.ps1 (PowerShell)" -ForegroundColor White
Write-Host ""
Write-Host "To stop the application:" -ForegroundColor Cyan
Write-Host "  - Run: stop.bat (Command Prompt)" -ForegroundColor White
Write-Host "  - Run: .\stop.ps1 (PowerShell)" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
