@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo.
echo ===============================================
echo         Divar Car Scraper - Run
echo ===============================================
echo.

if not exist "config.json" (
    echo Setup has not been completed yet.
    echo Please run setup.bat first.
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Project dependencies are not set up yet.
    echo Please run setup.bat first.
    echo.
    pause
    exit /b 1
)

if not exist "src\main.py" (
    echo ERROR: src\main.py was not found.
    echo Make sure run.bat is in the project root.
    echo.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" src\main.py
set "EXIT_CODE=%ERRORLEVEL%"

echo.
if not "%EXIT_CODE%"=="0" (
    echo Scraper stopped with an error. Exit code: %EXIT_CODE%
) else (
    echo Scraper finished.
)
echo.
pause
exit /b %EXIT_CODE%
