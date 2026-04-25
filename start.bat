@echo off
echo Starting AgroSnap Application...
echo.

REM Check if Docker is running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Docker is not installed or not running.
    echo Please install Docker Desktop for Windows and start it.
    pause
    exit /b 1
)

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: docker-compose is not available.
    echo Please install docker-compose or use 'docker compose' instead.
    pause
    exit /b 1
)

echo Building and starting services...
docker-compose up --build

pause
