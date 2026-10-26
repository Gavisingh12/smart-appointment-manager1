# CareCompass AI - 512 Disease Model Trainer PowerShell Helper
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host " CareCompass AI - 512 Disease Model Training Pipeline" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

$python313 = "C:\Users\Govinder Singh\AppData\Local\Programs\Python\Python313\python.exe"

if (Test-Path $python313) {
    Write-Host "Executing training pipeline with Python 3.13..." -ForegroundColor Green
    & $python313 scripts\train_disease_model.py
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    Write-Host "Executing training pipeline with Python Launcher (py -3.13)..." -ForegroundColor Green
    py -3.13 scripts\train_disease_model.py
} else {
    Write-Host "Executing training pipeline with default python..." -ForegroundColor Yellow
    python scripts\train_disease_model.py
}
