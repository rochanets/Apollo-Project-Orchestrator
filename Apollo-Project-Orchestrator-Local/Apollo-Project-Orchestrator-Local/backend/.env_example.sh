# Apollo Project Orchestrator - Environment Variables
# Copie este arquivo para .env e configure as variáveis com seus valores reais

# =============================================================================
# CONFIGURAÇÕES BÁSICAS
# =============================================================================

# Ambiente de execução (development, testing, production)
FLASK_ENV=development

# Chave secreta para JWT e sessões (GERE UMA NOVA!)
# Use: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-secret-key-here-generate-a-new-one

# =============================================================================
# BANCO DE DADOS
# =============================================================================

# Para desenvolvimento (SQLite)
DATABASE_URL=sqlite:///apollo.db

# Para produção (PostgreSQL recomendado)
# DATABASE_URL=postgresql://username:password@localhost:5432/apollo_db

# =============================================================================
# APIs EXTERNAS
# =============================================================================

# OpenAI API Key - Obtenha em https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-openai-api-key-here

# =============================================================================
# CONFIGURAÇÕES JWT
# =============================================================================

# Tempo de expiração do token de acesso (em minutos)
JWT_ACCESS_TOKEN_EXPIRES=60

# Tempo de expiração do token de refresh (em dias)
JWT_REFRESH_TOKEN_EXPIRES=30

# =============================================================================
# CONFIGURAÇÕES DE EMAIL (OPCIONAL)
# =============================================================================

# Para envio de emails de verificação/notificações
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# =============================================================================
# REDIS (OPCIONAL - Para cache e sessions)
# =============================================================================

REDIS_URL=redis://localhost:6379/0

# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA
# =============================================================================

# Rate limiting
RATELIMIT_STORAGE_URL=redis://localhost:6379/1

# Domínios permitidos para CORS (separados por vírgula)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# =============================================================================
# CONFIGURAÇÕES DE UPLOAD
# =============================================================================

# Tamanho máximo de upload (em MB)
MAX_CONTENT_LENGTH=16

# Diretório de uploads
UPLOAD_FOLDER=uploads

# =============================================================================
# LOGS
# =============================================================================

# Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Arquivo de log
LOG_FILE=logs/apollo.log

# =============================================================================
# CONFIGURAÇÕES DE PRODUÇÃO
# =============================================================================

# Número de workers para Gunicorn
WORKERS=4

# Host e porta para produção
HOST=0.0.0.0
PORT=5000