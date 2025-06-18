# Apollo Project Orchestrator

## 🚀 Visão Geral
O Apollo Project Orchestrator é uma solução completa baseada em IA que auxilia na estruturação, coleta, análise e execução de projetos, desde a concepção até o Go-Live, de forma automatizada e colaborativa.

## ✨ Funcionalidades Principais

### 🎯 Gestão Inteligente de Projetos
- **Cadastro Completo**: Nome, cliente, responsável, objetivos e prioridades
- **Fluxo Multi-etapas**: 8 etapas estruturadas do projeto
- **Controle de Estado**: Sistema robusto que previne avanços automáticos indesejados

### 📄 Processamento de Documentos
- **Upload Múltiplo**: Suporte a diversos formatos de arquivo
- **Análise Automática**: IA processa documentos e extrai insights
- **Indexação**: Organização inteligente do conteúdo

### 🤖 Integração com IA
- **OpenAI Integration**: Análise real de documentos quando configurada
- **Fallback Inteligente**: Simulação local quando API não disponível
- **Geração de Perguntas**: Perguntas críticas contextualizadas automaticamente

### 🔧 Arquitetura Robusta
- **Sistema de Lock**: Previne mudanças de estado durante processamento
- **Logs Detalhados**: Monitoramento completo para debug
- **Proteções Múltiplas**: Várias camadas de verificação de integridade

## 🏗️ Arquitetura do Sistema

### Frontend (React)
- **Framework**: React 18 com Vite
- **UI Components**: Shadcn/UI + Tailwind CSS
- **Ícones**: Lucide React
- **Estado**: Hooks nativos do React com refs para controle rigoroso

### Backend (Flask)
- **Framework**: Flask com extensões
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Autenticação**: JWT
- **CORS**: Configurado para desenvolvimento local

## 📋 Etapas do Projeto

1. **📝 Cadastro do Projeto** - Informações básicas
2. **📤 Upload de Documentos** - Anexar documentação
3. **❓ Geração de Perguntas** - IA gera perguntas críticas
4. **📊 Coleta de Informações** - Documentação e esclarecimentos
5. **🔧 Análise Técnica** - Levantamento do ambiente
6. **💻 Execução do Projeto** - Desenvolvimento automatizado
7. **🧪 Testes** - Testes integrados e correções
8. **🚀 Go Live** - Documentação final e deploy

## 🛠️ Instalação e Configuração

### Pré-requisitos
- **Node.js** 18+ (para frontend)
- **Python** 3.8+ (para backend)
- **Git** (para versionamento)

### Instalação Rápida

#### 1. Backend
```bash
cd backend
pip install -r requirements.txt
# Configurar .env com sua chave OpenAI
python src/main.py
```

#### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

### Configuração da OpenAI
Edite o arquivo `backend/.env`:
```env
OPENAI_API_KEY=sua-chave-da-openai-aqui
```

## 🔍 Correções Implementadas

### ✅ Problema de Avanço Automático Resolvido
- **Sistema de Lock**: Bloqueia mudanças durante processamento
- **Refs para Estado**: Controle rigoroso com useRef
- **Verificações Múltiplas**: Proteções em várias camadas
- **Delays Estratégicos**: Tempo para estabilização do estado

### ✅ Interface Melhorada
- **Caixas Brancas**: Todas as caixas de interação com fundo branco
- **Layout Otimizado**: Tamanhos ajustados e espaçamento melhorado
- **Responsividade**: Funciona em desktop e mobile

### ✅ Logs e Monitoramento
- **Debug Completo**: Logs detalhados para desenvolvimento
- **Produção**: Logs específicos para ambiente de produção
- **Rastreamento**: Stack traces para identificação de problemas

## 🚨 Solução de Problemas

### Backend não inicia
```bash
# Verificar Python
python --version

# Reinstalar dependências
pip install -r requirements.txt

# Verificar porta
netstat -an | grep 5000
```

### Frontend não carrega
```bash
# Verificar Node.js
node --version

# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install

# Verificar porta
netstat -an | grep 5173
```

### Erro de CORS
- Verificar se backend está rodando
- Confirmar URL da API no frontend
- Backend já configurado para aceitar requisições locais

## 📊 Monitoramento e Debug

### Logs do Frontend
Abra o console do navegador (F12) para ver:
- Estados de navegação
- Processamento da IA
- Erros de comunicação com API

### Logs do Backend
Terminal onde o servidor está rodando mostra:
- Requisições recebidas
- Processamento da IA
- Erros de servidor

## 🔮 Próximos Passos

1. **Configurar OpenAI**: Para análise real de documentos
2. **Personalizar**: Adaptar às suas necessidades específicas
3. **Expandir**: Adicionar novas funcionalidades seguindo a arquitetura
4. **Deploy**: Preparar para ambiente de produção

## 📞 Suporte

Para problemas ou dúvidas:
1. Verificar logs do console (frontend)
2. Verificar logs do terminal (backend)
3. Consultar documentação das APIs
4. Revisar configurações de ambiente

## 📄 Licença

Este projeto foi desenvolvido como solução personalizada para gestão inteligente de projetos com IA.

---

**Desenvolvido com ❤️ usando React, Flask e OpenAI**

