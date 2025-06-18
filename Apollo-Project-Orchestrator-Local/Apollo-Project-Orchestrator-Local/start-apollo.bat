@echo off
echo Iniciando Apollo Project Orchestrator...

REM Caminho absoluto para o backend
cd backend

REM Ativa o ambiente virtual
call .venv\Scripts\activate.bat

REM Inicializa o banco de dados (cria tabelas se não existirem)
python create_db.py

REM Abre o frontend em nova janela
start cmd /k "cd ../frontend && npm run dev"

REM Aguarda 3 segundos para o frontend subir
timeout /t 3 /nobreak > NUL

REM Abre o navegador na tela de login
start http://localhost:5173

REM Roda o backend com Flask
python -m src.main

pause
