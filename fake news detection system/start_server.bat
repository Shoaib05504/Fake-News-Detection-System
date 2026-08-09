@echo off
title Fake News Detection Server
color 0A
echo ========================================
echo   FAKE NEWS DETECTION SYSTEM
echo   Auto-Starting Server...
echo ========================================
echo.
echo Checking models...
echo.

cd /d "%~dp0"

REM Check if models exist
if not exist "models\best_model.pkl" (
    echo [ERROR] Model files not found!
    echo.
    echo Please train the model first by running:
    echo    py -3.12 train_full_fast.py
    echo.
    pause
    exit /b 1
)

echo [OK] Models found!
echo.
echo Starting Flask server...
echo Opening browser in 5 seconds...
echo.
echo ========================================
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start browser after 5 seconds in background
start /B cmd /c "timeout /t 5 /nobreak >nul && start http://localhost:5000"

REM Start Flask server
py -3.12 app.py

pause
