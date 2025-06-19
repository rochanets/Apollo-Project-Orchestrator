@echo off
title Apollo Project Orchestrator - Startup
color 0A

echo ===========================================================
echo    APOLLO PROJECT ORCHESTRATOR - SYSTEM STARTUP
echo ===========================================================
echo.

REM Verificar se estamos no diretório correto
if not exist "backend" (
    echo [ERRO] Diretorio 'backend' nao encontrado!
    echo Execute este arquivo a partir do diretorio raiz do projeto.
    echo.
    pause
    exit /b 1
)

if not exist "frontend" (
    echo [ERRO] Diretorio 'frontend' nao encontrado!
    echo Execute este arquivo a partir do diretorio raiz do projeto.
    echo.
    pause
    exit /b 1
)

echo [INFO] Verificando estrutura do projeto...
echo [OK] Estrutura do projeto verificada com sucesso!
echo.

REM ===========================================================
REM CONFIGURAR BACKEND (Flask)
REM ===========================================================
echo [STEP 1/4] Configurando Backend Flask...
cd backend

REM Verificar se existe ambiente virtual
if exist ".venv" (
    echo [INFO] Ambiente virtual encontrado, ativando...
    call .venv\Scripts\activate.bat
) else (
    echo [INFO] Ambiente virtual nao encontrado.
    echo [INFO] Instalando dependencias globalmente...
)

REM Verificar e configurar arquivo de entrada Flask
if exist "src\main.py" (
    echo [INFO] Arquivo src\main.py encontrado
    set FLASK_APP=src.main
    set ENTRY_FILE=src\main.py
) else if exist "src\app.py" (
    echo [INFO] Encontrado src\app.py ^(Application Factory^)
    set FLASK_APP=src.app
    set ENTRY_FILE=src\app.py
) else if exist "app.py" (
    echo [INFO] Encontrado app.py na raiz do backend
    set FLASK_APP=app.py
    set ENTRY_FILE=app.py
) else (
    echo [AVISO] Nenhum arquivo de entrada Flask encontrado!
    echo [INFO] Criando arquivo src\main.py automaticamente...
    
    REM Criar diretório src se não existir
    if not exist "src" mkdir src
    
    REM Criar arquivo main.py básico
    (
        echo # Apollo Project Orchestrator - Auto-generated main.py
        echo from flask import Flask
        echo from flask_cors import CORS
        echo.
        echo app = Flask^(__name__^)
        echo app.config['SECRET_KEY'] = 'apollo-dev-secret'
        echo CORS^(app^)
        echo.
        echo @app.route^('/'^)
        echo def home^(^):
        echo     return {'status': 'ok', 'message': 'Apollo Project Orchestrator'}
        echo.
        echo if __name__ == '__main__':
        echo     app.run^(host='0.0.0.0', port=5000, debug=True^)
    ) > "src\main.py"
    
    echo [OK] Arquivo src\main.py criado automaticamente
    set FLASK_APP=src.main
    set ENTRY_FILE=src\main.py
)

REM Verificar se requirements.txt existe
if exist "requirements.txt" (
    echo [INFO] Instalando dependencias do requirements.txt...
    pip install -r requirements.txt >nul 2>&1
) else if exist "requirements\base.txt" (
    echo [INFO] Instalando dependencias do requirements\base.txt...
    pip install -r requirements\base.txt >nul 2>&1
) else (
    echo [AVISO] Arquivo requirements.txt nao encontrado!
    echo [INFO] Tentando instalar dependencias minimas...
    pip install flask flask-sqlalchemy flask-cors >nul 2>&1
)

REM Verificar se precisa criar o banco de dados
if exist "create_db.py" (
    echo [INFO] Inicializando banco de dados...
    python create_db.py
) else if exist "src\create_db.py" (
    echo [INFO] Inicializando banco de dados...
    python src\create_db.py
) else (
    echo [INFO] Script create_db.py nao encontrado, continuando...
)

echo [OK] Backend configurado com sucesso!
echo.

REM ===========================================================
REM CONFIGURAR FRONTEND (React/Vite)
REM ===========================================================
echo [STEP 2/4] Verificando Frontend...
cd ..\frontend

REM Verificar se node_modules existe
if not exist "node_modules" (
    echo [INFO] Instalando dependencias do frontend...
    call npm install
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependencias do frontend!
        echo [INFO] Verifique se o Node.js esta instalado.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Dependencias do frontend ja instaladas
)

echo [OK] Frontend verificado com sucesso!
echo.

REM ===========================================================
REM INICIAR SERVICOS
REM ===========================================================
echo [STEP 3/4] Iniciando servicos...

REM Voltar para o diretorio backend
cd ..\backend

REM Iniciar backend em nova janela
echo [INFO] Iniciando servidor Flask...
echo [INFO] Usando arquivo: %ENTRY_FILE%
start "Apollo Backend (Flask)" cmd /k "title Apollo Backend - %ENTRY_FILE% ^& color 0B ^& echo Servidor Flask iniciando com %ENTRY_FILE%... ^& echo. ^& python %ENTRY_FILE% || python -m %FLASK_APP% || flask run --host=0.0.0.0 --port=5000 --debug"

REM Aguardar um pouco para o backend inicializar
echo [INFO] Aguardando backend inicializar...
timeout /t 3 /nobreak >nul

REM Iniciar frontend em nova janela
echo [INFO] Iniciando servidor de desenvolvimento React...
cd ..\frontend
start "Apollo Frontend (React)" cmd /k "title Apollo Frontend ^& color 0E ^& echo Servidor React iniciando... ^& npm run dev"

REM Aguardar um pouco para o frontend inicializar
echo [INFO] Aguardando frontend inicializar...
timeout /t 5 /nobreak >nul

echo [OK] Servicos iniciados com sucesso!
echo.

REM ===========================================================
REM ABRIR APLICACAO NO NAVEGADOR
REM ===========================================================
echo [STEP 4/4] Abrindo aplicacao no navegador...

REM Aguardar mais um pouco para garantir que os serviços estão prontos
timeout /t 2 /nobreak >nul

REM Abrir o frontend no navegador
echo [INFO] Abrindo http://localhost:5173 no navegador...
start http://localhost:5173

echo.
echo ===========================================================
echo    APOLLO PROJECT ORCHESTRATOR INICIADO COM SUCESSO!
echo ===========================================================
echo.
echo Servicos rodando:
echo   ^> Backend (Flask):  http://localhost:5000
echo   ^> Frontend (React): http://localhost:5173
echo.
echo Para parar os servicos:
echo   1. Feche as janelas do Backend e Frontend
echo   2. Ou pressione Ctrl+C em cada terminal
echo.
echo Logs:
echo   ^> Backend:  Verifique a janela "Apollo Backend (Flask)"
echo   ^> Frontend: Verifique a janela "Apollo Frontend (React)"
echo.

REM Voltar para o diretório raiz
cd ..

echo Pressione qualquer tecla para fechar esta janela...
pause >nul