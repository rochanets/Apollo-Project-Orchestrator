#!/usr/bin/env python3
"""
Script para corrigir o banco de dados do Apollo Project Orchestrator
Adiciona as colunas faltantes na tabela projects
"""

import sqlite3
import os
from datetime import datetime

def fix_database():
    """Corrigir estrutura do banco de dados"""
    
    db_path = "apollo.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Verificando estrutura atual da tabela projects...")
        
        # Verificar colunas existentes
        cursor.execute("PRAGMA table_info(projects)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        print(f"Colunas existentes: {existing_columns}")
        
        # Colunas que devem existir
        required_columns = [
            ("start_date", "DATETIME"),
            ("end_date", "DATETIME"), 
            ("estimated_hours", "INTEGER"),
            ("actual_hours", "INTEGER DEFAULT 0"),
            ("completion_percentage", "INTEGER DEFAULT 0")
        ]
        
        # Adicionar colunas faltantes
        for column_name, column_type in required_columns:
            if column_name not in existing_columns:
                print(f"➕ Adicionando coluna: {column_name}")
                cursor.execute(f"ALTER TABLE projects ADD COLUMN {column_name} {column_type}")
            else:
                print(f"✅ Coluna já existe: {column_name}")
        
        conn.commit()
        print("✅ Banco de dados corrigido com sucesso!")
        
        # Verificar novamente
        cursor.execute("PRAGMA table_info(projects)")
        new_columns = [row[1] for row in cursor.fetchall()]
        print(f"Colunas após correção: {new_columns}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir banco: {e}")
        return False

def create_backup():
    """Criar backup do banco antes da correção"""
    db_path = "apollo.db"
    if os.path.exists(db_path):
        backup_path = f"apollo_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"📦 Backup criado: {backup_path}")

if __name__ == "__main__":
    print("🚀 Apollo Project Orchestrator - Database Fix")
    print("=" * 50)
    
    # Criar backup
    create_backup()
    
    # Corrigir banco
    if fix_database():
        print("\n🎉 Correção concluída! Tente executar o projeto novamente.")
    else:
        print("\n❌ Falha na correção. Verifique os logs de erro.")
