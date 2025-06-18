from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models.database import db
from src.routes.auth import auth_bp
import os

# Configurar ambiente
os.environ["FLASK_ENV"] = "development"

# Inicializar app
app = Flask(__name__)

# Caminho do banco
basedir = os.path.abspath(os.path.dirname(__file__))  # src/
db_path = os.path.abspath(os.path.join(basedir, '..', 'apollo.db'))  # backend/apollo.db
print("FLASK ESTÁ USANDO O BANCO:", db_path)

# Configurações do Flask
app.config.update({
    'DEBUG': True,
    'ENV': 'development',
    'SQLALCHEMY_DATABASE_URI': f"sqlite:///{db_path}",
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'JWT_SECRET_KEY': 'sua-chave-jwt-segura'
})

# Inicializar extensões
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Registrar rotas
app.register_blueprint(auth_bp, url_prefix='/api/auth')

@app.route('/')
def index():
    return 'Apollo API está no ar!'

if __name__ == '__main__':
    app.run(debug=True)
