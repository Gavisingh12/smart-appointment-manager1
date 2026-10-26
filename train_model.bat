@echo off
echo ===================================================
echo  CareCompass AI - 512 Disease Model Trainer
echo ===================================================
echo.

where py >nul 2>nul
if %errorlevel% equ 0 (
    echo Using Python Launcher (py -3.13)...
    py -3.13 scripts\train_disease_model.py
    if %errorlevel% neq 0 (
        echo Trying py -3...
        py -3 scripts\train_disease_model.py
    )
) else (
    echo Using Windows Python...
    "C:\Users\Govinder Singh\AppData\Local\Programs\Python\Python313\python.exe" scripts\train_disease_model.py
)

echo.
echo Model training process finished.
pause
