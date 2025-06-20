@echo off
echo =====================================
echo Apollo Project Orchestrator
echo Instalacao de Dependencias Backend
echo =====================================

cd /d "%~dp0"

echo.
echo [1/4] Verificando ambiente virtual...
if not exist "venv\" (
    echo Criando ambiente virtual...
    python -m venv venv
)

echo.
echo [2/4] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo [3/4] Atualizando pip...
python -m pip install --upgrade pip

echo.
echo [4/4] Instalando dependencias compativel com Python 3.13...
pip uninstall -y sqlalchemy flask-sqlalchemy flask-migrate
pip install -r requirements.txt

echo.
echo =====================================
echo Instalacao concluida!
echo =====================================
echo.
echo Para iniciar o servidor:
echo   start.bat
echo.
pause