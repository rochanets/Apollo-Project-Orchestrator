from src.models.database import db
from src.main import app

with app.app_context():
    import os
print("CAMINHO ABSOLUTO DO BANCO:", os.path.abspath("apollo.db"))
db.create_all()
print("Banco de dados criado com sucesso!")