# PowerShell script to start AgroSnap Application

Write-Host "Starting AgroSnap Application..." -ForegroundColor Green
Write-Host ""

# Check if Docker is running
try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not found"
    }
    Write-Host "Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Docker is not installed or not running." -ForegroundColor Red
    Write-Host "Please install Docker Desktop for Windows and start it." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if docker-compose is available
try {
    $composeVersion = docker-compose --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "docker-compose not found"
    }
    Write-Host "docker-compose found: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: docker-compose is not available." -ForegroundColor Red
    Write-Host "Please install docker-compose or use 'docker compose' instead." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Building and starting services..." -ForegroundColor Yellow
docker-compose up --build

Read-Host "Press Enter to exit"
