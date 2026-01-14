Write-Host "Starting Music RPG Attack Game..." -ForegroundColor Green
python main.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nError: Could not run the game." -ForegroundColor Red
    Write-Host "Make sure Python is installed and pygame is installed." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
}
