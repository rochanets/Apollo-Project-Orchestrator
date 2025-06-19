from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime, timedelta
import hashlib
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'apollo-secret-key-2024'

# Inicializar CORS
CORS(app)

# Arquivo do banco de dados
DB_FILE = 'apollo.db'

def get_db_connection():
    """Cria conexão com o banco de dados"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
    return conn

def init_database():
    """Inicializa o banco de dados com as tabelas necessárias"""
    conn = get_db_connection()
    
    # Criar tabela de usuários
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Criar tabela de projetos
    conn.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            client TEXT NOT NULL,
            responsible TEXT NOT NULL,
            objective TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'active',
            current_step INTEGER DEFAULT 0,
            start_date TEXT,
            deadline TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            uploaded_files TEXT DEFAULT '[]',
            ai_questions TEXT DEFAULT '[]',
            ai_analysis TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Gera hash da senha"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verifica se a senha está correta"""
    return hash_password(password) == password_hash

def generate_token(user_id):
    """Gera um token simples baseado no user_id"""
    return f"apollo_token_{user_id}_{datetime.now().timestamp()}"

def verify_token(token):
    """Verifica se o token é válido e retorna o user_id"""
    try:
        if token.startswith('apollo_token_'):
            parts = token.split('_')
            if len(parts) >= 3:
                user_id = int(parts[2])
                # Verificar se o usuário existe
                conn = get_db_connection()
                user = conn.execute('SELECT id FROM users WHERE id = ?', (user_id,)).fetchone()
                conn.close()
                return user_id if user else None
        return None
    except:
        return None

def get_current_user(request):
    """Obtém o usuário atual do token de autorização"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    user_id = verify_token(token)
    
    if user_id:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None
    return None

def dict_from_row(row):
    """Converte sqlite3.Row para dict"""
    return {key: row[key] for key in row.keys()}

# Inicializar banco de dados
init_database()

# ROTAS DE AUTENTICAÇÃO

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Nome, email e senha são obrigatórios'}), 400
        
        conn = get_db_connection()
        
        # Verificar se usuário já existe
        existing_user = conn.execute('SELECT id FROM users WHERE email = ?', (data['email'],)).fetchone()
        if existing_user:
            conn.close()
            return jsonify({'message': 'Email já cadastrado'}), 400
        
        # Criar novo usuário
        cursor = conn.execute('''
            INSERT INTO users (name, email, password_hash, created_at)
            VALUES (?, ?, ?, ?)
        ''', (data['name'], data['email'], hash_password(data['password']), datetime.now().isoformat()))
        
        user_id = cursor.lastrowid
        conn.commit()
        
        # Buscar usuário criado
        user = conn.execute('SELECT id, name, email, created_at FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        
        # Criar token
        token = generate_token(user_id)
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'user': dict_from_row(user),
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email e senha são obrigatórios'}), 400
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (data['email'],)).fetchone()
        conn.close()
        
        if not user or not verify_password(data['password'], user['password_hash']):
            return jsonify({'message': 'Email ou senha incorretos'}), 401
        
        # Criar token
        token = generate_token(user['id'])
        
        # Remover senha do retorno
        user_response = {k: v for k, v in dict_from_row(user).items() if k != 'password_hash'}
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': user_response,
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/api/auth/verify', methods=['GET'])
def verify_token_route():
    try:
        user = get_current_user(request)
        
        if not user:
            return jsonify({'message': 'Token inválido'}), 401
        
        # Remover senha do retorno
        user_response = {k: v for k, v in user.items() if k != 'password_hash'}
        
        return jsonify({
            'message': 'Token válido',
            'user': user_response
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

# ROTAS DE PROJETOS

@app.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        user = get_current_user(request)
        if not user:
            return jsonify({'message': 'Token inválido'}), 401
        
        conn = get_db_connection()
        projects = conn.execute('SELECT * FROM projects WHERE user_id = ? ORDER BY created_at DESC', (user['id'],)).fetchall()
        conn.close()
        
        # Converter para lista de dicts e processar campos JSON
        result = []
        for project in projects:
            project_dict = dict_from_row(project)
            # Converter campos JSON
            project_dict['uploaded_files'] = json.loads(project_dict['uploaded_files']) if project_dict['uploaded_files'] else []
            project_dict['ai_questions'] = json.loads(project_dict['ai_questions']) if project_dict['ai_questions'] else []
            project_dict['ai_analysis'] = json.loads(project_dict['ai_analysis']) if project_dict['ai_analysis'] else None
            result.append(project_dict)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/api/projects', methods=['POST'])
def create_project():
    try:
        user = get_current_user(request)
        if not user:
            return jsonify({'message': 'Token inválido'}), 401
            
        data = request.get_json()
        
        # Validações
        required_fields = ['name', 'client', 'responsible', 'objective']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} é obrigatório'}), 400
        
        conn = get_db_connection()
        cursor = conn.execute('''
            INSERT INTO projects (
                name, client, responsible, objective, description, priority,
                start_date, deadline, created_at, updated_at, user_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], data['client'], data['responsible'], data['objective'],
            data.get('description', ''), data.get('priority', 'medium'),
            data.get('start_date'), data.get('deadline'),
            datetime.now().isoformat(), datetime.now().isoformat(), user['id']
        ))
        
        project_id = cursor.lastrowid
        conn.commit()
        
        # Buscar projeto criado
        project = conn.execute('SELECT * FROM projects WHERE id = ?', (project_id,)).fetchone()
        conn.close()
        
        project_dict = dict_from_row(project)
        project_dict['uploaded_files'] = []
        project_dict['ai_questions'] = []
        project_dict['ai_analysis'] = None
        
        return jsonify({
            'message': 'Projeto criado com sucesso',
            'project': project_dict
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        user = get_current_user(request)
        if not user:
            return jsonify({'message': 'Token inválido'}), 401
            
        conn = get_db_connection()
        
        # Verificar se o projeto existe e pertence ao usuário
        project = conn.execute('SELECT * FROM projects WHERE id = ? AND user_id = ?', (project_id, user['id'])).fetchone()
        if not project:
            conn.close()
            return jsonify({'message': 'Projeto não encontrado'}), 404
        
        data = request.get_json()
        
        # Preparar campos para atualização
        update_fields = []
        update_values = []
        
        for field in ['name', 'client', 'responsible', 'objective', 'description', 'priority', 'current_step', 'start_date', 'deadline']:
            if field in data:
                update_fields.append(f'{field} = ?')
                update_values.append(data[field])
        
        # Campos JSON
        for field in ['uploaded_files', 'ai_questions', 'ai_analysis']:
            if field in data:
                update_fields.append(f'{field} = ?')
                update_values.append(json.dumps(data[field]) if data[field] is not None else None)
        
        # Sempre atualizar updated_at
        update_fields.append('updated_at = ?')
        update_values.append(datetime.now().isoformat())
        update_values.append(project_id)
        
        # Executar update
        conn.execute(f'UPDATE projects SET {", ".join(update_fields)} WHERE id = ?', update_values)
        conn.commit()
        
        # Buscar projeto atualizado
        updated_project = conn.execute('SELECT * FROM projects WHERE id = ?', (project_id,)).fetchone()
        conn.close()
        
        project_dict = dict_from_row(updated_project)
        # Converter campos JSON
        project_dict['uploaded_files'] = json.loads(project_dict['uploaded_files']) if project_dict['uploaded_files'] else []
        project_dict['ai_questions'] = json.loads(project_dict['ai_questions']) if project_dict['ai_questions'] else []
        project_dict['ai_analysis'] = json.loads(project_dict['ai_analysis']) if project_dict['ai_analysis'] else None
        
        return jsonify({
            'message': 'Projeto atualizado com sucesso',
            'project': project_dict
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        user = get_current_user(request)
        if not user:
            return jsonify({'message': 'Token inválido'}), 401
            
        conn = get_db_connection()
        
        # Verificar se o projeto existe e pertence ao usuário
        project = conn.execute('SELECT id FROM projects WHERE id = ? AND user_id = ?', (project_id, user['id'])).fetchone()
        if not project:
            conn.close()
            return jsonify({'message': 'Projeto não encontrado'}), 404
        
        # Deletar projeto
        conn.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Projeto excluído com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

# ROTA DE HEALTH CHECK
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        users_count = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
        projects_count = conn.execute('SELECT COUNT(*) as count FROM projects').fetchone()['count']
        conn.close()
        
        return jsonify({
            'status': 'online',
            'message': 'Apollo Project Orchestrator Backend',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat(),
            'database': 'SQLite',
            'users_count': users_count,
            'projects_count': projects_count
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro no banco de dados: {str(e)}'
        }), 500

# ROTAS DE SIMULAÇÃO DE IA
@app.route('/api/ai/analyze', methods=['POST'])
def analyze_documents():
    try:
        user = get_current_user(request)
        if not user:
            return jsonify({'message': 'Token inválido'}), 401
            
        # Simulação de análise de IA
        questions = [
            {
                'id': 1,
                'category': 'Requisitos Funcionais',
                'question': 'Quais são os principais módulos que o sistema deve conter?',
                'priority': 'high',
                'context': 'Baseado na análise dos documentos, identifiquei a necessidade de definir melhor a arquitetura modular.'
            },
            {
                'id': 2,
                'category': 'Integração',
                'question': 'O sistema precisa se integrar com algum sistema existente? Se sim, quais?',
                'priority': 'high',
                'context': 'Para garantir a compatibilidade e fluxo de dados adequado.'
            },
            {
                'id': 3,
                'category': 'Usuários',
                'question': 'Quantos usuários simultâneos o sistema deve suportar?',
                'priority': 'medium',
                'context': 'Importante para dimensionar a infraestrutura adequada.'
            },
            {
                'id': 4,
                'category': 'Segurança',
                'question': 'Quais são os requisitos de segurança e conformidade necessários?',
                'priority': 'high',
                'context': 'Considerando as melhores práticas de segurança para sistemas comerciais.'
            }
        ]
        
        analysis = {
            'summary': 'Análise concluída com sucesso. Foram identificados pontos importantes para o desenvolvimento do projeto.',
            'questions': questions,
            'insights': [
                'Projeto bem estruturado com objetivos claros',
                'Documentação fornece boa base para desenvolvimento',
                'Identificadas oportunidades de otimização no processo'
            ],
            'next_steps': [
                'Aguardar respostas das perguntas críticas',
                'Definir arquitetura técnica detalhada',
                'Elaborar cronograma de desenvolvimento'
            ]
        }
        
        return jsonify(analysis), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Iniciando Apollo Project Orchestrator Backend...")
    print("📊 Banco de dados: SQLite (apollo.db)")
    print("🔐 Autenticação: Token baseado em timestamp")
    print("🌐 CORS: Habilitado")
    print("📡 Servidor rodando em: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# ROTAS DE AUTENTICAÇÃO

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validações
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Nome, email e senha são obrigatórios'}), 400
        
        # Verificar se usuário já existe
        if any(u['email'] == data['email'] for u in data_store['users']):
            return jsonify({'message': 'Email já cadastrado'}), 400
        
        # Criar novo usuário
        user = {
            'id': data_store['next_user_id'],
            'name': data['name'],
            'email': data['email'],
            'password_hash': hash_password(data['password']),
            'created_at': datetime.now().isoformat()
        }
        
        data_store['users'].append(user)
        data_store['next_user_id'] += 1
        save_data()
        
        # Criar token
        token = generate_token(user['id'])
        
        # Remover senha do retorno
        user_response = {k: v for k, v in user.items() if k != 'password_hash'}
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'user': user_response,
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Email e senha são obrigatórios'}), 400
        
        # Buscar usuário
        user = next((u for u in data_store['users'] if u['email'] == data['email']), None)
        
        if not user or not verify_password(data['password'], user['password_hash']):
            return jsonify({'message': 'Email ou senha incorretos'}), 401
        
        # Criar token
        token = generate_token(user['id'])
        
        # Remover senha do retorno
        user_response = {k: v for k, v in user.items() if k != 'password_hash'}
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': user_response,
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/api/auth/verify', methods=['GET'])
def verify_token_route():
    try:
        user = get_current_user(request)
        
        if not user:
            return jsonify({'message': 'Token inválido'}), 401
        
        # Remover senha do retorno
        user_response = {k: v for k, v in user.items() if k != 'password_hash'}
        
        return jsonify({
            'message': 'Token válido',
            'user': user_response
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

# ROTAS DE PROJETOS

@app.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        user = get_current_user(request)
        if not user:
            return jsonify({'message': 'Token inválido'}), 401
        
        user_projects = [p for p in data_store['projects'] if p['user_id'] == user['id']]
        
        return jsonify(user_projects), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/api/projects', methods=['POST'])
def create_project():
    try:
        user = get_current_user(request)
        if not user:
            return jsonify({'message': 'Token inválido'}), 401
            
        data = request.get_json()
        
        # Validações
        required_fields = ['name', 'client', 'responsible', 'objective']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} é obrigatório'}), 400
        
        # Criar projeto
        project = {
            'id': data_store['next_project_id'],
            'name': data['name'],
            'client': data['client'],
            'responsible': data['responsible'],
            'objective': data['objective'],
            'description': data.get('description', ''),
            'priority': data.get('priority', 'medium'),
            'status': 'active',
            'current_step': 0,
            'start_date': data.get('start_date'),
            'deadline': data.get('deadline'),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'user_id': user['id'],
            'uploaded_files': [],
            'ai_questions': [],
            'ai_analysis': None
        }
        
        data_store['projects'].append(project)
        data_store['next_project_id'] += 1
        save_data()
        
        return jsonify({
            'message': 'Projeto criado com sucesso',
            'project': project
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        user = get_current_user(request)
        if not user:
            return jsonify({'message': 'Token inválido'}), 401
            
        # Buscar projeto
        project_index = next((i for i, p in enumerate(data_store['projects']) 
                            if p['id'] == project_id and p['user_id'] == user['id']), None)
        
        if project_index is None:
            return jsonify({'message': 'Projeto não encontrado'}), 404
        
        data = request.get_json()
        project = data_store['projects'][project_index]
        
        # Atualizar campos
        for field in ['name', 'client', 'responsible', 'objective', 'description', 
                     'priority', 'current_step', 'start_date', 'deadline', 
                     'uploaded_files', 'ai_questions', 'ai_analysis']:
            if field in data:
                project[field] = data[field]
        
        project['updated_at'] = datetime.now().isoformat()
        save_data()
        
        return jsonify({
            'message': 'Projeto atualizado com sucesso',
            'project': project
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        user = get_current_user(request)
        if not user:
            return jsonify({'message': 'Token inválido'}), 401
            
        # Buscar projeto
        project_index = next((i for i, p in enumerate(data_store['projects']) 
                            if p['id'] == project_id and p['user_id'] == user['id']), None)
        
        if project_index is None:
            return jsonify({'message': 'Projeto não encontrado'}), 404
        
        data_store['projects'].pop(project_index)
        save_data()
        
        return jsonify({'message': 'Projeto excluído com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

# ROTA DE HEALTH CHECK
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'online',
        'message': 'Apollo Project Orchestrator Backend',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'users_count': len(data_store['users']),
        'projects_count': len(data_store['projects'])
    }), 200

# ROTAS DE SIMULAÇÃO DE IA
@app.route('/api/ai/analyze', methods=['POST'])
def analyze_documents():
    try:
        user = get_current_user(request)
        if not user:
            return jsonify({'message': 'Token inválido'}), 401
            
        # Simulação de análise de IA
        questions = [
            {
                'id': 1,
                'category': 'Requisitos Funcionais',
                'question': 'Quais são os principais módulos que o sistema deve conter?',
                'priority': 'high',
                'context': 'Baseado na análise dos documentos, identifiquei a necessidade de definir melhor a arquitetura modular.'
            },
            {
                'id': 2,
                'category': 'Integração',
                'question': 'O sistema precisa se integrar com algum sistema existente? Se sim, quais?',
                'priority': 'high',
                'context': 'Para garantir a compatibilidade e fluxo de dados adequado.'
            },
            {
                'id': 3,
                'category': 'Usuários',
                'question': 'Quantos usuários simultâneos o sistema deve suportar?',
                'priority': 'medium',
                'context': 'Importante para dimensionar a infraestrutura adequada.'
            },
            {
                'id': 4,
                'category': 'Segurança',
                'question': 'Quais são os requisitos de segurança e conformidade necessários?',
                'priority': 'high',
                'context': 'Considerando as melhores práticas de segurança para sistemas comerciais.'
            }
        ]
        
        analysis = {
            'summary': 'Análise concluída com sucesso. Foram identificados pontos importantes para o desenvolvimento do projeto.',
            'questions': questions,
            'insights': [
                'Projeto bem estruturado com objetivos claros',
                'Documentação fornece boa base para desenvolvimento',
                'Identificadas oportunidades de otimização no processo'
            ],
            'next_steps': [
                'Aguardar respostas das perguntas críticas',
                'Definir arquitetura técnica detalhada',
                'Elaborar cronograma de desenvolvimento'
            ]
        }
        
        return jsonify(analysis), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Iniciando Apollo Project Orchestrator Backend...")
    print("📊 Armazenamento: Arquivo JSON")
    print("🔐 Autenticação: Token simples")
    print("🌐 CORS: Habilitado")
    print("📡 Servidor rodando em: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)