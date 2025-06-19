#!/usr/bin/env python3
"""
Script para corrigir problemas do Apollo Project Orchestrator
"""

import os
import sys
import sqlite3
import shutil
from datetime import datetime

def backup_database():
    """Criar backup do banco"""
    db_path = "apollo.db"
    if os.path.exists(db_path):
        backup_path = f"apollo_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(db_path, backup_path)
        print(f"📦 Backup criado: {backup_path}")
        return backup_path
    return None

def fix_database_schema():
    """Corrigir estrutura do banco de dados"""
    db_path = "apollo.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Verificando estrutura da tabela projects...")
        
        # Verificar colunas existentes
        cursor.execute("PRAGMA table_info(projects)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        print(f"Colunas existentes: {existing_columns}")
        
        # Colunas que devem existir
        required_columns = [
            ("start_date", "DATETIME"),
            ("end_date", "DATETIME"), 
            ("estimated_hours", "INTEGER"),
            ("actual_hours", "INTEGER", "0"),
            ("completion_percentage", "INTEGER", "0")
        ]
        
        # Adicionar colunas faltantes
        for column_info in required_columns:
            column_name = column_info[0]
            column_type = column_info[1]
            default_value = column_info[2] if len(column_info) > 2 else None
            
            if column_name not in existing_columns:
                if default_value:
                    sql = f"ALTER TABLE projects ADD COLUMN {column_name} {column_type} DEFAULT {default_value}"
                else:
                    sql = f"ALTER TABLE projects ADD COLUMN {column_name} {column_type}"
                
                print(f"➕ Adicionando coluna: {column_name}")
                cursor.execute(sql)
            else:
                print(f"✅ Coluna já existe: {column_name}")
        
        conn.commit()
        
        # Verificar novamente
        cursor.execute("PRAGMA table_info(projects)")
        new_columns = [row[1] for row in cursor.fetchall()]
        print(f"Colunas após correção: {new_columns}")
        
        conn.close()
        print("✅ Estrutura do banco corrigida!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir banco: {e}")
        if 'conn' in locals():
            conn.close()
        return False

def fix_app_structure():
    """Verificar e sugerir correções na estrutura da aplicação"""
    
    print("\n🔍 Verificando estrutura da aplicação...")
    
    # Verificar se admin blueprint existe (problema detectado)
    admin_route_path = "src/routes/admin.py"
    if not os.path.exists(admin_route_path):
        print("⚠️ Arquivo admin.py não encontrado, mas referenciado no app.py")
        
        # Criar arquivo admin.py básico
        admin_content = '''"""
Blueprint de administração do Apollo Project Orchestrator
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.database import User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/health', methods=['GET'])
@jwt_required()
def admin_health():
    """Health check do admin"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    return jsonify({
        'status': 'ok',
        'message': 'Admin panel funcionando',
        'user': user.name
    }), 200

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def list_all_users():
    """Listar todos os usuários (apenas admin)"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    
    users = User.query.all()
    return jsonify({
        'users': [u.to_dict() for u in users]
    }), 200
'''
        
        with open(admin_route_path, 'w', encoding='utf-8') as f:
            f.write(admin_content)
        print(f"✅ Criado arquivo {admin_route_path}")
    
    # Verificar imports problemáticos
    print("✅ Estrutura da aplicação verificada!")

def main():
    """Função principal"""
    print("🚀 Apollo Project Orchestrator - Correção de Problemas")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("src/app.py"):
        print("❌ Execute este script no diretório backend do projeto!")
        return False
    
    # 1. Fazer backup
    backup_path = backup_database()
    
    # 2. Corrigir estrutura da aplicação
    fix_app_structure()
    
    # 3. Corrigir banco de dados
    if fix_database_schema():
        print("\n🎉 Correções aplicadas com sucesso!")
        print("\nPróximos passos:")
        print("1. Substitua o conteúdo do arquivo src/app.py pelo código corrigido")
        print("2. Execute: python src/main.py")
        print("3. Ou tente novamente: flask db migrate")
        return True
    else:
        print("\n❌ Falha nas correções!")
        if backup_path:
            print(f"Restaure o backup se necessário: {backup_path}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
