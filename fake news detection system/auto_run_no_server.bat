REM filepath: c:\Users\user\Desktop\fake news detection system\fake news detection system\auto_run_no_server.bat
@echo off
title Auto Run - Process Kaggle Data and Open Report
color 0A

REM ensure script runs from this folder
cd /d "%~dp0"

echo ========================================
echo Running Kaggle processing and opening report
echo ========================================

REM Ensure Python and pandas
py -3.12 -m pip install --upgrade pip >nul 2>&1
py -3.12 -m pip install pandas >nul 2>&1

REM Run dataset processing
echo.
echo Running: py -3.12 process_kaggle_data.py
py -3.12 process_kaggle_data.py
if errorlevel 1 (
    echo.
    echo [ERROR] process_kaggle_data.py failed. Check output above.
    pause
    exit /b 1
)

REM Create HTML report from CSV
echo.
echo Generating HTML report...
py -3.12 post_process_open.py
if errorlevel 1 (
    echo.
    echo [ERROR] post_process_open.py failed. Check output above.
    pause
    exit /b 1
)

REM Open report.html in default browser
if exist "report.html" (
    start "" "%~dp0report.html"
) else (
    echo [ERROR] report.html not found.
)

pause
