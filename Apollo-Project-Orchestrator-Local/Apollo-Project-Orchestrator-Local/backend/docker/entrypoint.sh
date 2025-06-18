#!/bin/bash

set -e

echo "🚀 Apollo Project Orchestrator - Starting Backend..."

# Aguardar serviços necessários
echo "⏳ Waiting for database..."
/wait-for-it.sh postgres:5432 --timeout=60 --strict -- echo "✅ Database is ready!"

echo "⏳ Waiting for Redis..."
/wait-for-it.sh redis:6379 --timeout=30 --strict -- echo "✅ Redis is ready!"

# Executar migrações do banco
echo "🔄 Running database migrations..."
flask db upgrade || echo "⚠️ Migration failed or no migrations to run"

# Criar usuário admin se não existir
echo "👤 Creating admin user if not exists..."
python -c "
from src.app import create_app
from src.extensions import db
from src.models.database import User
from werkzeug.security import generate_password_hash
import os

app = create_app()
with app.app_context():
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@apollo.com')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(
            name='Administrator',
            email=admin_email,
            password_hash=generate_password_hash(admin_password),
            user_level='admin',
            email_verified=True,
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f'✅ Admin user created: {admin_email}')
    else:
        print(f'ℹ️ Admin user already exists: {admin_email}')
" || echo "⚠️ Admin user creation failed"

echo "🎯 Starting application..."

# Executar comando passado como argumento
exec "$@"