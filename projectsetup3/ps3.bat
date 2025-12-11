@echo off
setlocal enabledelayedexpansion

REM ============================================
REM  ProjectSetup 3.0 - Launcher
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
    pause
    exit /b 1
)

REM Verifica se o ambiente virtual existe
if exist "%SCRIPT_DIR%..\venv\Scripts\activate.bat" (
    echo [INFO] Ativando ambiente virtual...
    call "%SCRIPT_DIR%..\venv\Scripts\activate.bat"
)

REM Verifica se index.py existe
if not exist "%SCRIPT_DIR%index.py" (
    echo [ERRO] Arquivo index.py nao encontrado em: %SCRIPT_DIR%
    pause
    exit /b 1
)

REM Executa o script principal
echo [INFO] Iniciando ProjectSetup 3.0...
python "%SCRIPT_DIR%index.py" %*

REM Captura o código de saída
set "EXIT_CODE=%ERRORLEVEL%"

REM Volta para o diretório original
cd /d "%CUR_DIR%"

REM Retorna o código de saída
exit /b %EXIT_CODE%
