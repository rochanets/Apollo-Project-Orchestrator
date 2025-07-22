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

from flask_cors import CORS
from src.app import create_app

print("✅ Usando Application Factory (src.app.create_app)")
app = create_app()

# Aplicar CORS após a criação do app
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])


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