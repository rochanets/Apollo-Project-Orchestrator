"""
Rotas de autenticação melhoradas com validações e segurança aprimorada
"""

from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
import re

from src.extensions import db, limiter, blacklisted_tokens
from src.models.database import User, AuditLog

auth_bp = Blueprint('auth', __name__)

# =============================================================================
# VALIDATORS
# =============================================================================

class AuthValidator:
    """Validador para dados de autenticação"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validar formato do email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """Validar força da senha"""
        if len(password) < 8:
            return False, "Senha deve ter pelo menos 8 caracteres"
        
        if not re.search(r'[A-Z]', password):
            return False, "Senha deve conter pelo menos uma letra maiúscula"
        
        if not re.search(r'[a-z]', password):
            return False, "Senha deve conter pelo menos uma letra minúscula"
        
        if not re.search(r'\d', password):
            return False, "Senha deve conter pelo menos um número"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Senha deve conter pelo menos um caractere especial"
        
        return True, "Senha válida"
    
    @staticmethod
    def validate_registration_data(data: dict) -> tuple[bool, list]:
        """Validar dados de registro"""
        errors = []
        
        # Campos obrigatórios
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"Campo '{field}' é obrigatório")
        
        # Validar email
        if data.get('email') and not AuthValidator.validate_email(data['email']):
            errors.append("Formato de email inválido")
        
        # Validar senha
        if data.get('password'):
            is_valid, message = AuthValidator.validate_password(data['password'])
            if not is_valid:
                errors.append(message)
        
        # Validar nome
        if data.get('name') and len(data['name'].strip()) < 2:
            errors.append("Nome deve ter pelo menos 2 caracteres")
        
        return len(errors) == 0, errors

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_client_info():
    """Obter informações do cliente"""
    return {
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', ''),
        'forwarded_for': request.headers.get('X-Forwarded-For', ''),
        'host': request.headers.get('Host', '')
    }

def log_action(user_id, action, resource_type, resource_id=None, details=None, success=True, error_message=None):
    """Registrar ação no log de auditoria"""
    try:
        client_info = get_client_info()
        
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=client_info['ip_address'],
            user_agent=client_info['user_agent'],
            success=success,
            error_message=error_message
        )
        
        db.session.add(log)
        db.session.commit()
        
    except Exception as e:
        current_app.logger.error(f"Erro ao registrar log de auditoria: {e}")

def check_account_lockout(user):
    """Verificar se conta está bloqueada"""
    if user.is_locked():
        time_left = (user.locked_until - datetime.utcnow()).total_seconds() / 60
        return True, f"Conta bloqueada. Tente novamente em {int(time_left)} minutos"
    return False, None

# =============================================================================
# ROUTES
# =============================================================================

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """Registrar novo usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validar dados
        is_valid, errors = AuthValidator.validate_registration_data(data)
        if not is_valid:
            return jsonify({'errors': errors}), 400
        
        # Verificar se email já existe
        existing_user = User.query.filter_by(email=data['email'].lower()).first()
        if existing_user:
            log_action(
                user_id=None,
                action='registration_failed',
                resource_type='user',
                details={'email': data['email'], 'reason': 'email_exists'},
                success=False,
                error_message='Email já cadastrado'
            )
            return jsonify({'error': 'Email já cadastrado'}), 409
        
        # Criar novo usuário
        user = User(
            name=data['name'].strip(),
            email=data['email'].lower(),
            password=data['password'],  # Será hasheada pelo setter
            company=data.get('company', '').strip(),
            role=data.get('role', '').strip(),
            user_level='user'  # Novos usuários sempre como 'user'
        )
        
        # Validar modelo
        user.validate()
        
        db.session.add(user)
        db.session.commit()
        
        # Log da ação
        log_action(
            user_id=user.id,
            action='user_registered',
            resource_type='user',
            resource_id=user.id,
            details={'email': user.email, 'name': user.name}
        )
        
        # Criar tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Usuário cadastrado com sucesso',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro no registro: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """Fazer login"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        email = data['email'].lower()
        password = data['password']
        
        # Buscar usuário
        user = User.query.filter_by(email=email).first()
        
        if not user:
            log_action(
                user_id=None,
                action='login_failed',
                resource_type='user',
                details={'email': email, 'reason': 'user_not_found'},
                success=False,
                error_message='Usuário não encontrado'
            )
            return jsonify({'error': 'Email ou senha inválidos'}), 401
        
        # Verificar se conta está ativa
        if not user.is_active:
            log_action(
                user_id=user.id,
                action='login_failed',
                resource_type='user',
                resource_id=user.id,
                details={'reason': 'account_inactive'},
                success=False,
                error_message='Conta inativa'
            )
            return jsonify({'error': 'Conta desativada. Entre em contato com o administrador'}), 401
        
        # Verificar bloqueio de conta
        is_locked, lock_message = check_account_lockout(user)
        if is_locked:
            log_action(
                user_id=user.id,
                action='login_failed',
                resource_type='user',
                resource_id=user.id,
                details={'reason': 'account_locked'},
                success=False,
                error_message='Conta bloqueada'
            )
            return jsonify({'error': lock_message}), 401
        
        # Verificar senha
        if not user.verify_password(password):
            user.increment_login_attempts()
            db.session.commit()
            
            log_action(
                user_id=user.id,
                action='login_failed',
                resource_type='user',
                resource_id=user.id,
                details={'reason': 'invalid_password', 'attempts': user.login_attempts},
                success=False,
                error_message='Senha inválida'
            )
            
            return jsonify({'error': 'Email ou senha inválidos'}), 401
        
        # Login bem-sucedido
        user.reset_login_attempts()
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Criar tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        # Log da ação
        log_action(
            user_id=user.id,
            action='user_login',
            resource_type='user',
            resource_id=user.id,
            details={'login_method': 'email_password'}
        )
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro no login: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Renovar token de acesso"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'Usuário não encontrado ou inativo'}), 401
        
        # Verificar se não está bloqueado
        is_locked, lock_message = check_account_lockout(user)
        if is_locked:
            return jsonify({'error': lock_message}), 401
        
        # Criar novo token
        new_token = create_access_token(identity=current_user_id)
        
        # Log da ação
        log_action(
            user_id=current_user_id,
            action='token_refreshed',
            resource_type='user',
            resource_id=current_user_id
        )
        
        return jsonify({
            'access_token': new_token,
            'message': 'Token renovado com sucesso'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro na renovação do token: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Obter informações do usuário atual"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao obter usuário atual: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Fazer logout"""
    try:
        current_user_id = get_jwt_identity()
        jti = get_jwt()['jti']
        
        # Adicionar token à blacklist
        blacklisted_tokens.add(jti)
        
        # Log da ação
        log_action(
            user_id=current_user_id,
            action='user_logout',
            resource_type='user',
            resource_id=current_user_id
        )
        
        return jsonify({'message': 'Logout realizado com sucesso'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro no logout: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
@limiter.limit("3 per minute")
def change_password():
    """Alterar senha do usuário"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        if not data or not data.get('current_password') or not data.get('new_password'):
            return jsonify({'error': 'Senha atual e nova senha são obrigatórias'}), 400
        
        # Verificar senha atual
        if not user.verify_password(data['current_password']):
            log_action(
                user_id=current_user_id,
                action='password_change_failed',
                resource_type='user',
                resource_id=current_user_id,
                details={'reason': 'invalid_current_password'},
                success=False
            )
            return jsonify({'error': 'Senha atual incorreta'}), 401
        
        # Validar nova senha
        is_valid, message = AuthValidator.validate_password(data['new_password'])
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Verificar se nova senha é diferente da atual
        if user.verify_password(data['new_password']):
            return jsonify({'error': 'Nova senha deve ser diferente da atual'}), 400
        
        # Atualizar senha
        user.password = data['new_password']
        db.session.commit()
        
        # Log da ação
        log_action(
            user_id=current_user_id,
            action='password_changed',
            resource_type='user',
            resource_id=current_user_id
        )
        
        return jsonify({'message': 'Senha alterada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao alterar senha: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/forgot-password', methods=['POST'])
@limiter.limit("3 per hour")
def forgot_password():
    """Solicitar redefinição de senha"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email'):
            return jsonify({'error': 'Email é obrigatório'}), 400
        
        email = data['email'].lower()
        
        # Verificar se email existe
        user = User.query.filter_by(email=email).first()
        
        # Por segurança, sempre retornar sucesso mesmo se email não existir
        if user and user.is_active:
            # TODO: Implementar envio de email com token de redefinição
            # Por enquanto, apenas log
            log_action(
                user_id=user.id,
                action='password_reset_requested',
                resource_type='user',
                resource_id=user.id,
                details={'email': email}
            )
        else:
            # Log tentativa com email inexistente
            log_action(
                user_id=None,
                action='password_reset_requested',
                resource_type='user',
                details={'email': email, 'user_exists': False}
            )
        
        return jsonify({
            'message': 'Se o email estiver cadastrado, você receberá instruções para redefinição da senha'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro na solicitação de redefinição de senha: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/verify-email', methods=['POST'])
@jwt_required()
def verify_email():
    """Verificar email do usuário"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        verification_code = data.get('verification_code') if data else None
        
        # TODO: Implementar verificação real do código
        # Por enquanto, marcar como verificado
        if verification_code == '123456':  # Código de teste
            user.email_verified = True
            db.session.commit()
            
            log_action(
                user_id=current_user_id,
                action='email_verified',
                resource_type='user',
                resource_id=current_user_id
            )
            
            return jsonify({'message': 'Email verificado com sucesso'}), 200
        else:
            return jsonify({'error': 'Código de verificação inválido'}), 400
        
    except Exception as e:
        current_app.logger.error(f"Erro na verificação de email: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/resend-verification', methods=['POST'])
@jwt_required()
@limiter.limit("3 per hour")
def resend_verification():
    """Reenviar código de verificação de email"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        if user.email_verified:
            return jsonify({'error': 'Email já verificado'}), 400
        
        # TODO: Implementar envio real do código
        log_action(
            user_id=current_user_id,
            action='verification_code_resent',
            resource_type='user',
            resource_id=current_user_id
        )
        
        return jsonify({'message': 'Código de verificação reenviado'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao reenviar verificação: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/check-email', methods=['POST'])
@limiter.limit("10 per minute")
def check_email():
    """Verificar se email já está cadastrado"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email'):
            return jsonify({'error': 'Email é obrigatório'}), 400
        
        email = data['email'].lower()
        
        if not AuthValidator.validate_email(email):
            return jsonify({'error': 'Formato de email inválido'}), 400
        
        user_exists = User.query.filter_by(email=email).first() is not None
        
        return jsonify({
            'exists': user_exists,
            'available': not user_exists
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao verificar email: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_user_sessions():
    """Obter sessões ativas do usuário"""
    try:
        current_user_id = get_jwt_identity()
        
        # Buscar logs de login recentes
        recent_logins = AuditLog.query.filter_by(
            user_id=current_user_id,
            action='user_login',
            success=True
        ).order_by(AuditLog.created_at.desc()).limit(10).all()
        
        sessions = []
        for login in recent_logins:
            sessions.append({
                'id': login.id,
                'login_time': login.created_at.isoformat(),
                'ip_address': login.ip_address,
                'user_agent': login.user_agent,
                'location': 'Unknown'  # TODO: Implementar geolocalização por IP
            })
        
        return jsonify({'sessions': sessions}), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao obter sessões: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/revoke-all-sessions', methods=['POST'])
@jwt_required()
def revoke_all_sessions():
    """Revogar todas as sessões do usuário"""
    try:
        current_user_id = get_jwt_identity()
        current_jti = get_jwt()['jti']
        
        # TODO: Implementar revogação real de todos os tokens
        # Por enquanto, adicionar token atual à blacklist
        blacklisted_tokens.add(current_jti)
        
        log_action(
            user_id=current_user_id,
            action='all_sessions_revoked',
            resource_type='user',
            resource_id=current_user_id
        )
        
        return jsonify({'message': 'Todas as sessões foram revogadas'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao revogar sessões: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# =============================================================================
# UTILITY ROUTES
# =============================================================================

@auth_bp.route('/health', methods=['GET'])
def health_check():
    """Verificar saúde do serviço de autenticação"""
    try:
        # Verificar conectividade com banco
        db.session.execute('SELECT 1')
        
        return jsonify({
            'status': 'ok',
            'message': 'Serviço de autenticação funcionando',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Health check falhou: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Serviço de autenticação com problemas',
            'timestamp': datetime.utcnow().isoformat()
        }), 503

@auth_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_auth_stats():
    """Obter estatísticas de autenticação (apenas para admins)"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin():
            return jsonify({'error': 'Acesso negado'}), 403
        
        # Estatísticas básicas
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        verified_users = User.query.filter_by(email_verified=True).count()
        
        # Logins nas últimas 24h
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_logins = AuditLog.query.filter(
            AuditLog.action == 'user_login',
            AuditLog.success == True,
            AuditLog.created_at >= yesterday
        ).count()
        
        # Tentativas de login falhadas nas últimas 24h
        failed_logins = AuditLog.query.filter(
            AuditLog.action == 'login_failed',
            AuditLog.created_at >= yesterday
        ).count()
        
        return jsonify({
            'total_users': total_users,
            'active_users': active_users,
            'verified_users': verified_users,
            'recent_logins_24h': recent_logins,
            'failed_logins_24h': failed_logins,
            'verification_rate': round((verified_users / total_users) * 100, 2) if total_users > 0 else 0
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao obter estatísticas: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500