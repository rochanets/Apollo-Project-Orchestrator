# Apollo Project Orchestrator - Frontend

## 🎨 Descrição
Interface React moderna e responsiva para o Apollo Project Orchestrator com sistema robusto de controle de estado.

## ✨ Funcionalidades
- **Interface Intuitiva**: Design limpo e profissional
- **Fluxo Multi-etapas**: Navegação controlada entre 8 etapas
- **Gestão de Estado Robusta**: Sistema com locks e proteções
- **Análise de IA**: Interface para processamento inteligente
- **Upload de Arquivos**: Drag & drop e seleção múltipla
- **Logs Detalhados**: Sistema completo de debug

## 🏗️ Arquitetura

### Tecnologias
- **React 18**: Framework principal
- **Vite**: Build tool e dev server
- **Tailwind CSS**: Estilização
- **Shadcn/UI**: Componentes de interface
- **Lucide React**: Ícones

### Estrutura de Pastas
```
src/
├── components/          # Componentes reutilizáveis
│   ├── ui/             # Componentes base (shadcn/ui)
│   ├── AuthPage.jsx    # Página de autenticação
│   └── CreateProjectModal.jsx  # Modal de criação
├── services/           # Serviços e APIs
│   └── api.js         # Cliente da API
├── assets/            # Recursos estáticos
│   └── apollo-logo.png
├── App.jsx            # Componente principal
├── App.css           # Estilos globais
└── main.jsx          # Ponto de entrada
```

## 🔧 Correções Implementadas

### Sistema de Controle de Estado
```javascript
// Refs para controle rigoroso
const currentStepRef = useRef(initialStep);
const isProcessingRef = useRef(false);
const stepLockRef = useRef(false);

// Sistema de lock
const lockStepChanges = (reason) => {
  stepLockRef.current = true;
  logStateChange('STEP_LOCK_ACTIVATED', false, true, reason);
};
```

### Proteções Múltiplas
- **Lock durante IA**: Bloqueia mudanças durante processamento
- **Verificação de Estado**: Monitora mudanças inesperadas
- **Delays Estratégicos**: Tempo para estabilização
- **Logs Detalhados**: Rastreamento completo

### Interface Melhorada
- **Caixas Brancas**: Fundo branco em todas as interações
- **Layout Responsivo**: Funciona em todos os dispositivos
- **Feedback Visual**: Indicadores de progresso e estado

## 🚀 Instalação

### Pré-requisitos
- Node.js 18+
- npm ou yarn

### Comandos
```bash
# Instalar dependências
npm install

# Desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview da build
npm run preview
```

## ⚙️ Configuração

### API URL
Arquivo: `src/services/api.js`
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

### Variáveis de Ambiente
Criar arquivo `.env.local`:
```env
VITE_API_URL=http://localhost:5000/api
```

## 🔍 Debug e Logs

### Console do Navegador
O sistema gera logs detalhados:
```javascript
🔍 [DEBUG] HANDLE_AI_ANALYSIS_STARTED
🔍 [DEBUG] STEP_LOCK_ACTIVATED
🔍 [DEBUG] AI_SIMULATION_SUCCESS
🔍 [DEBUG] STEP_LOCK_DEACTIVATED
```

### Tipos de Log
- **CURRENT_STEP_CHANGE**: Mudanças de etapa
- **STEP_LOCK_ACTIVATED/DEACTIVATED**: Sistema de lock
- **AI_ANALYSIS_***: Processamento da IA
- **USEEFFECT_***: Execução de efeitos

## 🎯 Componentes Principais

### App.jsx
Componente principal com:
- Gerenciamento de estado global
- Sistema de navegação entre etapas
- Integração com API
- Controle de autenticação

### CreateProjectModal.jsx
Modal para criação/edição de projetos:
- Formulário completo
- Validação de campos
- Integração com API

### AuthPage.jsx
Página de autenticação:
- Login de usuários
- Interface responsiva
- Redirecionamento automático

## 🔧 Desenvolvimento

### Adicionar Nova Etapa
1. Atualizar array `projectSteps`
2. Implementar renderização em `renderStepContent`
3. Adicionar lógica específica se necessário

### Adicionar Novo Componente
1. Criar arquivo em `src/components/`
2. Importar no componente pai
3. Seguir padrões de estilização existentes

### Integrar Nova API
1. Adicionar método em `src/services/api.js`
2. Implementar tratamento de erro
3. Atualizar estado conforme necessário

## 🚨 Solução de Problemas

### Build Falha
```bash
# Limpar cache
rm -rf node_modules .vite
npm install
```

### Erro de CORS
- Verificar se backend está rodando
- Confirmar URL da API
- Verificar configuração do backend

### Componente não Renderiza
- Verificar imports
- Verificar console para erros
- Verificar estrutura de props

## 📱 Responsividade

O sistema é totalmente responsivo:
- **Desktop**: Layout completo com sidebar
- **Tablet**: Layout adaptado
- **Mobile**: Interface otimizada para touch

## 🎨 Customização

### Cores
Arquivo: `tailwind.config.js`
```javascript
theme: {
  extend: {
    colors: {
      apollo: {
        orange: '#ff6b35',
        // adicionar mais cores
      }
    }
  }
}
```

### Componentes
Todos os componentes seguem o padrão shadcn/ui e podem ser customizados facilmente.

---

**Interface moderna e robusta para gestão inteligente de projetos** 🚀

