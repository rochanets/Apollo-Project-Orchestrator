# 🚀 Guia de Início Rápido - Apollo Project Orchestrator

## ⚡ Instalação Express (5 minutos)

### 1️⃣ Pré-requisitos
Certifique-se de ter instalado:
- **Node.js 18+**: https://nodejs.org/
- **Python 3.8+**: https://python.org/

### 2️⃣ Extrair e Navegar
```bash
# Extrair o ZIP para:
# C:\Users\hfnetto\OneDrive - Stefanini\Documents\GitHub\Apollo-Project-Orchestrator

cd "C:\Users\hfnetto\OneDrive - Stefanini\Documents\GitHub\Apollo-Project-Orchestrator"
```

### 3️⃣ Configurar Backend (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
python src/main.py
```
✅ Backend rodando em: http://localhost:5000

### 4️⃣ Configurar Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
✅ Frontend rodando em: http://localhost:5173

### 5️⃣ Acessar Sistema
Abra seu navegador em: **http://localhost:5173**

## 🔧 Configuração da OpenAI (Opcional)

Para análise real de documentos, edite `backend/.env`:
```env
OPENAI_API_KEY=sua-chave-da-openai-aqui
```

## ✅ Verificação Rápida

### Backend Funcionando?
- Acesse: http://localhost:5000/api/health
- Deve retornar: `{"status": "ok"}`

### Frontend Funcionando?
- Acesse: http://localhost:5173
- Deve carregar a interface do Apollo

## 🎯 Primeiros Passos

1. **Criar Projeto**: Clique em "Novo" na sidebar
2. **Upload Documentos**: Vá para Etapa 1 e faça upload
3. **Análise IA**: Na Etapa 2, clique "Iniciar Análise da IA"
4. **Responder Perguntas**: Preencha as respostas geradas
5. **Navegar Etapas**: Use os botões de navegação

## 🚨 Problemas Comuns

### ❌ "pip não encontrado"
```bash
# Windows
python -m pip install -r requirements.txt

# Ou instalar pip
python -m ensurepip --upgrade
```

### ❌ "npm não encontrado"
- Reinstalar Node.js: https://nodejs.org/
- Verificar PATH do sistema

### ❌ "Porta em uso"
```bash
# Verificar portas
netstat -an | findstr "5000"
netstat -an | findstr "5173"

# Matar processo se necessário
taskkill /F /PID <numero_do_processo>
```

### ❌ Erro de CORS
- Verificar se backend está rodando
- Confirmar URL no frontend: `src/services/api.js`

## 📞 Suporte Rápido

### Logs Importantes
- **Frontend**: Console do navegador (F12)
- **Backend**: Terminal onde está rodando

### Comandos de Debug
```bash
# Verificar versões
node --version
python --version
pip --version

# Reinstalar dependências
cd frontend && rm -rf node_modules && npm install
cd backend && pip install -r requirements.txt --force-reinstall
```

## 🎉 Pronto!

Agora você tem o Apollo Project Orchestrator rodando localmente com todas as correções implementadas!

**Próximo passo**: Configure sua chave da OpenAI para análise real de documentos.

---

**Tempo total de instalação: ~5 minutos** ⏱️

