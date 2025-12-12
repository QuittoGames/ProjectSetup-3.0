@echo off
setlocal

:: Diretório onde o .bat está
set SCRIPT_DIR=%~dp0

:: Caminho da pasta Services (ajuste se necessário)
set TARGET_DIR=%SCRIPT_DIR%projectsetup3\Services

:: Volta depois
set CUR_DIR=%CD%

cd /d "%TARGET_DIR%"
pythonw CLIService.py %*

cd /d "%CUR_DIR%"
endlocal
