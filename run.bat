# Multi-Agent AI CLI Launcher for Windows
@echo off
setlocal

cd /d "%~dp0"

if "%1"=="" (
    python src\cli.py --help
    goto :eof
)

python src\cli.py %*
