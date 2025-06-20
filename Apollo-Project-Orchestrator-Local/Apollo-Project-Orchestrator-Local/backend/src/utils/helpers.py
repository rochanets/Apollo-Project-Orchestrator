"""
Funções auxiliares para o sistema
"""
from datetime import datetime
from flask import request, current_app

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
        from src.models.database import AuditLog, db
        
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