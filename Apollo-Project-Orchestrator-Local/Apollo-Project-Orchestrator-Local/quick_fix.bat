@echo off
title Apollo - Quick Fix
color 0A

echo ===========================================================
echo    APOLLO - SOLUCAO RAPIDA PARA DEPENDENCIAS
echo ===========================================================
echo.

cd backend
call .venv\Scripts\activate.bat

echo [QUICK FIX] Instalando apenas dependencias essenciais...

REM Instalar apenas o que é necessário para funcionar
pip install flask
pip install flask-sqlalchemy  
pip install flask-cors
pip install python-dotenv
pip install requests

echo.
echo [INFO] Dependencias essenciais instaladas!
echo [INFO] O psycopg2-binary sera ignorado ^(so precisa para PostgreSQL^)
echo [INFO] Para desenvolvimento local, SQLite e suficiente
echo.

echo [TESTE] Verificando se Flask funciona...
python -c "from flask import Flask; app = Flask('test'); print('✅ Flask funcionando!')" 2>nul && (
    echo [OK] Sistema pronto para uso!
) || (
    echo [ERRO] Ainda ha problemas...
)

echo.
echo Agora execute: start-apollo.bat
pause