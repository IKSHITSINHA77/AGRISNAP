# PowerShell script to stop AgroSnap Application

Write-Host "Stopping AgroSnap Application..." -ForegroundColor Yellow
Write-Host ""

docker-compose down

Write-Host "Application stopped." -ForegroundColor Green
Read-Host "Press Enter to exit"
