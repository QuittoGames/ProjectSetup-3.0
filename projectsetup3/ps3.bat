@echo off
REM Salva o diretório atual
set CUR_DIR=%CD%

REM Vai para a pasta onde está o script
cd /d D:\Projects\Python\ProjectSetup-3.0\

REM Ativa o ambiente virtual (se tiver)
REM call ..\venv\Scripts\activate.bat

REM Executa o script
python index.py

REM Volta pro diretório original
cd /d %CUR_DIR%
