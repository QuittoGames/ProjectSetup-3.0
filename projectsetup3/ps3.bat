@echo off
setlocal enabledelayedexpansion

REM ============================================
REM  ProjectSetup 3.0 - Interactive Launcher
REM  Executa a interface interativa do sistema
REM ============================================

REM Salva o diretório atual
set "CUR_DIR=%CD%"

REM Define o diretório do script (relativo ao .bat)
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao encontrado no PATH!
    echo        Instale Python 3.8+ e adicione ao PATH do sistema.
    echo.
    pause
    exit /b 1
)

REM Captura versão do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PY_VERSION=%%i

REM Verifica se o ambiente virtual existe
if exist "%SCRIPT_DIR%..\venv\Scripts\activate.bat" (
    echo [INFO] Ativando ambiente virtual Python %PY_VERSION%...
    call "%SCRIPT_DIR%..\venv\Scripts\activate.bat"
    if errorlevel 1 (
        echo [WARN] Falha ao ativar venv, continuando com Python global...
    )
) else (
    echo [INFO] Usando Python %PY_VERSION% (global)
)

REM Verifica se index.py existe
if not exist "%SCRIPT_DIR%index.py" (
    echo.
    echo [ERRO] Arquivo principal nao encontrado!
    echo        Esperado: %SCRIPT_DIR%index.py
    echo.
    pause
    exit /b 1
)

REM Verifica dependências críticas (rich)
python -c "import rich" 2>nul
if errorlevel 1 (
    echo.
    echo [WARN] Dependencias nao encontradas!
    echo        Instalando pacotes necessarios...
    echo.
    if exist "%SCRIPT_DIR%..\requirements\requirements.txt" (
        python -m pip install -q -r "%SCRIPT_DIR%..\requirements\requirements.txt"
    ) else (
        python -m pip install -q rich
    )
)

REM Executa o script principal
echo [INFO] Iniciando ProjectSetup 3.0 (modo interativo)...
echo.
python "%SCRIPT_DIR%index.py" %*

REM Captura o código de saída
set "EXIT_CODE=%ERRORLEVEL%"

if !EXIT_CODE! neq 0 (
    echo.
    echo [ERRO] Programa encerrado com codigo de erro: !EXIT_CODE!
    echo.
    pause
)

REM Volta para o diretório original
cd /d "%CUR_DIR%"

REM Retorna o código de saída
exit /b %EXIT_CODE%
