@echo off
REM Salva o diretório atual
set CUR_DIR=%CD%

REM Vai para a pasta onde está o script
cd /d D:\Projects\Python\ProjectSetup-3.0\Services

REM Ativa o ambiente virtual (se tiver)
REM call ..\venv\Scripts\activate.bat

REM Executa o script
python CLIService.py

REM Volta pro diretório original
cd /d %CUR_DIR%
