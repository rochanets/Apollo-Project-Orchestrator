@echo off
echo ========================================
echo    Apollo Project Orchestrator
echo    Iniciando Backend e Frontend
echo ========================================

:: Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado. Por favor, instale o Python 3.8+
    pause
    exit /b 1
)

:: Verificar se Node.js está instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Node.js nao encontrado. Por favor, instale o Node.js
    pause
    exit /b 1
)

echo [1/4] Preparando ambiente do backend...
cd backend
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)
call venv\Scripts\activate

echo [2/4] Instalando dependencias do backend...
pip install -r ..\requirements.txt
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias do backend
    pause
    exit /b 1
)

echo [3/4] Instalando dependencias do frontend...
cd ..\frontend
call npm install
if errorlevel 1 (
    echo ERRO: Falha ao instalar dependencias do frontend
    pause
    exit /b 1
)

echo [4/4] Iniciando servicos...
echo.
echo Iniciando Backend em segundo plano...
cd ..\backend
start "Apollo Backend" cmd /k "venv\Scripts\activate && python -m src.main"

echo Aguardando 3 segundos para o backend inicializar...
timeout /t 3 /nobreak >nul

echo Iniciando Frontend...
cd ..\frontend
echo.
echo ========================================
echo   APOLLO PROJECT ORCHESTRATOR ATIVO
echo ========================================
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:5000
echo.
echo Para parar os servicos, feche as janelas.
echo ========================================
echo.
call npm run dev

pause