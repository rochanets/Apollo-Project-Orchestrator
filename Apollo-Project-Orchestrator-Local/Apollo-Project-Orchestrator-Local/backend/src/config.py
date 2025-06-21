import os
from datetime import timedelta
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Configuração base para todas as outras configurações"""
    
    # =============================================================================
    # CONFIGURAÇÕES BÁSICAS
    # =============================================================================
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # =============================================================================
    # BANCO DE DADOS
    # =============================================================================
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 0
    }
    
    # =============================================================================
    # JWT CONFIGURAÇÕES
    # =============================================================================
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 30))
    )
    JWT_ALGORITHM = 'HS256'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    # =============================================================================
    # OPENAI CONFIGURAÇÕES
    # =============================================================================
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-3.5-turbo'
    OPENAI_MAX_TOKENS = 2000
    OPENAI_TEMPERATURE = 0.7
    AI_FALLBACK_ENABLED = True
    
    # =============================================================================
    # CORS E SEGURANÇA
    # =============================================================================
    CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000', 'http://localhost:5174']
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    CORS_EXPOSE_HEADERS = ['Authorization']
    
    # =============================================================================
    # UPLOAD CONFIGURAÇÕES
    # =============================================================================
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16)) * 1024 * 1024  # MB para bytes
    UPLOAD_FOLDER = os.path.join(BASE_DIR, os.environ.get('UPLOAD_FOLDER', 'uploads'))
    ALLOWED_EXTENSIONS = {
        'documents': {'txt', 'pdf', 'doc', 'docx', 'rtf'},
        'images': {'png', 'jpg', 'jpeg', 'gif', 'bmp'},
        'data': {'csv', 'xlsx', 'xls', 'json'},
        'archives': {'zip', 'rar', '7z'}
    }
    
    # =============================================================================
    # CACHE CONFIGURAÇÕES
    # =============================================================================
    CACHE_TYPE = 'redis' if os.environ.get('REDIS_URL') else 'simple'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # =============================================================================
    # RATE LIMITING
    # =============================================================================
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'redis://localhost:6379/1')
    RATELIMIT_DEFAULT = "100 per hour"
    
    # =============================================================================
    # EMAIL CONFIGURAÇÕES
    # =============================================================================
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@apollo.com')
    
    # =============================================================================
    # LOGS CONFIGURAÇÕES
    # =============================================================================
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/apollo.log')
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # =============================================================================
    # CONFIGURAÇÕES DE APLICAÇÃO
    # =============================================================================
    APP_NAME = 'Apollo Project Orchestrator'
    APP_VERSION = '1.0.0'
    API_VERSION = 'v1'
    
    @staticmethod
    def init_app(app):
        """Inicialização específica da configuração"""
        pass


class DevelopmentConfig(Config):
    """Configuração para ambiente de desenvolvimento"""
    
    DEBUG = True
    TESTING = False
    
    # Banco SQLite para desenvolvimento
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(BASE_DIR, "apollo.db")}'
    
    # Logs mais verbosos em desenvolvimento
    LOG_LEVEL = 'DEBUG'
    
    # Cache simples em desenvolvimento
    CACHE_TYPE = 'simple'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Configurar logs para desenvolvimento
        import logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )


class TestingConfig(Config):
    """Configuração para testes"""
    
    TESTING = True
    DEBUG = True
    
    # Banco em memória para testes
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Desabilitar proteções em testes
    WTF_CSRF_ENABLED = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=2)
    
    # Cache simples para testes
    CACHE_TYPE = 'simple'
    
    # Desabilitar rate limiting em testes
    RATELIMIT_ENABLED = False


class ProductionConfig(Config):
    """Configuração para produção"""
    
    DEBUG = False
    TESTING = False
    
    # Banco PostgreSQL para produção
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://apollo:password@localhost/apollo_production'
    
    # Configurações otimizadas para produção
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_timeout': 20,
        'max_overflow': 10,
        'pool_size': 10
    }
    
    # SSL para PostgreSQL
    if os.environ.get('DATABASE_URL') and 'postgresql' in os.environ.get('DATABASE_URL'):
        SQLALCHEMY_ENGINE_OPTIONS['connect_args'] = {"sslmode": "require"}
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Configurar logs para produção
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Criar diretório de logs se não existir
        log_dir = os.path.dirname(Config.LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configurar handler rotativo
        file_handler = RotatingFileHandler(
            Config.LOG_FILE,
            maxBytes=Config.LOG_MAX_BYTES,
            backupCount=Config.LOG_BACKUP_COUNT
        )
        
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info(f'{Config.APP_NAME} startup')


class DockerConfig(ProductionConfig):
    """Configuração específica para containers Docker"""
    
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        
        # Log para stdout em containers
        import logging
        import sys
        
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
        ))
        app.logger.addHandler(stream_handler)


# Mapeamento de configurações
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Retorna a configuração baseada na variável de ambiente FLASK_ENV"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])