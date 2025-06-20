"""
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
