"""
Apollo Project Orchestrator - Arquivo Principal
Arquivo de entrada principal do sistema Apollo Project Orchestrator
"""

import os
import sys
from pathlib import Path

print(f"DEBUG: Este arquivo main.py está em: {os.path.abspath(__file__)}")

# Adicionar o diretório raiz ao Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Configurar variáveis de ambiente
os.environ.setdefault('FLASK_ENV', 'development')

try:
    # Tentar usar o Application Factory se disponível
    from src.app import create_app
    from flask_cors import CORS

    print("✅ Usando Application Factory (src.app.create_app)")
    app = create_app()

    # Adicione o CORS aqui para garantir que será aplicado no app criado pela factory
    CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

except ImportError:
    # Fallback para estrutura simples se app.py não existir
    print("⚠️  Application Factory não encontrado, usando estrutura simples")

    from flask import Flask, jsonify
    from flask_cors import CORS
    from src.extensions import db

    app = Flask(__name__)
    app.config['CORS_ORIGINS'] = ['http://localhost:5173', 'http://localhost:3000']
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # Configurações básicas
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'apollo-dev-secret-key-2025')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///apollo.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensões
    db.init_app(app)

    # Registrar blueprints se disponíveis
    try:
        from src.routes.ai import ai_bp
        app.register_blueprint(ai_bp, url_prefix='/api/ai')
        print("✅ Blueprint AI registrado")
    except ImportError as e:
        print(f"⚠️  Blueprint AI não disponível: {e}")

    try:
        from src.routes.projects import projects_bp
        app.register_blueprint(projects_bp, url_prefix='/api/projects')
        print("✅ Blueprint Projects registrado")
    except ImportError as e:
        print(f"⚠️  Blueprint Projects não disponível: {e}")

    try:
        from src.routes.users import users_bp
        app.register_blueprint(users_bp, url_prefix='/api/users')
        print("✅ Blueprint Users registrado")
    except ImportError as e:
        print(f"⚠️  Blueprint Users não disponível: {e}")

    try:
        from src.routes.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        print("✅ Blueprint Auth registrado")
    except ImportError as e:
        print(f"⚠️  Blueprint Auth não disponível: {e}")

    # Rotas básicas
    @app.route('/')
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'ok',
            'message': 'Apollo Project Orchestrator está funcionando!',
            'version': '1.0.0',
            'environment': os.environ.get('FLASK_ENV', 'development')
        })

    @app.route('/api')
    def api_info():
        return jsonify({
            'name': 'Apollo Project Orchestrator API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'health': '/',
                'api_info': '/api',
                'ai': '/api/ai',
                'projects': '/api/projects',
                'users': '/api/users',
                'auth': '/api/auth'
            }
        })

# Criar tabelas do banco de dados se necessário
def init_database():
    """Inicializar banco de dados"""
    try:
        with app.app_context():
            # Importar modelos para garantir que as tabelas sejam criadas
            try:
                from src.models.database import User, Project, ProjectStep, ProjectPermission, AuditLog
                print("✅ Modelos principais importados")

                from src.extensions import db
                db.create_all()
                print("✅ Banco de dados inicializado")

            except ImportError as e:
                print(f"⚠️  Modelos do database.py não encontrados: {e}")

    except Exception as e:
        print(f"⚠️  Erro ao inicializar banco: {e}")

if __name__ == '__main__':
    print("🚀 Iniciando Apollo Project Orchestrator...")
    print(f"📁 Diretório de trabalho: {os.getcwd()}")
    print(f"🐍 Python path: {sys.path[0]}")

    # Inicializar banco de dados
    init_database()

    # Configurações de desenvolvimento
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    print(f"🌐 Servidor iniciando em: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print("=" * 50)

    try:
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=True if debug else False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Apollo Project Orchestrator encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)