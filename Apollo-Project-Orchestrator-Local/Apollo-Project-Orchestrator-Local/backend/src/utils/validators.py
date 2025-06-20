"""
Validadores para autenticação e outros módulos
"""
import re

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