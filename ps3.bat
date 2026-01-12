@echo off
setlocal enabledelayedexpansion

REM ============================================
REM  ProjectSetup 3.0 - Interactive Launcher
REM  Windows / Batch
REM ============================================

REM Salva o diretório atual do usuário
set "CUR_DIR=%CD%"

REM Define o diretório do script (sempre relativo ao .bat, não ao diretório atual)
set "SCRIPT_DIR=%~dp0"

REM Muda para o diretório do script para garantir paths relativos corretos
cd /d "%SCRIPT_DIR%"

echo [INFO] Project root: %SCRIPT_DIR%
echo.

REM --- Verifica Python ---
python --version >nul 2>nul
if errorlevel 1 (
    echo [ERRO] Python 3 nao encontrado no PATH!
    pause
    exit /b 1
)

REM Captura versão do Python
for /f "tokens=2" %%i in ('python --version 2^>nul') do set PY_VERSION=%%i
echo [INFO] Python %PY_VERSION% detectado

REM --- Ativa venv se existir ---
if exist "%SCRIPT_DIR%venv\Scripts\activate.bat" (
    echo [INFO] Ativando venv...
    call "%SCRIPT_DIR%venv\Scripts\activate.bat"
) else (
    echo [INFO] Usando Python global
)

REM --- Instala todas dependências do requirements.txt ---
set "REQ_FILE=%SCRIPT_DIR%projectsetup3\requirements\requirements.txt"
if exist "%REQ_FILE%" (
    echo [INFO] Instalando todas dependencias de %REQ_FILE% ...
    python -m pip install --user -r "%REQ_FILE%"
) else (
    echo [WARN] requirements.txt nao encontrado em %REQ_FILE%
)

REM --- Instala pacote local projectsetup3 (editable) ---
python -c "import projectsetup3" >nul 2>nul
if errorlevel 1 (
    echo [WARN] Modulo projectsetup3 nao encontrado
    echo [INFO] Adicionando diretorio ao PYTHONPATH...
    set "PYTHONPATH=%SCRIPT_DIR%;%PYTHONPATH%"
)

REM --- Executa o pacote ProjectSetup ---
echo.
echo [INFO] Iniciando ProjectSetup 3.0...
echo.
python -m projectsetup3 %*
set "EXIT_CODE=%ERRORLEVEL%"

REM --- Finalizacao ---
echo.
if !EXIT_CODE! neq 0 (
    echo [ERRO] Encerrado com codigo !EXIT_CODE!
    echo Pressione qualquer tecla para sair...
    pause >nul
) else (
    echo [OK] Finalizado com sucesso!
    timeout /t 2 /nobreak >nul
)

REM Volta para o diretório original
cd /d "%CUR_DIR%"

REM Retorna o código de saída
exit /b %EXIT_CODE%
