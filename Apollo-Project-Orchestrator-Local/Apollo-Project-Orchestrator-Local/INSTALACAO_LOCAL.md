# Apollo Project Orchestrator - Instruções de Instalação Local

## Visão Geral
O Apollo Project Orchestrator é um sistema completo de gestão de projetos com IA integrada. Este pacote contém todas as correções implementadas para resolver o problema de avanço automático de etapas.

## Estrutura do Projeto
```
Apollo-Project-Orchestrator/
├── frontend/                 # Aplicação React
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── backend/                  # API Flask
│   ├── src/
│   ├── requirements.txt
│   ├── .env
│   └── ...
├── docs/                     # Documentação
└── README.md
```

## Pré-requisitos

### Node.js (para o Frontend)
- **Versão recomendada**: 18.x ou superior
- **Download**: https://nodejs.org/
- **Verificar instalação**: `node --version` e `npm --version`

### Python (para o Backend)
- **Versão recomendada**: 3.8 ou superior
- **Download**: https://python.org/
- **Verificar instalação**: `python --version` e `pip --version`

## Instalação e Configuração

### 1. Clonar/Extrair o Projeto
```bash
# Extrair o arquivo ZIP no caminho desejado
# C:\Users\hfnetto\OneDrive - Stefanini\Documents\GitHub\Apollo-Project-Orchestrator
```

### 2. Configurar o Backend

#### 2.1. Navegar para a pasta do backend
```bash
cd backend
```

#### 2.2. Criar ambiente virtual (recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

#### 2.3. Instalar dependências
```bash
pip install -r requirements.txt
```

#### 2.4. Configurar variáveis de ambiente
Edite o arquivo `.env` e configure sua chave da OpenAI:
```
SECRET_KEY=apollo-secret-key-change-in-production
DATABASE_URL=sqlite:///apollo.db
OPENAI_API_KEY=sua-chave-da-openai-aqui
```

#### 2.5. Inicializar banco de dados
```bash
python src/main.py
```

### 3. Configurar o Frontend

#### 3.1. Navegar para a pasta do frontend
```bash
cd ../frontend
```

#### 3.2. Instalar dependências
```bash
npm install
```

#### 3.3. Configurar URL da API
Verifique se o arquivo `src/services/api.js` está configurado para:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

## Execução

### 1. Iniciar o Backend
```bash
cd backend
python src/main.py
```
O backend estará disponível em: http://localhost:5000

### 2. Iniciar o Frontend (em outro terminal)
```bash
cd frontend
npm run dev
```
O frontend estará disponível em: http://localhost:5173

## Funcionalidades Implementadas

### ✅ Correções Principais
- **Problema de Avanço Automático**: Resolvido com arquitetura robusta de controle de estado
- **Sistema de Lock**: Bloqueia mudanças de etapa durante processamento da IA
- **Logs Detalhados**: Sistema completo de monitoramento para debug
- **Proteções Múltiplas**: Várias camadas de verificação de estado
- **Interface Melhorada**: Caixas de interação com fundo branco e layout otimizado

### ✅ Funcionalidades Principais
- **Gestão de Projetos**: Criar, editar e gerenciar projetos
- **Upload de Documentos**: Anexar arquivos ao projeto
- **Análise de IA**: Geração automática de perguntas críticas
- **Fluxo Multi-etapas**: Navegação controlada entre etapas
- **Integração OpenAI**: Análise real de documentos (quando configurada)

## Solução de Problemas

### Backend não inicia
- Verifique se o Python está instalado corretamente
- Certifique-se de que todas as dependências foram instaladas
- Verifique se a porta 5000 não está sendo usada por outro processo

### Frontend não carrega
- Verifique se o Node.js está instalado corretamente
- Execute `npm install` novamente se necessário
- Certifique-se de que a porta 5173 não está sendo usada

### Erro de CORS
- Verifique se o backend está rodando
- Confirme se a URL da API no frontend está correta
- O backend já está configurado para aceitar requisições do frontend

### Análise da IA não funciona
- Verifique se a chave da OpenAI está configurada no arquivo `.env`
- O sistema possui fallback para simulação local caso a API não esteja disponível
- Verifique os logs do backend para mais detalhes

## Desenvolvimento

### Estrutura do Código

#### Frontend (React)
- `src/App.jsx`: Componente principal com toda a lógica de estado
- `src/components/`: Componentes reutilizáveis
- `src/services/api.js`: Serviços de comunicação com a API

#### Backend (Flask)
- `src/main.py`: Arquivo principal da aplicação
- `src/routes/`: Rotas da API organizadas por funcionalidade
- `src/models/`: Modelos de dados

### Logs e Debug
O sistema possui logs detalhados que podem ser visualizados:
- **Frontend**: Console do navegador (F12)
- **Backend**: Terminal onde o servidor está rodando

## Suporte
Para problemas ou dúvidas, verifique:
1. Os logs do console (frontend)
2. Os logs do terminal (backend)
3. A documentação das APIs utilizadas
4. As configurações de ambiente

## Próximos Passos
1. Configure sua chave da OpenAI para análise real de documentos
2. Personalize o sistema conforme suas necessidades
3. Implemente novas funcionalidades seguindo a arquitetura existente

