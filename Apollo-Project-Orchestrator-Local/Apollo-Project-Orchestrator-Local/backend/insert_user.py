from src.models.database import db, User
from src.main import app
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    existing_user = User.query.filter_by(email='hfnetto@stefanini.com').first()
    if not existing_user:
        user = User(
            name='hfnetto',
            email='hfnetto@stefanini.com',
            password_hash=generate_password_hash('teste123'),
            company='Stefanini',
            role='Admin',
            user_level='Senior',
            email_verified=True
        )
        db.session.add(user)
        db.session.commit()
        print('Usuário criado com sucesso')
    else:
        print('Usuário já existe')
