@echo off
set CUR_DIR=%CD%

cd /d D:\Projects\Python\ProjectSetup-3.0\Services

pythonw CLIService.py %*

cd /d %CUR_DIR%
