"""
Application Factory para o Apollo Project Orchestrator - CORRIGIDO
"""

import os
import sys
import logging
from pathlib import Path
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

# Adicionar o diretório pai ao Python path para importações absolutas
if __name__ == '__main__':
    current_dir = Path(__file__).parent
    backend_dir = current_dir.parent
    sys.path.insert(0, str(backend_dir))

try:
    # Tentar importação relativa (quando usado como módulo)
    from .config import get_config
    from .extensions import db, migrate, jwt, cors, cache, limiter, mail
except ImportError:
    # Fallback para importação absoluta (quando executado diretamente)
    from config import get_config
    from extensions import db, migrate, jwt, cors, cache, limiter, mail


def create_app(config_name=None):
    """
    Factory para criar a aplicação Flask
    
    Args:
        config_name (str): Nome da configuração ('development', 'testing', 'production')
    
    Returns:
        Flask: Instância da aplicação configurada
    """
    
    app = Flask(__name__)
    
    # =============================================================================
    # CONFIGURAÇÃO
    # =============================================================================
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Inicializar configurações específicas
    config_class.init_app(app)
    
    # =============================================================================
    # INICIALIZAR EXTENSÕES
    # =============================================================================
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    cache.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)
    
    # =============================================================================
    # REGISTRAR BLUEPRINTS
    # =============================================================================
    
    register_blueprints(app)
    
    # =============================================================================
    # HANDLERS DE ERRO
    # =============================================================================
    
    register_error_handlers(app)
    
    # =============================================================================
    # COMANDOS CLI
    # =============================================================================
    
    register_commands(app)
    
    # =============================================================================
    # HOOKS DE REQUEST
    # =============================================================================
    
    register_hooks(app)
    
    return app


def register_blueprints(app):
    """Registrar todos os blueprints da aplicação"""
    
    try:
        # Tentar importação relativa primeiro
        from .routes.auth import auth_bp
        from .routes.projects import projects_bp
        from .routes.users import users_bp
        from .routes.ai import ai_bp
    except ImportError:
        # Fallback para importação absoluta
        from routes.auth import auth_bp
        from routes.projects import projects_bp
        from routes.users import users_bp
        from routes.ai import ai_bp
    
    # Registrar blueprints com prefixos
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    
    # Rota raiz para health check
    @app.route('/api/health')
    def api_health_check():
        return jsonify({
            'status': 'ok',
            'message': 'API está funcionando!',
            'version': app.config.get('APP_VERSION', '1.0.0'),
            'environment': os.environ.get('FLASK_ENV', 'development')
        })
    
    # Rota para informações da API
    @app.route('/api')
    def api_info():
        return jsonify({
            'name': app.config['APP_NAME'],
            'version': app.config['APP_VERSION'],
            'api_version': app.config['API_VERSION'],
            'endpoints': {
                'auth': '/api/auth',
                'projects': '/api/projects',
                'users': '/api/users',
                'ai': '/api/ai'
            },
            'docs': '/api/docs'
        })


def register_error_handlers(app):
    """Registrar handlers para tratamento de erros"""
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handler para exceções HTTP"""
        return jsonify({
            'error': e.name,
            'message': e.description,
            'status_code': e.code
        }), e.code
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': 'Requisição malformada'
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Credenciais inválidas ou token expirado'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': 'Acesso negado'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'Recurso não encontrado'
        }), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({
            'error': 'Too Many Requests',
            'message': 'Limite de requisições excedido. Tente novamente mais tarde.'
        }), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Erro interno do servidor: {error}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Erro interno do servidor'
        }), 500


def register_commands(app):
    """Registrar comandos CLI customizados"""
    
    @app.cli.command()
    def init_db():
        """Inicializar o banco de dados"""
        db.create_all()
        print("Banco de dados inicializado!")
    
    @app.cli.command()
    def create_admin():
        """Criar usuário administrador"""
        try:
            from .models.database import User
        except ImportError:
            from models.database import User
        from werkzeug.security import generate_password_hash
        
        email = input("Email do administrador: ")
        name = input("Nome do administrador: ")
        password = input("Senha do administrador: ")
        
        if User.query.filter_by(email=email).first():
            print("Usuário já existe!")
            return
        
        admin = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            user_level='admin',
            email_verified=True,
            is_active=True
        )
        
        db.session.add(admin)
        db.session.commit()
        print(f"Administrador {name} criado com sucesso!")
    
    @app.cli.command()
    def seed_data():
        """Popular banco com dados de exemplo"""
        try:
            try:
                from .utils.seed import seed_database
            except ImportError:
                from utils.seed import seed_database
            seed_database()
            print("Dados de exemplo criados!")
        except ImportError:
            print("⚠️  Módulo utils.seed não encontrado. Comando não disponível.")


def register_hooks(app):
    """Registrar hooks de request/response"""
    
    @app.before_request
    def before_request():
        """Executado antes de cada requisição"""
        pass
    
    @app.after_request
    def after_request(response):
        """Executado após cada requisição"""
        # Adicionar headers de segurança
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        return response
    
    @app.teardown_appcontext
    def teardown_db(error):
        """Limpar recursos após cada requisição"""
        if error:
            db.session.rollback()
        db.session.remove()


# Proteção para execução direta
if __name__ == '__main__':
    print("⚠️  AVISO: app.py não deve ser executado diretamente!")
    print("📝 Use o main.py para iniciar o servidor:")
    print("   python main.py")
    print("   ou")
    print("   python -m src.main")
    sys.exit(1)