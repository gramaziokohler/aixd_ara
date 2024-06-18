@ECHO OFF
SETLOCAL EnableExtensions EnableDelayedExpansion

REM The following lines are courtesy of Windows' magnificent support for shell programming:
REM https://superuser.com/a/1166728
for /f %%a in ('copy /Z "%~dpf0" nul') do set "CR=%%a"
for /f %%a in ('"prompt $H&for %%b in (0) do rem"') do set "BS=%%a"

REM Retrieve current code page, before changing it
for /f "usebackq tokens=4" %%i in (`chcp`) do (
  set _PREV_CHCP=%%i
)

SET CONDA_PATH=%UserProfile%\Miniconda3
SET CONDA_ENV_NAME=aixd_ara

REM Switch code page, so that we can print extended ASCII
CHCP 65001 >nul

:select_rhino_version
set RHINO_VERSION=
set /p RHINO_VERSION="Select Rhino version (7 or 8) [7]:"
if not "%RHINO_VERSION%"=="" set RHINO_VERSION=%RHINO_VERSION:~0,1%
if "%RHINO_VERSION%"=="" set RHINO_VERSION=7
if "%RHINO_VERSION%"=="7" goto valid_rhino_version
if "%RHINO_VERSION%"=="8" goto valid_rhino_version

ECHO Invalid Rhino version, please choose either 7 or 8.
GOTO select_rhino_version

:valid_rhino_version

<nul set /p"=[√] Starting ARA installation..."
ECHO.

:check_conda_presence
<nul set /p"=[ ] Checking conda..."
WHERE conda >nul 2>&1

IF %ERRORLEVEL%==0 (
    <nul set /p"=!BS!!CR![√] Conda command found!"
    GOTO use_existing_conda
)
IF %ERRORLEVEL%==1 (
    <nul set /p"=!BS!!CR![x] Conda not found, we will install Miniconda"
)

ECHO.

<nul set /p"=[ ] Installing miniconda (Python distribution)..."
CALL curl -S -s -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
IF %ERRORLEVEL% neq 0 GOTO miniconda_download_failed
SET CONDA_COMMAND=%CONDA_PATH%\condabin\conda

REM The last argument must NOT be quoted according to the conda docs, and that works even for paths with spaces in them
START /wait /min "Starting miniconda installation..." "Miniconda3-latest-Windows-x86_64.exe" /InstallationType=JustMe /S /D=%CONDA_PATH%
IF %ERRORLEVEL%==2 (
    <nul set /p"=!BS!!CR![√] Miniconda seems to be already installed, will skip step and continue..."
    ECHO.
    GOTO compas_install
)
IF %ERRORLEVEL% neq 0 GOTO miniconda_install_failed
<nul set /p"=!BS!!CR![√] Installing miniconda (Python distribution)..."
ECHO.

:compas_install
<nul set /p"=[ ] Looking for virtual environment (%CONDA_ENV_NAME%)..."
CALL "%CONDA_COMMAND%" activate %CONDA_ENV_NAME% >nul 2>&1
IF %ERRORLEVEL%==0 (
    <nul set /p"=!BS!!CR![√] Virtual environment already exists! (%CONDA_ENV_NAME%)"
    ECHO.
    GOTO compas_install_to_rhino
)
<nul set /p"=!BS!!CR![√] Virtual environment not found, will create it now...                                     "
ECHO.

<nul set /p"=[ ] Creating virtual environment..."
CALL "%CONDA_COMMAND%" create -c conda-forge -n %CONDA_ENV_NAME% aixd aixd_ara compas flask python=3.9 -y >nul 2>&1
<nul set /p"=!BS!!CR![√] Created virtual environment '%CONDA_ENV_NAME%' successfully"
ECHO.

:conda_activate_virtual_env
ECHO ON
<nul set /p"=[ ] Activating virtual environment..."
CALL "%CONDA_COMMAND%" activate %CONDA_ENV_NAME%
IF %ERRORLEVEL% neq 0 GOTO conda_activate_failed
<nul set /p"=!BS!!CR![√] Activated virtual environment successfully"
ECHO.

:compas_install_to_rhino
<nul set /p"=[√] Activating environment '%CONDA_ENV_NAME%' for Rhino..."
ECHO.
<nul set /p"=[√] Environment location: %CONDA_PREFIX%"
python -m compas_rhino.install -v %RHINO_VERSION%.0
<nul set /p"=[√] Successfully installed ARA on Rhino"
ECHO.
GOTO end_of_installer

:use_existing_conda
for /f "tokens=* delims=" %%a in ('where conda') do (
    set "CONDA_COMMAND=%%a"
    goto found_conda
)
:found_conda
ECHO.
GOTO compas_install

:conda_activate_failed
ECHO.
ECHO Could not activate virtual environment. Exiting.
GOTO end_of_installer

:miniconda_install_failed
ECHO.
ECHO Could not install miniconda. Exiting.
GOTO end_of_installer

:miniconda_download_failed
ECHO.
ECHO Could not download miniconda. Exiting.
GOTO end_of_installer

:end_of_installer
SET _ERRORLEVEL=%ERRORLEVEL%
CHCP %_PREV_CHCP% >nul
PAUSE
EXIT /B %_ERRORLEVEL%
