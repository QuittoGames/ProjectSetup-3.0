@echo off
setlocal enabledelayedexpansion

REM ============================================
REM  ProjectSetup 3.0 - CLI Launcher
REM  Executa a interface de linha de comando
REM ============================================

REM Salva o diretório atual
set "CUR_DIR=%CD%"

REM Define o diretório do script (relativo ao .bat)
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado! Instale Python 3.8+ e adicione ao PATH.
    exit /b 1
)

REM Verifica se o ambiente virtual existe
if exist "%SCRIPT_DIR%..\venv\Scripts\activate.bat" (
    call "%SCRIPT_DIR%..\venv\Scripts\activate.bat" >nul 2>&1
)

REM Verifica se CLIService.py existe
set "CLI_SCRIPT=%SCRIPT_DIR%Services\CLIService.py"
if not exist "!CLI_SCRIPT!" (
    echo [ERRO] CLIService.py nao encontrado em: %SCRIPT_DIR%Services\
    exit /b 1
)

REM Executa o CLI (usa python.exe, não pythonw, para manter console)
python "!CLI_SCRIPT!" %*

REM Captura o código de saída
set "EXIT_CODE=%ERRORLEVEL%"

REM Volta para o diretório original
cd /d "%CUR_DIR%"

REM Retorna o código de saída
exit /b %EXIT_CODE%
