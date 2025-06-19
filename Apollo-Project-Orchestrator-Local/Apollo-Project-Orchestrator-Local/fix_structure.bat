@echo off
title Apollo Project Orchestrator - Structure Fix
color 0E

echo ===========================================================
echo    APOLLO PROJECT ORCHESTRATOR - STRUCTURE FIX
echo ===========================================================
echo.
echo Este script corrigira problemas estruturais encontrados
echo no projeto Apollo Project Orchestrator.
echo.

if not exist "backend" (
    echo [ERRO] Execute este script a partir do diretorio raiz do projeto!
    pause
    exit /b 1
)

cd backend

echo [STEP 1/4] Verificando e criando estrutura basica...

REM Criar diretórios se não existirem
if not exist "src" mkdir src
if not exist "src\models" mkdir src\models
if not exist "src\routes" mkdir src\routes
if not exist "src\services" mkdir src\services
if not exist "src\utils" mkdir src\utils
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "instance" mkdir instance

echo [OK] Estrutura de diretorios verificada

echo.
echo [STEP 2/4] Criando arquivos __init__.py faltantes...

REM Criar __init__.py se não existirem
if not exist "src\__init__.py" (
    echo # Apollo Project Orchestrator - Pacote Principal > "src\__init__.py"
    echo __version__ = "1.0.0" >> "src\__init__.py"
    echo [INFO] Criado src\__init__.py
)

if not exist "src\models\__init__.py" (
    echo # Apollo Models Package > "src\models\__init__.py"
    echo [INFO] Criado src\models\__init__.py
)

if not exist "src\routes\__init__.py" (
    echo # Apollo Routes Package > "src\routes\__init__.py"
    echo [INFO] Criado src\routes\__init__.py
)

if not exist "src\services\__init__.py" (
    echo # Apollo Services Package > "src\services\__init__.py"
    echo [INFO] Criado src\services\__init__.py
)

if not exist "src\utils\__init__.py" (
    echo # Apollo Utils Package > "src\utils\__init__.py"
    echo [INFO] Criado src\utils\__init__.py
)

echo [OK] Arquivos __init__.py verificados

echo.
echo [STEP 3/4] Verificando arquivo principal main.py...

if not exist "src\main.py" (
    echo [INFO] Criando arquivo src\main.py...
    (
        echo """
        echo Apollo Project Orchestrator - Arquivo Principal
        echo """
        echo.
        echo import os
        echo import sys
        echo from pathlib import Path
        echo.
        echo # Adicionar diretorio raiz ao Python path
        echo root_dir = Path^(__file__^).parent.parent
        echo sys.path.insert^(0, str^(root_dir^)^)
        echo.
        echo from flask import Flask, jsonify
        echo from flask_cors import CORS
        echo.
        echo # Criar aplicacao Flask
        echo app = Flask^(__name__^)
        echo.
        echo # Configuracoes basicas
        echo app.config['SECRET_KEY'] = os.environ.get^('SECRET_KEY', 'apollo-dev-secret-key'^)
        echo app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get^('DATABASE_URL', 'sqlite:///apollo.db'^)
        echo app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        echo.
        echo # Inicializar CORS
        echo CORS^(app, origins=['http://localhost:3000', 'http://localhost:5173']^)
        echo.
        echo # Rotas basicas
        echo @app.route^('/'^)
        echo @app.route^('/health'^)
        echo def health_check^(^):
        echo     return jsonify^({
        echo         'status': 'ok',
        echo         'message': 'Apollo Project Orchestrator funcionando!',
        echo         'version': '1.0.0'
        echo     }^)
        echo.
        echo @app.route^('/api'^)
        echo def api_info^(^):
        echo     return jsonify^({
        echo         'name': 'Apollo Project Orchestrator API',
        echo         'version': '1.0.0',
        echo         'status': 'running'
        echo     }^)
        echo.
        echo if __name__ == '__main__':
        echo     print^("🚀 Apollo Project Orchestrator iniciando..."^)
        echo     print^("🌐 Servidor: http://localhost:5000"^)
        echo     
        echo     app.run^(
        echo         host='0.0.0.0',
        echo         port=5000,
        echo         debug=True,
        echo         threaded=True
        echo     ^)
    ) > "src\main.py"
    echo [OK] Arquivo src\main.py criado
) else (
    echo [INFO] Arquivo src\main.py ja existe
)

echo.
echo [STEP 4/4] Verificando arquivo .env...

if not exist ".env" (
    echo [INFO] Criando arquivo .env basico...
    (
        echo # Apollo Project Orchestrator - Environment Variables
        echo SECRET_KEY=apollo-secret-key-change-in-production
        echo DATABASE_URL=sqlite:///apollo.db
        echo OPENAI_API_KEY=sua-chave-da-openai-aqui
        echo FLASK_ENV=development
        echo CORS_ORIGINS=http://localhost:3000,http://localhost:5173
    ) > ".env"
    echo [OK] Arquivo .env criado
) else (
    echo [INFO] Arquivo .env ja existe
)

echo.
echo ===========================================================
echo                ESTRUTURA CORRIGIDA COM SUCESSO!
echo ===========================================================
echo.
echo Estrutura final:
echo   backend/
echo   ├── src/
echo   │   ├── __init__.py
echo   │   ├── main.py          ^<-- ARQUIVO PRINCIPAL
echo   │   ├── models/
echo   │   │   └── __init__.py
echo   │   ├── routes/
echo   │   │   └── __init__.py
echo   │   ├── services/
echo   │   │   └── __init__.py
echo   │   └── utils/
echo   │       └── __init__.py
echo   ├── logs/
echo   ├── uploads/
echo   ├── instance/
echo   └── .env
echo.
echo Agora voce pode:
echo   1. Executar: start-apollo.bat
echo   2. Ou manualmente: python src\main.py
echo.

cd ..
pause