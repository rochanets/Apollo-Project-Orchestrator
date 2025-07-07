from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from src.extensions import db
from src.models.database import Project, ProjectPermission, ProjectStep, User, AuditLog

projects_bp = Blueprint('projects', __name__)

# Definição das etapas padrão do projeto
DEFAULT_STEPS = [
    {'step_number': 0, 'step_name': 'Cadastro do Projeto', 'description': 'Informações básicas do projeto'},
    {'step_number': 1, 'step_name': 'Upload de Documentos', 'description': 'Anexar documentação do projeto'},
    {'step_number': 2, 'step_name': 'Geração de Perguntas', 'description': 'IA gera perguntas críticas'},
    {'step_number': 3, 'step_name': 'Coleta de Informações', 'description': 'Documentação e esclarecimentos'},
    {'step_number': 4, 'step_name': 'Análise Técnica', 'description': 'Levantamento do ambiente'},
    {'step_number': 5, 'step_name': 'Execução do Projeto', 'description': 'Desenvolvimento automatizado'},
    {'step_number': 6, 'step_name': 'Testes', 'description': 'Testes integrados e correções'},
    {'step_number': 7, 'step_name': 'Go Live', 'description': 'Documentação final e deploy'}
]

def log_action(user_id, action, resource_type, resource_id=None, details=None):
    try:
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao registrar log: {e}")

def has_project_permission(user_id, project_id, required_level='viewer'):
    """Verifica se o usuário tem permissão no projeto"""
    project = Project.query.get(project_id)
    if not project:
        return False
    
    # Owner sempre tem permissão total
    if project.owner_id == user_id:
        return True
    
    # Verificar permissões específicas
    permission = ProjectPermission.query.filter_by(
        project_id=project_id,
        user_id=user_id
    ).first()
    
    if not permission:
        return False
    
    # Hierarquia de permissões: owner > editor > viewer
    levels = {'viewer': 1, 'editor': 2, 'owner': 3}
    return levels.get(permission.permission_level, 0) >= levels.get(required_level, 0)

@projects_bp.route('', methods=['GET'])
@projects_bp.route('/', methods=['GET'])
@jwt_required()
def get_projects():
    try:
        current_user_id = get_jwt_identity()
        
        # Buscar projetos onde o usuário é owner ou tem permissão
        owned_projects = Project.query.filter_by(owner_id=current_user_id).all()
        
        # Buscar projetos com permissão
        permissions = ProjectPermission.query.filter_by(user_id=current_user_id).all()
        shared_project_ids = [p.project_id for p in permissions]
        shared_projects = Project.query.filter(Project.id.in_(shared_project_ids)).all() if shared_project_ids else []
        
        # Combinar e remover duplicatas
        all_projects = list({p.id: p for p in owned_projects + shared_projects}.values())
        
        projects_data = []
        for project in all_projects:
            project_dict = project.to_dict()
            # Adicionar informação de permissão
            if project.owner_id == current_user_id:
                project_dict['permission_level'] = 'owner'
            else:
                permission = next((p for p in permissions if p.project_id == project.id), None)
                project_dict['permission_level'] = permission.permission_level if permission else 'viewer'
            
            projects_data.append(project_dict)
        
        return jsonify({'projects': projects_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@projects_bp.route('', methods=['POST'])
@projects_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        print("Recebendo dados para criar projeto:", data)
        
        # Validação dos campos obrigatórios
        required_fields = ['name', 'client', 'responsible', 'objective']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        # Criar novo projeto
        project = Project(
            name=data['name'],
            client=data['client'],
            responsible=data['responsible'],
            objective=data['objective'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            status=data.get('status', 'active'),  # ADICIONE ESTA LINHA
            owner_id=current_user_id
        )
        
        db.session.add(project)
        db.session.flush()
        
        # Criar etapas padrão
        for step_data in DEFAULT_STEPS:
            step = ProjectStep(
                project_id=project.id,
                step_number=step_data['step_number'],
                step_name=step_data['step_name'],
                description=step_data['description'],
                status=step_data.get('status', 'pending') # ADICIONE ESTA LINHA
            )
            db.session.add(step)
        
        # Criar permissão de owner para o criador
        permission = ProjectPermission(
            project_id=project.id,
            user_id=current_user_id,
            permission_level='owner',
            granted_by=current_user_id
        )
        db.session.add(permission)
        
        db.session.commit()
        
        # Log da ação
        log_action(current_user_id, 'project_created', 'project', project.id, {'name': project.name})
        
        return jsonify({
            'message': 'Projeto criado com sucesso',
            'project': project.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print("Erro ao criar projeto:", e)

        if isinstance(e, ValueError):
            # Retorna um erro 400 com a mensagem de validação
            return jsonify({'error': str(e)}), 400
        raise  # Isso faz o traceback aparecer no terminal

@projects_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    try:
        current_user_id = get_jwt_identity()
        
        if not has_project_permission(current_user_id, project_id, 'viewer'):
            return jsonify({'error': 'Acesso negado'}), 403
        
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Projeto não encontrado'}), 404
        
        # Buscar etapas do projeto
        steps = ProjectStep.query.filter_by(project_id=project_id).order_by(ProjectStep.step_number).all()
        
        project_data = project.to_dict()
        project_data['steps'] = [step.to_dict() for step in steps]
        
        return jsonify({'project': project_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@projects_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    try:
        current_user_id = get_jwt_identity()
        
        if not has_project_permission(current_user_id, project_id, 'editor'):
            return jsonify({'error': 'Acesso negado'}), 403
        
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Projeto não encontrado'}), 404
        
        data = request.get_json()
        
        # Atualizar campos permitidos
        updatable_fields = ['name', 'client', 'responsible', 'objective', 'description', 'status', 'priority', 'current_step']
        for field in updatable_fields:
            if field in data:
                setattr(project, field, data[field])
        
        project.updated_at = datetime.utcnow()
        
        # Se o status mudou para 'completed', definir data de conclusão
        if data.get('status') == 'completed' and project.completed_at is None:
            project.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        # Log da ação
        log_action(current_user_id, 'project_updated', 'project', project.id, {'fields': list(data.keys())})
        
        return jsonify({
            'message': 'Projeto atualizado com sucesso',
            'project': project.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    try:
        current_user_id = get_jwt_identity()
        
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Projeto não encontrado'}), 404
        
        # Apenas o owner pode deletar o projeto
        if project.owner_id != current_user_id:
            return jsonify({'error': 'Apenas o proprietário pode excluir o projeto'}), 403
        
        project_name = project.name
        
        # Deletar projeto (cascade vai deletar permissões e etapas)
        db.session.delete(project)
        db.session.commit()
        
        # Log da ação
        log_action(current_user_id, 'project_deleted', 'project', project_id, {'name': project_name})
        
        return jsonify({'message': 'Projeto excluído com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@projects_bp.route('/<int:project_id>/steps/<int:step_number>', methods=['PUT'])
@jwt_required()
def update_project_step(project_id, step_number):
    try:
        current_user_id = get_jwt_identity()
        
        if not has_project_permission(current_user_id, project_id, 'editor'):
            return jsonify({'error': 'Acesso negado'}), 403
        
        step = ProjectStep.query.filter_by(project_id=project_id, step_number=step_number).first()
        if not step:
            return jsonify({'error': 'Etapa não encontrada'}), 404
        
        data = request.get_json()
        
        # Atualizar status da etapa
        if 'status' in data:
            old_status = step.status
            step.status = data['status']
            
            if data['status'] == 'in_progress' and old_status != 'in_progress':
                step.started_at = datetime.utcnow()
            elif data['status'] == 'completed' and old_status != 'completed':
                step.completed_at = datetime.utcnow()
        
        # Atualizar notas
        if 'notes' in data:
            step.notes = data['notes']
        
        db.session.commit()
        
        # Log da ação
        log_action(current_user_id, 'project_step_updated', 'project', project_id, {
            'step_number': step_number,
            'status': data.get('status'),
            'notes_updated': 'notes' in data
        })
        
        return jsonify({
            'message': 'Etapa atualizada com sucesso',
            'step': step.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

