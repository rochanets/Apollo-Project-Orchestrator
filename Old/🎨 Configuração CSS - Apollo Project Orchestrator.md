# 🎨 Configuração CSS - Apollo Project Orchestrator

## ⚠️ **IMPORTANTE - Configuração CSS Necessária**

Se a interface não está aparecendo corretamente, você precisa instalar e configurar o CSS. Siga os passos abaixo:

## 🚀 **Instalação Rápida do CSS**

### 1️⃣ **Instalar Dependências CSS**
```bash
cd frontend
npm install
```

### 2️⃣ **Verificar Arquivos CSS**
Certifique-se de que estes arquivos existem:

- ✅ `src/index.css` - CSS principal com Tailwind
- ✅ `src/App.css` - Estilos do componente principal  
- ✅ `tailwind.config.js` - Configuração do Tailwind
- ✅ `components.json` - Configuração do Shadcn/UI

### 3️⃣ **Reiniciar o Servidor**
```bash
# Parar o servidor (Ctrl+C)
# Depois reiniciar:
npm run dev
```

## 📁 **Arquivos CSS Incluídos**

### 🎨 **src/index.css**
- Configuração completa do Tailwind CSS
- Variáveis CSS customizadas para tema Apollo
- Estilos para modo claro e escuro
- Classes utilitárias personalizadas
- Animações e transições

### ⚙️ **tailwind.config.js**
- Configuração do Tailwind CSS
- Cores personalizadas do Apollo
- Animações customizadas
- Sombras e efeitos especiais
- Responsividade

### 🧩 **components.json**
- Configuração do Shadcn/UI
- Aliases para imports
- Estilo "new-york"
- Integração com Tailwind

## 🎯 **Cores do Tema Apollo**

### 🟠 **Cores Principais**
- **Apollo Orange**: `#FF6B35`
- **Apollo Orange Light**: `#FFA500`
- **Apollo Orange Dark**: `#E55A2B`

### 🌓 **Modo Claro/Escuro**
- **Fundo Claro**: `#FFFFFF`
- **Fundo Escuro**: `#1A1A1A`
- **Texto Claro**: `#1A1A1A`
- **Texto Escuro**: `#F0F0F0`

## 🔧 **Solução de Problemas CSS**

### ❌ **Interface sem estilo**
```bash
# 1. Verificar se Tailwind está instalado
npm list tailwindcss

# 2. Reinstalar dependências
rm -rf node_modules package-lock.json
npm install

# 3. Verificar se arquivos CSS existem
ls -la src/index.css
ls -la tailwind.config.js
```

### ❌ **Componentes não aparecem**
```bash
# Verificar se Shadcn/UI está instalado
npm list @radix-ui/react-tabs
npm list lucide-react

# Se não estiver, instalar:
npm install @radix-ui/react-tabs lucide-react
```

### ❌ **Erro de import**
Verifique se o arquivo `src/main.jsx` importa o CSS:
```jsx
import './index.css'  // Esta linha deve existir
```

## 📱 **Classes CSS Úteis**

### 🎨 **Botões**
```css
.btn-primary     /* Botão principal laranja */
.btn-secondary   /* Botão secundário */
```

### 📦 **Cards**
```css
.card           /* Card básico */
.card-header    /* Cabeçalho do card */
.card-content   /* Conteúdo do card */
```

### 🚨 **Alertas**
```css
.alert-success  /* Alerta de sucesso */
.alert-error    /* Alerta de erro */
.alert-warning  /* Alerta de aviso */
```

### ✨ **Animações**
```css
.animate-fade-in    /* Fade in suave */
.apollo-gradient    /* Gradiente Apollo */
.apollo-shadow      /* Sombra Apollo */
```

## 🎭 **Componentes Shadcn/UI Disponíveis**

- ✅ Button, Card, Input, Label
- ✅ Tabs, Alert, Dialog, Popover
- ✅ Select, Checkbox, Switch
- ✅ Progress, Skeleton, Tooltip
- ✅ E muito mais...

## 🔄 **Atualização do CSS**

Se você fizer alterações no CSS:

1. **Salvar arquivos**
2. **Vite recarrega automaticamente**
3. **Verificar no navegador**

## 📞 **Suporte CSS**

Se ainda houver problemas:

1. **Verificar console do navegador** (F12)
2. **Verificar se há erros de CSS**
3. **Confirmar que Tailwind está carregando**
4. **Verificar se variáveis CSS estão definidas**

---

**Com estes arquivos, a interface Apollo deve aparecer perfeitamente estilizada!** 🎨✨

