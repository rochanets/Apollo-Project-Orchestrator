@echo off
title Apollo Project Orchestrator - System Diagnostic
color 0C

echo ===========================================================
echo    APOLLO PROJECT ORCHESTRATOR - SYSTEM DIAGNOSTIC
echo ===========================================================
echo.

echo [DIAGNOSTIC] Verificando sistema...
echo.

REM Verificar Python
echo [CHECK] Python installation:
python --version 2>nul
if errorlevel 1 (
    echo [ERRO] Python nao encontrado! Instale Python 3.8 ou superior.
    echo Download: https://python.org/
) else (
    echo [OK] Python instalado
)
echo.

REM Verificar Node.js
echo [CHECK] Node.js installation:
node --version 2>nul
if errorlevel 1 (
    echo [ERRO] Node.js nao encontrado! Instale Node.js 18 ou superior.
    echo Download: https://nodejs.org/
) else (
    echo [OK] Node.js instalado
    npm --version 2>nul
    if errorlevel 1 (
        echo [AVISO] npm nao encontrado!
    ) else (
        echo [OK] npm instalado
    )
)
echo.

REM Verificar pip
echo [CHECK] pip installation:
pip --version 2>nul
if errorlevel 1 (
    echo [ERRO] pip nao encontrado!
) else (
    echo [OK] pip instalado
)
echo.

REM Verificar estrutura do projeto
echo [CHECK] Project structure:
if exist "backend" (
    echo [OK] Diretorio backend encontrado
    
    if exist "backend\src" (
        echo [OK] Diretorio backend\src encontrado
    ) else (
        echo [AVISO] Diretorio backend\src nao encontrado
    )
    
    if exist "backend\src\main.py" (
        echo [OK] backend\src\main.py encontrado
    ) else if exist "backend\app.py" (
        echo [OK] backend\app.py encontrado
    ) else if exist "backend\src\app.py" (
        echo [OK] backend\src\app.py encontrado
    ) else (
        echo [ERRO] Nenhum arquivo de entrada Flask encontrado!
    )
    
    if exist "backend\requirements.txt" (
        echo [OK] backend\requirements.txt encontrado
    ) else if exist "backend\requirements\base.txt" (
        echo [OK] backend\requirements\base.txt encontrado
    ) else (
        echo [AVISO] requirements.txt nao encontrado
    )
    
    if exist "backend\.venv" (
        echo [OK] Ambiente virtual Python encontrado
    ) else (
        echo [INFO] Ambiente virtual nao encontrado - sera usado Python global
    )
    
) else (
    echo [ERRO] Diretorio backend nao encontrado!
)

if exist "frontend" (
    echo [OK] Diretorio frontend encontrado
    
    if exist "frontend\package.json" (
        echo [OK] frontend\package.json encontrado
    ) else (
        echo [ERRO] frontend\package.json nao encontrado!
    )
    
    if exist "frontend\node_modules" (
        echo [OK] node_modules instalado
    ) else (
        echo [INFO] node_modules nao encontrado - execute 'npm install' no frontend
    )
    
) else (
    echo [ERRO] Diretorio frontend nao encontrado!
)
echo.

REM Verificar portas
echo [CHECK] Port availability:
netstat -an | findstr ":5000" >nul
if errorlevel 1 (
    echo [OK] Porta 5000 (backend) disponivel
) else (
    echo [AVISO] Porta 5000 ja esta em uso!
)

netstat -an | findstr ":5173" >nul
if errorlevel 1 (
    echo [OK] Porta 5173 (frontend) disponivel
) else (
    echo [AVISO] Porta 5173 ja esta em uso!
)
echo.

REM Verificar dependências Python críticas
if exist "backend" (
    cd backend
    echo [CHECK] Python dependencies:
    python -c "import flask; print('[OK] Flask instalado:', flask.__version__)" 2>nul || echo [ERRO] Flask nao instalado
    python -c "import flask_sqlalchemy; print('[OK] Flask-SQLAlchemy instalado')" 2>nul || echo [AVISO] Flask-SQLAlchemy nao instalado
    python -c "import flask_cors; print('[OK] Flask-CORS instalado')" 2>nul || echo [AVISO] Flask-CORS nao instalado
    cd ..
)
echo.

REM Resumo
echo ===========================================================
echo                      RESUMO DO DIAGNOSTICO
echo ===========================================================
echo.
echo Para resolver problemas comuns:
echo.
echo 1. Se Python nao estiver instalado:
echo    ^> Baixe em https://python.org/
echo.
echo 2. Se Node.js nao estiver instalado:
echo    ^> Baixe em https://nodejs.org/
echo.
echo 3. Se as dependencias Python estiverem faltando:
echo    ^> cd backend
echo    ^> pip install -r requirements.txt
echo.
echo 4. Se as dependencias Node.js estiverem faltando:
echo    ^> cd frontend
echo    ^> npm install
echo.
echo 5. Se as portas estiverem em uso:
echo    ^> Feche outros aplicativos que possam estar usando as portas 5000 e 5173
echo    ^> Ou reinicie o computador
echo.

pause