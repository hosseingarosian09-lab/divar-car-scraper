@echo off
REM =============================================================================
REM scrape.bat
REM Quick launcher for the Divar Car Scraper project on Windows
REM Double-click this file or run it from Command Prompt / PowerShell
REM =============================================================================

echo.
echo  ===============================================
echo     Divar Car Scraper   (personal project)
echo  ===============================================
echo.

REM ────────────────────────────────────────────────
REM Optional: activate virtual environment (uncomment if you use venv)
REM if exist venv\Scripts\activate.bat (
REM     echo Activating virtual environment...
REM     call venv\Scripts\activate.bat
REM )

REM ────────────────────────────────────────────────
echo Changing to source directory...
cd /d "%~dp0src"
if errorlevel 1 (
    echo.
    echo ERROR: Could not find or enter src\ folder
    echo Make sure scrape.bat is in the project root.
    echo.
    pause
    exit /b 1
)

REM ────────────────────────────────────────────────
echo Running main.py ...
echo.

python main.py

REM ────────────────────────────────────────────────
echo.
echo  ===============================================
echo               Finished
echo  ===============================================
echo.

pause