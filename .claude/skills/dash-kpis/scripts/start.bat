@echo off
REM Abre o painel do negocio no navegador. Nao precisa instalar nada.
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python 3 nao encontrado. Instale em python.org e marque "Add Python to PATH".
  pause
  exit /b 1
)
python server.py %*
