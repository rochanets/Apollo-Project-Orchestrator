from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models.database import db, User, AuditLog

users_bp = Blueprint('users', __name__)

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

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        # Campos que podem ser atualizados
        updatable_fields = ['name', 'company', 'role']
        updated_fields = []
        
        for field in updatable_fields:
            if field in data and data[field] != getattr(user, field):
                setattr(user, field, data[field])
                updated_fields.append(field)
        
        if updated_fields:
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Log da ação
            log_action(current_user_id, 'profile_updated', 'user', current_user_id, {'fields': updated_fields})
        
        return jsonify({
            'message': 'Perfil atualizado com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@users_bp.route('/', methods=['GET'])
@jwt_required()
def list_users():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Apenas admins podem listar usuários
        if not current_user or current_user.user_level != 'admin':
            return jsonify({'error': 'Acesso negado'}), 403
        
        users = User.query.filter_by(is_active=True).all()
        users_data = [user.to_dict() for user in users]
        
        return jsonify({'users': users_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@users_bp.route('/<int:user_id>/deactivate', methods=['PUT'])
@jwt_required()
def deactivate_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Apenas admins podem desativar usuários
        if not current_user or current_user.user_level != 'admin':
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Não pode desativar a si mesmo
        if user_id == current_user_id:
            return jsonify({'error': 'Não é possível desativar sua própria conta'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log da ação
        log_action(current_user_id, 'user_deactivated', 'user', user_id, {'email': user.email})
        
        return jsonify({'message': 'Usuário desativado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

