#!/bin/bash

# Script de Início Rápido - Apollo Project Orchestrator Frontend

echo "🚀 Iniciando Apollo Project Orchestrator Frontend..."

# 1. Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Instale Node.js 18+ antes de continuar."
    exit 1
fi

# 2. Verificar versão do Node.js
NODE_VERSION=$(node -v | cut -d. -f1 | cut -dv -f2)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js versão 18+ necessária. Versão atual: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detectado"

# 3. Navegar para o diretório do frontend
cd frontend || {
    echo "❌ Diretório 'frontend' não encontrado"
    exit 1
}

# 4. Verificar se o backend está rodando
echo "🔍 Verificando se o backend está rodando..."
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Backend detectado em http://localhost:5000"
else
    echo "⚠️  Backend não detectado. Certifique-se de que o servidor está rodando na porta 5000"
    echo "   Execute no diretório raiz: python app.py"
fi

# 5. Instalar dependências se necessário
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências..."
    npm install
else
    echo "✅ Dependências já instaladas"
fi

# 6. Criar arquivo .env.local se não existir
if [ ! -f ".env.local" ]; then
    echo "⚙️  Criando arquivo de configuração .env.local..."
    cat > .env.local << EOF
VITE_API_URL=http://localhost:5000
VITE_APP_NAME=Apollo Project Orchestrator
VITE_APP_VERSION=1.0.0
VITE_ENABLE_DEBUG=true
EOF
    echo "✅ Arquivo .env.local criado"
fi

# 7. Verificar portas
if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Porta 5173 já está em uso. Encerrando processo..."
    pkill -f "vite.*5173" || true
    sleep 2
fi

# 8. Iniciar o servidor de desenvolvimento
echo "🎯 Iniciando servidor de desenvolvimento na porta 5173..."
echo "📱 Acesse: http://localhost:5173"
echo "🛑 Para parar: Ctrl+C"
echo ""

npm run dev