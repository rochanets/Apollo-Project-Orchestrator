# Dockerfile para produção do Apollo Project Orchestrator Backend
FROM python:3.11-slim

# Metadata
LABEL maintainer="Apollo Team <admin@apollo.com>"
LABEL version="1.0.0"
LABEL description="Apollo Project Orchestrator Backend - Production"

# Argumentos de build
ARG APP_ENV=production
ARG WORKERS=4

# Configurar variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=${APP_ENV} \
    WORKERS=${WORKERS} \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    curl \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Criar usuário não-root para segurança
RUN groupadd -r apollo && useradd -r -g apollo apollo

# Configurar diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências Python primeiro (para cache de layers)
COPY requirements/ requirements/
RUN pip install --upgrade pip && \
    pip install -r requirements/prod.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p logs uploads instance static && \
    chown -R apollo:apollo /app

# Copiar scripts de inicialização
COPY docker/entrypoint.sh /entrypoint.sh
COPY docker/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /entrypoint.sh /wait-for-it.sh

# Mudar para usuário não-root
USER apollo

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Expor porta
EXPOSE 5000

# Ponto de entrada
ENTRYPOINT ["/entrypoint.sh"]

# Comando padrão
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--keep-alive", "2", "src.app:create_app()"]