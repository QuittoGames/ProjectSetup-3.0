@echo off
setlocal enabledelayedexpansion

REM ============================================
REM  ProjectSetup 3.0 - Interactive Launcher
REM  Executa a interface interativa do sistema
REM ============================================

REM Salva o diretório atual do usuário
set "CUR_DIR=%CD%"

REM Define o diretório do script (sempre relativo ao .bat, não ao diretório atual)
set "SCRIPT_DIR=%~dp0"

REM Muda para o diretório do script para garantir paths relativos corretos
cd /d "%SCRIPT_DIR%"

REM Debug - mostra onde está executando
echo [DEBUG] Diretorio do script: %SCRIPT_DIR%
echo [DEBUG] Diretorio atual: %CD%
echo.
timeout /t 5 /nobreak
echo.

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
        timeout /t 3 /nobreak >nul
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
        if errorlevel 1 (
            echo [ERRO] Falha ao instalar dependencias!
            pause
            exit /b 1
        )
    ) else (
        python -m pip install -q rich
        if errorlevel 1 (
            echo [ERRO] Falha ao instalar rich!
            pause
            exit /b 1
        )
    )
)

REM Executa o script principal
echo [INFO] Iniciando ProjectSetup 3.0 (modo interativo)...
echo.
python "%SCRIPT_DIR%index.py" %* 2>&1

REM Captura o código de saída
set "EXIT_CODE=%ERRORLEVEL%"

REM Sempre pausa no final para ver mensagens (erro ou sucesso)
echo.
if !EXIT_CODE! neq 0 (
    echo [ERRO] Programa encerrado com codigo de erro: !EXIT_CODE!
    echo        Pressione qualquer tecla para fechar...
) else (
    echo [OK] Programa finalizado com sucesso!
    echo      Fechando em 2 segundos...
    timeout /t 2 /nobreak >nul 2>&1
    goto :skip_pause
)   
echo.
pause >nul
:skip_pause

REM Volta para o diretório original
cd /d "%CUR_DIR%"

REM Retorna o código de saída
exit /b %EXIT_CODE%
