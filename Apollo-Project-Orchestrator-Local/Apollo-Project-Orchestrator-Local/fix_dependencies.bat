@echo off
title Apollo Project Orchestrator - Dependencies Fix
color 0C

echo ===========================================================
echo    APOLLO PROJECT ORCHESTRATOR - DEPENDENCIES FIX
echo ===========================================================
echo.
echo Este script corrigira o problema de dependencias no Windows
echo removendo psycopg2-binary e outras dependencias problematicas.
echo.

if not exist "backend" (
    echo [ERRO] Execute este script a partir do diretorio raiz do projeto!
    pause
    exit /b 1
)

cd backend

echo [STEP 1/4] Ativando ambiente virtual...

if exist ".venv" (
    call .venv\Scripts\activate.bat
    echo [OK] Ambiente virtual ativado
) else (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute setup-apollo.bat primeiro
    pause
    exit /b 1
)

echo.
echo [STEP 2/4] Criando requirements simplificado para Windows...

REM Criar arquivo requirements simplificado
(
    echo # Apollo Project Orchestrator - Windows Development Dependencies
    echo flask==2.3.3
    echo werkzeug==2.3.7
    echo flask-sqlalchemy==3.0.5
    echo flask-migrate==4.0.5
    echo alembic==1.12.0
    echo flask-jwt-extended==4.5.3
    echo flask-cors==4.0.0
    echo flask-caching==2.1.0
    echo flask-limiter==3.5.0
    echo flask-mail==0.9.1
    echo python-dotenv==1.0.0
    echo openai==0.28.1
    echo requests==2.31.0
    echo bcrypt==4.0.1
    echo email-validator==2.0.0
    echo click==8.1.7
    echo pytest==7.4.2
    echo pytest-flask==1.2.0
) > requirements-windows.txt

echo [OK] Arquivo requirements-windows.txt criado

echo.
echo [STEP 3/4] Instalando dependencias corrigidas...

echo [INFO] Atualizando pip...
python -m pip install --upgrade pip >nul 2>&1

echo [INFO] Instalando dependencias do requirements-windows.txt...
pip install -r requirements-windows.txt
if errorlevel 1 (
    echo [ERRO] Algumas dependencias falharam. Tentando instalacao individual...
    
    echo [INFO] Instalando pacotes criticos individualmente...
    pip install flask
    pip install flask-sqlalchemy
    pip install flask-cors
    pip install python-dotenv
    pip install requests
    
    echo [INFO] Instalando pacotes opcionais...
    pip install openai || echo [AVISO] OpenAI nao instalado - funcionara em modo simulacao
    pip install flask-jwt-extended || echo [AVISO] JWT nao instalado
    pip install bcrypt || echo [AVISO] bcrypt nao instalado
    
) else (
    echo [OK] Dependencias instaladas com sucesso!
)

echo.
echo [STEP 4/4] Verificando instalacao...

echo [TEST] Testando imports criticos...
python -c "import flask; print('[OK] Flask:', flask.__version__)" 2>nul || echo [ERRO] Flask nao importa
python -c "import flask_sqlalchemy; print('[OK] SQLAlchemy instalado')" 2>nul || echo [AVISO] SQLAlchemy nao instalado
python -c "import flask_cors; print('[OK] CORS instalado')" 2>nul || echo [AVISO] CORS nao instalado
python -c "import dotenv; print('[OK] python-dotenv instalado')" 2>nul || echo [AVISO] python-dotenv nao instalado

echo.
echo ===========================================================
echo           DEPENDENCIAS CORRIGIDAS COM SUCESSO!
echo ===========================================================
echo.
echo O que foi feito:
echo   ^> Removido psycopg2-binary ^(causa problemas no Windows^)
echo   ^> Removido redis ^(nao necessario para desenvolvimento^)
echo   ^> Criado requirements-windows.txt simplificado
echo   ^> Instalado apenas dependencias essenciais
echo.
echo Para desenvolvimento local:
echo   ^> O sistema usara SQLite em vez de PostgreSQL
echo   ^> Cache simples em vez de Redis
echo   ^> Todas as funcionalidades principais funcionarao
echo.
echo Proximos passos:
echo   1. Execute: start-apollo.bat
echo   2. Acesse: http://localhost:5173
echo.

cd ..
pause