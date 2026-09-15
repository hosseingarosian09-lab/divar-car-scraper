@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo.
echo ===============================================
echo        Divar Car Scraper - Windows Setup
echo ===============================================
echo.

call :find_python
if defined PYTHON_EXE goto :python_ready

echo Python 3.10 or newer was not found.
echo Trying to install Python 3.13 with winget...
echo.

where winget >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python is not installed and winget is not available.
    echo Install Python 3.10 or newer from https://www.python.org/downloads/
    echo Then run setup.bat again.
    goto :fail
)

winget install --id Python.Python.3.13 -e --source winget --scope user --accept-package-agreements --accept-source-agreements --disable-interactivity
set "WINGET_EXIT=%ERRORLEVEL%"

rem winget may report an already-installed package with a non-zero code.
rem Always search again before treating that as a setup failure.
call :find_python
if defined PYTHON_EXE goto :python_ready

if not "%WINGET_EXIT%"=="0" (
    echo.
    echo winget did not complete a new installation, and a usable Python was not found.
)

echo.
echo ERROR: Python 3.10+ still could not be located.
echo If Python is already installed, restart Windows once and run setup.bat again.
echo Otherwise install Python from https://www.python.org/downloads/
echo and enable "Add python.exe to PATH" during installation.
goto :fail

:python_ready
echo Using Python:
echo   %PYTHON_EXE% %PYTHON_ARGS%
"%PYTHON_EXE%" %PYTHON_ARGS% --version
if errorlevel 1 goto :fail

echo.
echo Creating the project virtual environment...
if not exist ".venv\Scripts\python.exe" (
    "%PYTHON_EXE%" %PYTHON_ARGS% -m venv .venv
    if errorlevel 1 (
        echo ERROR: Could not create the virtual environment.
        goto :fail
    )
)

set "VENV_PYTHON=.venv\Scripts\python.exe"

echo.
echo Preparing pip...
"%VENV_PYTHON%" -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Could not prepare pip.
    goto :fail
)

echo.
echo Installing project requirements...
"%VENV_PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Could not install requirements.
    goto :fail
)

:choose_format
echo.
echo Choose the output format:
echo   1. CSV
echo   2. JSON
set "FORMAT_CHOICE="
set /p "FORMAT_CHOICE=Enter 1 or 2: "

if "%FORMAT_CHOICE%"=="1" (
    set "SAVE_FORMAT=csv"
    goto :save_config
)
if "%FORMAT_CHOICE%"=="2" (
    set "SAVE_FORMAT=json"
    goto :save_config
)

echo Invalid choice. Please enter 1 or 2.
goto :choose_format

:save_config
> config.json echo {"format":"%SAVE_FORMAT%"}
if errorlevel 1 (
    echo ERROR: Could not create config.json.
    goto :fail
)

echo.
echo ===============================================
echo Setup completed successfully.
echo Output format: %SAVE_FORMAT%
echo.
echo Double-click run.bat to start the scraper.
echo ===============================================
echo.
pause
exit /b 0

:find_python
set "PYTHON_EXE="
set "PYTHON_ARGS="

rem 1) Python Launcher / PATH.
where py >nul 2>nul
if not errorlevel 1 (
    py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_EXE=py"
        set "PYTHON_ARGS=-3"
        exit /b 0
    )
)

where python >nul 2>nul
if not errorlevel 1 (
    python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_EXE=python"
        set "PYTHON_ARGS="
        exit /b 0
    )
)

rem 2) Common install locations.
call :try_python_path "%LocalAppData%\Programs\Python\Python313\python.exe"
if defined PYTHON_EXE exit /b 0
call :try_python_path "%LocalAppData%\Programs\Python\Python312\python.exe"
if defined PYTHON_EXE exit /b 0
call :try_python_path "%LocalAppData%\Programs\Python\Python311\python.exe"
if defined PYTHON_EXE exit /b 0
call :try_python_path "%LocalAppData%\Programs\Python\Python310\python.exe"
if defined PYTHON_EXE exit /b 0

call :try_python_path "%ProgramFiles%\Python313\python.exe"
if defined PYTHON_EXE exit /b 0
call :try_python_path "%ProgramFiles%\Python312\python.exe"
if defined PYTHON_EXE exit /b 0
call :try_python_path "%ProgramFiles%\Python311\python.exe"
if defined PYTHON_EXE exit /b 0
call :try_python_path "%ProgramFiles%\Python310\python.exe"
if defined PYTHON_EXE exit /b 0

rem 3) WinGet-specific install/link directories.
call :try_python_path "%LocalAppData%\Microsoft\WinGet\Links\python.exe"
if defined PYTHON_EXE exit /b 0

if exist "%LocalAppData%\Programs\Python\" (
    for /f "delims=" %%P in ('where /r "%LocalAppData%\Programs\Python" python.exe 2^>nul') do (
        call :try_python_path "%%P"
        if defined PYTHON_EXE exit /b 0
    )
)

if exist "%LocalAppData%\Microsoft\WinGet\Packages\" (
    for /f "delims=" %%P in ('where /r "%LocalAppData%\Microsoft\WinGet\Packages" python.exe 2^>nul') do (
        call :try_python_path "%%P"
        if defined PYTHON_EXE exit /b 0
    )
)
exit /b 0

:try_python_path
if not exist "%~1" exit /b 0
"%~1" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_EXE=%~1"
    set "PYTHON_ARGS="
)
exit /b 0

:fail
echo.
echo Setup did not complete.
echo Fix the error above and run setup.bat again.
echo.
pause
exit /b 1
