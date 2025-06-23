"""
Extensões do Flask - Inicializadas separadamente para evitar imports circulares
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail

# =============================================================================
# INICIALIZAÇÃO DAS EXTENSÕES
# =============================================================================

# Banco de dados
db = SQLAlchemy()

# Migrações
migrate = Migrate()

# JWT para autenticação
jwt = JWTManager()

# CORS para requisições cross-origin
cors = CORS(
    supports_credentials=True,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000", "http://localhost:5174"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }
    }
)

# Cache para performance
cache = Cache()

# Rate limiting para segurança
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Email
mail = Mail()

# =============================================================================
# CONFIGURAÇÕES JWT
# =============================================================================

# Set para armazenar tokens na blacklist
blacklisted_tokens = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """Verificar se o token está na blacklist"""
    return jwt_payload['jti'] in blacklisted_tokens

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Callback para token expirado"""
    return {
        'message': 'Token expirado',
        'error': 'token_expired'
    }, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Callback para token inválido"""
    return {
        'message': 'Token inválido',
        'error': 'invalid_token'
    }, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    """Callback para token ausente"""
    return {
        'message': 'Token de acesso necessário',
        'error': 'authorization_required'
    }, 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    """Callback para token não-fresh"""
    return {
        'message': 'Token fresh necessário',
        'error': 'fresh_token_required'
    }, 401

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """Callback para token revogado"""
    return {
        'message': 'Token foi revogado',
        'error': 'token_revoked'
    }, 401