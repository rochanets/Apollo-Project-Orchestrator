"""
Apollo Project Orchestrator - Seed Database
Utilitário para popular o banco de dados com dados de exemplo
"""

from datetime import datetime
from werkzeug.security import generate_password_hash
from ..extensions import db
from ..models.database import User, Project, ProjectStep


def seed_database():
    """
    Popular o banco de dados com dados de exemplo
    """
    try:
        print("🌱 Iniciando seed do banco de dados...")
        
        # Criar usuários de exemplo
        seed_users()
        
        # Criar projetos de exemplo
        seed_projects()
        
        print("✅ Seed do banco de dados concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro durante o seed: {e}")
        db.session.rollback()
        raise


def seed_users():
    """Criar usuários de exemplo"""
    
    # Verificar se já existem usuários
    if User.query.count() > 0:
        print("👥 Usuários já existem no banco. Pulando criação...")
        return
    
    users_data = [
        {
            'name': 'Administrador Apollo',
            'email': 'admin@apollo.com',
            'password': 'admin123',
            'user_level': 'admin',
            'company': 'Apollo Systems',
            'role': 'System Administrator'
        },
        {
            'name': 'João Silva',
            'email': 'joao@apollo.com',
            'password': 'user123',
            'user_level': 'user',
            'company': 'Apollo Systems',
            'role': 'Project Manager'
        },
        {
            'name': 'Maria Santos',
            'email': 'maria@apollo.com',
            'password': 'user123',
            'user_level': 'user',
            'company': 'Apollo Systems',
            'role': 'Developer'
        }
    ]
    
    for user_data in users_data:
        user = User(
            name=user_data['name'],
            email=user_data['email'],
            password_hash=generate_password_hash(user_data['password']),
            user_level=user_data['user_level'],
            company=user_data['company'],
            role=user_data['role'],
            email_verified=True,
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        db.session.add(user)
        print(f"👤 Usuário criado: {user_data['name']} ({user_data['email']})")
    
    db.session.commit()


def seed_projects():
    """Criar projetos de exemplo"""
    
    # Verificar se já existem projetos
    if Project.query.count() > 0:
        print("📁 Projetos já existem no banco. Pulando criação...")
        return
    
    # Buscar usuário admin para ser o owner
    admin_user = User.query.filter_by(user_level='admin').first()
    if not admin_user:
        print("⚠️  Usuário admin não encontrado. Não é possível criar projetos.")
        return
    
    projects_data = [
        {
            'name': 'Sistema de E-commerce',
            'description': 'Desenvolvimento de plataforma completa de e-commerce com integração de pagamentos e gestão de estoque.',
            'status': 'active',
            'priority': 'high'
        },
        {
            'name': 'App Mobile Corporativo',
            'description': 'Aplicativo mobile para gestão interna da empresa com funcionalidades de comunicação e produtividade.',
            'status': 'planning',
            'priority': 'medium'
        },
        {
            'name': 'Migração de Infraestrutura',
            'description': 'Migração completa da infraestrutura atual para cloud computing com foco em escalabilidade.',
            'status': 'active',
            'priority': 'high'
        }
    ]
    
    for project_data in projects_data:
        project = Project(
            name=project_data['name'],
            description=project_data['description'],
            status=project_data['status'],
            priority=project_data['priority'],
            owner_id=admin_user.id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(project)
        print(f"📁 Projeto criado: {project_data['name']}")
    
    db.session.commit()


def clear_database():
    """
    Limpar todos os dados do banco (CUIDADO: remove tudo!)
    """
    try:
        print("🗑️  Limpando banco de dados...")
        
        # Ordem importante devido às foreign keys
        ProjectStep.query.delete()
        Project.query.delete()
        User.query.delete()
        
        db.session.commit()
        print("✅ Banco de dados limpo com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao limpar banco: {e}")
        db.session.rollback()
        raise