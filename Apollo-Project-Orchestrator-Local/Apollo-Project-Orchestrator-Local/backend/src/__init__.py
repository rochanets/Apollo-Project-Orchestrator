# =============================================================================
# ARQUIVO: backend/src/__init__.py
# Substitua o conteúdo atual por:
# =============================================================================

"""
Apollo Project Orchestrator - Pacote Principal
Este arquivo inicializa o pacote src e disponibiliza as principais funcionalidades
"""

__version__ = "1.0.0"
__author__ = "Apollo Team"

# Disponibilizar principais componentes
try:
    from .app import create_app
    __all__ = ['create_app']
except ImportError:
    # Se app.py não existir, disponibilizar componentes básicos
    try:
        from .extensions import db
        __all__ = ['db']
    except ImportError:
        __all__ = []

# =============================================================================
# ARQUIVO: backend/src/routes/__init__.py (CRIAR SE NÃO EXISTIR)
# =============================================================================

"""
Apollo Project Orchestrator - Rotas
Inicialização do pacote de rotas
"""

# Importar e disponibilizar blueprints
__all__ = []

try:
    from .ai import ai_bp
    __all__.append('ai_bp')
except ImportError:
    pass

try:
    from .auth import auth_bp
    __all__.append('auth_bp')
except ImportError:
    pass

try:
    from .projects import projects_bp
    __all__.append('projects_bp')
except ImportError:
    pass

try:
    from .users import users_bp
    __all__.append('users_bp')
except ImportError:
    pass

try:
    from .user import user_bp
    __all__.append('user_bp')
except ImportError:
    pass

# =============================================================================
# ARQUIVO: backend/src/models/__init__.py (CRIAR SE NÃO EXISTIR)
# =============================================================================

"""
Apollo Project Orchestrator - Modelos de Dados
Inicialização do pacote de modelos
"""

__all__ = []

try:
    from .database import User, Project, ProjectStep, ProjectPermission, AuditLog, db
    __all__.extend(['User', 'Project', 'ProjectStep', 'ProjectPermission', 'AuditLog', 'db'])
except ImportError:
    try:
        from .user import User, db
        __all__.extend(['User', 'db'])
    except ImportError:
        pass

# =============================================================================
# ARQUIVO: backend/src/services/__init__.py (CRIAR SE NÃO EXISTIR)
# =============================================================================

"""
Apollo Project Orchestrator - Serviços
Inicialização do pacote de serviços
"""

__all__ = []

try:
    from .ai import AIAnalysisService
    __all__.append('AIAnalysisService')
except ImportError:
    pass

# =============================================================================
# ARQUIVO: backend/src/utils/__init__.py (CRIAR SE NÃO EXISTIR)
# =============================================================================

"""
Apollo Project Orchestrator - Utilitários
Inicialização do pacote de utilitários
"""

__all__ = []

# Funções utilitárias podem ser adicionadas aqui conforme necessário