from src.models.database import db
from src.main import app

# IMPORTA EXPLICITAMENTE OS MODELOS
from src.models.database import User, Project, ProjectPermission, ProjectStep, AuditLog

import os
print("CAMINHO ABSOLUTO DO BANCO:", os.path.abspath("apollo.db"))

with app.app_context():
    db.create_all()
    print("Banco de dados criado com sucesso!")
