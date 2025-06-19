@echo off
title Apollo Project Orchestrator - Initial Setup
color 0A

echo ===========================================================
echo    APOLLO PROJECT ORCHESTRATOR - INITIAL SETUP
echo ===========================================================
echo.
echo Este script ira configurar o ambiente de desenvolvimento
echo para o Apollo Project Orchestrator.
echo.
echo Pressione qualquer tecla para continuar ou Ctrl+C para cancelar...
pause >nul
echo.

REM Verificar estrutura do projeto
if not exist "backend" (
    echo [ERRO] Diretorio 'backend' nao encontrado!
    echo Execute este arquivo a partir do diretorio raiz do projeto.
    pause
    exit /b 1
)

if not exist "frontend" (
    echo [ERRO] Diretorio 'frontend' nao encontrado!
    echo Execute este arquivo a partir do diretorio raiz do projeto.
    pause
    exit /b 1
)

echo [INFO] Estrutura do projeto verificada!
echo.

REM ===========================================================
REM SETUP BACKEND
REM ===========================================================
echo [STEP 1/3] Configurando Backend Python/Flask...
cd backend

REM Criar ambiente virtual se não existir
if not exist ".venv" (
    echo [INFO] Criando ambiente virtual Python...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual!
        echo Verifique se o Python esta instalado corretamente.
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado!
) else (
    echo [INFO] Ambiente virtual ja existe
)

REM Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Atualizar pip
echo [INFO] Atualizando pip...
python -m pip install --upgrade pip >nul 2>&1

REM Instalar dependencias (com tratamento especial para Windows)
echo [INFO] Detectando sistema e instalando dependencias apropriadas...

REM Primeiro tentar instalar dependências básicas essenciais
echo [INFO] Instalando dependencias criticas...
pip install flask flask-sqlalchemy flask-cors python-dotenv requests
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias criticas!
    pause
    exit /b 1
)

REM Instalar dependências opcionais (podem falhar sem quebrar o sistema)
echo [INFO] Instalando dependencias opcionais...
pip install flask-jwt-extended >nul 2>&1 || echo [AVISO] flask-jwt-extended nao instalado
pip install openai >nul 2>&1 || echo [AVISO] openai nao instalado - funcionara em modo simulacao
pip install bcrypt >nul 2>&1 || echo [AVISO] bcrypt nao instalado
pip install email-validator >nul 2>&1 || echo [AVISO] email-validator nao instalado
pip install flask-migrate >nul 2>&1 || echo [AVISO] flask-migrate nao instalado
pip install alembic >nul 2>&1 || echo [AVISO] alembic nao instalado

REM Tentar instalar do requirements se existir (sem falhar se der erro)
if exist "requirements\base.txt" (
    echo [INFO] Tentando instalar requirements\base.txt ^(ignorando erros^)...
    pip install -r requirements\base.txt --ignore-installed --no-deps >nul 2>&1 || echo [AVISO] Alguns pacotes do requirements falharam - continuando
) else if exist "requirements.txt" (
    echo [INFO] Tentando instalar requirements.txt ^(ignorando erros^)...
    pip install -r requirements.txt --ignore-installed --no-deps >nul 2>&1 || echo [AVISO] Alguns pacotes do requirements falharam - continuando
)

REM Criar arquivo .env se não existir
if not exist ".env" (
    if exist ".env_example.sh" (
        echo [INFO] Criando arquivo .env a partir do exemplo...
        copy ".env_example.sh" ".env" >nul
        echo [INFO] Configure o arquivo .env com suas chaves de API
    ) else (
        echo [INFO] Criando arquivo .env basico...
        (
            echo SECRET_KEY=apollo-secret-key-change-in-production
            echo DATABASE_URL=sqlite:///apollo.db
            echo OPENAI_API_KEY=sua-chave-da-openai-aqui
            echo FLASK_ENV=development
        ) > .env
        echo [INFO] Arquivo .env criado. Configure suas chaves de API!
    )
) else (
    echo [INFO] Arquivo .env ja existe
)

REM Inicializar banco de dados
if exist "create_db.py" (
    echo [INFO] Inicializando banco de dados...
    python create_db.py
) else if exist "src\create_db.py" (
    echo [INFO] Inicializando banco de dados...
    python src\create_db.py
) else (
    echo [INFO] Script de criacao do banco nao encontrado
)

echo [OK] Backend configurado com sucesso!
echo.

REM ===========================================================
REM SETUP FRONTEND
REM ===========================================================
echo [STEP 2/3] Configurando Frontend React/Vite...
cd ..\frontend

REM Verificar se package.json existe
if not exist "package.json" (
    echo [ERRO] package.json nao encontrado no frontend!
    pause
    exit /b 1
)

REM Instalar dependencias
echo [INFO] Instalando dependencias do frontend...
call npm install
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias do frontend!
    echo Verifique se o Node.js esta instalado corretamente.
    pause
    exit /b 1
)

echo [OK] Frontend configurado com sucesso!
echo.

REM ===========================================================
REM VERIFICACAO FINAL
REM ===========================================================
echo [STEP 3/3] Verificacao final...

REM Voltar para backend e testar imports
cd ..\backend
call .venv\Scripts\activate.bat

echo [TEST] Testando imports Python...
python -c "import flask; print('Flask OK')" 2>nul || echo [ERRO] Flask nao importa
python -c "import flask_sqlalchemy; print('SQLAlchemy OK')" 2>nul || echo [AVISO] SQLAlchemy nao importa
python -c "import flask_cors; print('CORS OK')" 2>nul || echo [AVISO] CORS nao importa

REM Voltar para raiz
cd ..

echo.
echo ===========================================================
echo           CONFIGURACAO CONCLUIDA COM SUCESSO!
echo ===========================================================
echo.
echo Proximos passos:
echo.
echo 1. Configure suas chaves de API no arquivo backend\.env
echo    ^> OPENAI_API_KEY=sua-chave-da-openai
echo.
echo 2. Execute o sistema:
echo    ^> start-apollo.bat
echo.
echo 3. Acesse a aplicacao:
echo    ^> http://localhost:5173
echo.
echo Para diagnosticar problemas:
echo    ^> diagnose-apollo.bat
echo.

pause