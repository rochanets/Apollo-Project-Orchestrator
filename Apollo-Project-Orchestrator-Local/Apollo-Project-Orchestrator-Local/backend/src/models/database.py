"""
Modelos de dados melhorados para o Apollo Project Orchestrator
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, event
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
import re

db = SQLAlchemy()

# =============================================================================
# MIXINS
# =============================================================================

class TimestampMixin:
    """Mixin para adicionar timestamps automáticos"""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class AuditMixin(TimestampMixin):
    """Mixin para auditoria completa"""
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

# =============================================================================
# MODELOS PRINCIPAIS
# =============================================================================

class User(TimestampMixin, db.Model):
    """Modelo de usuário com validações e funcionalidades aprimoradas"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(100))
    role = db.Column(db.String(50))
    user_level = db.Column(db.String(20), default='user', nullable=False)  # 'admin', 'user'
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    
    # Índices para performance
    __table_args__ = (
        Index('idx_user_email_active', 'email', 'is_active'),
        Index('idx_user_level', 'user_level'),
        Index('idx_user_created_at', 'created_at'),
    )
    
    # Relacionamentos
    owned_projects = db.relationship('Project', foreign_keys='Project.owner_id', backref='owner', lazy='dynamic')
    project_permissions_as_user = db.relationship(
        'ProjectPermission', 
        foreign_keys='ProjectPermission.user_id', 
        backref='user_permission', 
        lazy='dynamic'
    )
    project_permissions_as_granter = db.relationship(
        'ProjectPermission', 
        foreign_keys='ProjectPermission.granted_by', 
        backref='granter_permission', 
        lazy='dynamic'
    )
    audit_logs_as_user = db.relationship(
        'AuditLog', 
        foreign_keys='AuditLog.user_id', 
        backref='user_audit_log', 
        lazy='dynamic'
    )
    
    @hybrid_property
    def password(self):
        """Propriedade write-only para senha"""
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """Setter para hash da senha"""
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """Verificar senha"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Verificar se é administrador"""
        return self.user_level == 'admin'
    
    def is_locked(self):
        """Verificar se conta está bloqueada"""
        if self.locked_until:
            return datetime.utcnow() < self.locked_until
        return False
    
    def lock_account(self, minutes=15):
        """Bloquear conta temporariamente"""
        self.locked_until = datetime.utcnow() + timedelta(minutes=minutes)
        self.login_attempts = 0
    
    def unlock_account(self):
        """Desbloquear conta"""
        self.locked_until = None
        self.login_attempts = 0
    
    def increment_login_attempts(self):
        """Incrementar tentativas de login"""
        self.login_attempts = (self.login_attempts or 0) + 1
        if self.login_attempts >= 5:
            self.lock_account()
    
    def reset_login_attempts(self):
        """Resetar tentativas de login"""
        self.login_attempts = 0
    
    def validate(self):
        """Validações customizadas"""
        errors = []
        
        # Validar nome
        if not self.name or len(self.name.strip()) < 2:
            errors.append("Nome deve ter pelo menos 2 caracteres")
        
        # Validar email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
        if not self.email or not re.match(email_pattern, self.email):
            errors.append("Email inválido")
        
        # Validar user_level
        if self.user_level not in ['admin', 'user']:
            errors.append("Nível de usuário deve ser 'admin' ou 'user'")
        
        if errors:
            raise ValueError('; '.join(errors))
    
    def to_dict(self, include_sensitive=False):
        """Converter para dicionário"""
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'company': self.company,
            'role': self.role,
            'user_level': self.user_level,
            'email_verified': self.email_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }
        
        if include_sensitive:
            data.update({
                'login_attempts': self.login_attempts,
                'locked_until': self.locked_until.isoformat() if self.locked_until else None
            })
        
        return data


class Project(AuditMixin, db.Model):
    """Modelo de projeto com validações e funcionalidades aprimoradas"""
    
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    client = db.Column(db.String(100), nullable=False)
    responsible = db.Column(db.String(100), nullable=False)
    objective = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='active', nullable=False)
    priority = db.Column(db.String(20), default='medium', nullable=False)
    current_step = db.Column(db.Integer, default=0)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    github_repo_url = db.Column(db.String(500))
    estimated_hours = db.Column(db.Integer)
    actual_hours = db.Column(db.Integer, default=0)
    completion_percentage = db.Column(db.Integer, default=0)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Índices para performance
    __table_args__ = (
        Index('idx_project_owner_status', 'owner_id', 'status'),
        Index('idx_project_created_at', 'created_at'),
        Index('idx_project_priority', 'priority'),
        Index('idx_project_completion', 'completion_percentage'),
    )
    
    # Relacionamentos
    permissions = db.relationship('ProjectPermission', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    steps = db.relationship('ProjectStep', backref='project', lazy='dynamic', cascade='all, delete-orphan', order_by='ProjectStep.step_number')
    files = db.relationship('ProjectFile', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    
    # Status válidos
    VALID_STATUSES = ['active', 'paused', 'completed', 'cancelled', 'on_hold']
    VALID_PRIORITIES = ['low', 'medium', 'high', 'urgent']
    
    @hybrid_property
    def is_completed(self):
        """Verificar se projeto está completo"""
        return self.status == 'completed'
    
    @hybrid_property
    def is_overdue(self):
        """Verificar se projeto está atrasado"""
        if self.end_date and not self.is_completed:
            return datetime.utcnow() > self.end_date
        return False
    
    def calculate_completion_percentage(self):
        """Calcular porcentagem de conclusão baseada nas etapas"""
        total_steps = self.steps.count()
        if total_steps == 0:
            return 0
        
        completed_steps = self.steps.filter_by(status='completed').count()
        return int((completed_steps / total_steps) * 100)
    
    def update_completion_percentage(self):
        """Atualizar porcentagem de conclusão"""
        self.completion_percentage = self.calculate_completion_percentage()
        
        # Se 100% completo, marcar como concluído
        if self.completion_percentage == 100 and self.status != 'completed':
            self.status = 'completed'
            self.completed_at = datetime.utcnow()
    
    def get_next_step(self):
        """Obter próxima etapa pendente"""
        return self.steps.filter_by(status='pending').order_by(ProjectStep.step_number).first()
    
    def validate(self):
        """Validações customizadas"""
        errors = []
        
        # Validar nome
        if not self.name or len(self.name.strip()) < 3:
            errors.append("Nome do projeto deve ter pelo menos 3 caracteres")
        
        # Validar objetivo
        if not self.objective or len(self.objective.strip()) < 10:
            errors.append("Objetivo deve ter pelo menos 10 caracteres")
        
        # Validar status
        if self.status not in self.VALID_STATUSES:
            errors.append(f"Status deve ser um dos: {', '.join(self.VALID_STATUSES)}")
        
        # Validar prioridade
        if self.priority not in self.VALID_PRIORITIES:
            errors.append(f"Prioridade deve ser uma das: {', '.join(self.VALID_PRIORITIES)}")
        
        # Validar datas
        if self.start_date and self.end_date and self.start_date > self.end_date:
            errors.append("Data de início não pode ser posterior à data de fim")
        
        if errors:
            raise ValueError('; '.join(errors))
    
    def to_dict(self, include_steps=False, include_permissions=False):
        """Converter para dicionário"""
        data = {
            'id': self.id,
            'name': self.name,
            'client': self.client,
            'responsible': self.responsible,
            'objective': self.objective,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'current_step': self.current_step,
            'owner_id': self.owner_id,
            'github_repo_url': self.github_repo_url,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours,
            'completion_percentage': self.completion_percentage,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'is_overdue': self.is_overdue
        }
        
        if include_steps:
            data['steps'] = [step.to_dict() for step in self.steps.order_by(ProjectStep.step_number)]
        
        if include_permissions:
            data['permissions'] = [perm.to_dict() for perm in self.permissions]
        
        return data


class ProjectPermission(TimestampMixin, db.Model):
    """Modelo de permissões de projeto"""
    
    __tablename__ = 'project_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    permission_level = db.Column(db.String(20), nullable=False)  # 'owner', 'editor', 'viewer'
    granted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    __table_args__ = (
        db.UniqueConstraint('project_id', 'user_id'),
        Index('idx_permission_project_user', 'project_id', 'user_id'),
    )
    
    # Níveis de permissão válidos
    VALID_LEVELS = ['owner', 'editor', 'viewer']
    
    def validate(self):
        """Validações customizadas"""
        if self.permission_level not in self.VALID_LEVELS:
            raise ValueError(f"Nível de permissão deve ser um dos: {', '.join(self.VALID_LEVELS)}")
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'permission_level': self.permission_level,
            'granted_by': self.granted_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ProjectStep(TimestampMixin, db.Model):
    """Modelo de etapas do projeto com funcionalidades aprimoradas"""
    
    __tablename__ = 'project_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    step_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending', nullable=False)
    estimated_hours = db.Column(db.Integer)
    actual_hours = db.Column(db.Integer, default=0)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    dependencies = db.Column(db.JSON)  # Lista de step_numbers que devem ser concluídos primeiro
    
    __table_args__ = (
        db.UniqueConstraint('project_id', 'step_number'),
        Index('idx_step_project_status', 'project_id', 'status'),
        Index('idx_step_assigned', 'assigned_to'),
    )
    
    # Status válidos
    VALID_STATUSES = ['pending', 'in_progress', 'completed', 'skipped', 'blocked']
    
    @hybrid_property
    def is_completed(self):
        """Verificar se etapa está completa"""
        return self.status == 'completed'
    
    @hybrid_property
    def is_overdue(self):
        """Verificar se etapa está atrasada"""
        # Implementar lógica baseada em estimativas e dependências
        return False
    
    def can_start(self):
        """Verificar se etapa pode ser iniciada (dependências resolvidas)"""
        if not self.dependencies:
            return True
        
        for dep_step_number in self.dependencies:
            dep_step = ProjectStep.query.filter_by(
                project_id=self.project_id,
                step_number=dep_step_number
            ).first()
            if not dep_step or not dep_step.is_completed:
                return False
        
        return True
    
    def start(self, user_id=None):
        """Iniciar etapa"""
        if self.status != 'pending':
            raise ValueError("Etapa deve estar pendente para ser iniciada")
        
        if not self.can_start():
            raise ValueError("Dependências não resolvidas")
        
        self.status = 'in_progress'
        self.started_at = datetime.utcnow()
        if user_id:
            self.assigned_to = user_id
    
    def complete(self, notes=None):
        """Completar etapa"""
        if self.status not in ['in_progress', 'pending']:
            raise ValueError("Etapa deve estar em progresso ou pendente para ser completada")
        
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        if notes:
            self.notes = notes
        
        # Atualizar porcentagem do projeto
        self.project.update_completion_percentage()
    
    def validate(self):
        """Validações customizadas"""
        errors = []
        
        # Validar nome
        if not self.step_name or len(self.step_name.strip()) < 3:
            errors.append("Nome da etapa deve ter pelo menos 3 caracteres")
        
        # Validar status
        if self.status not in self.VALID_STATUSES:
            errors.append(f"Status deve ser um dos: {', '.join(self.VALID_STATUSES)}")
        
        # Validar número da etapa
        if self.step_number < 0:
            errors.append("Número da etapa deve ser positivo")
        
        if errors:
            raise ValueError('; '.join(errors))
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'step_number': self.step_number,
            'step_name': self.step_name,
            'description': self.description,
            'status': self.status,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours,
            'assigned_to': self.assigned_to,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'notes': self.notes,
            'dependencies': self.dependencies,
            'can_start': self.can_start(),
            'is_overdue': self.is_overdue
        }


class ProjectFile(TimestampMixin, db.Model):
    """Modelo para arquivos do projeto"""
    
    __tablename__ = 'project_files'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    
    __table_args__ = (
        Index('idx_file_project', 'project_id'),
        Index('idx_file_uploaded_by', 'uploaded_by'),
    )
    
    @hybrid_property
    def file_extension(self):
        """Obter extensão do arquivo"""
        return self.filename.split('.')[-1].lower() if '.' in self.filename else ''
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'content_type': self.content_type,
            'file_extension': self.file_extension,
            'uploaded_by': self.uploaded_by,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AuditLog(TimestampMixin, db.Model):
    """Modelo de log de auditoria melhorado"""
    
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)
    resource_id = db.Column(db.Integer)
    details = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    session_id = db.Column(db.String(100))
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)
    
    __table_args__ = (
        Index('idx_audit_user_action', 'user_id', 'action'),
        Index('idx_audit_resource', 'resource_type', 'resource_id'),
        Index('idx_audit_created_at', 'created_at'),
    )
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'session_id': self.session_id,
            'success': self.success,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# =============================================================================
# EVENT LISTENERS
# =============================================================================

@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def validate_user(mapper, connection, target):
    """Validar usuário antes de inserir/atualizar"""
    target.validate()

@event.listens_for(Project, 'before_insert')
@event.listens_for(Project, 'before_update')
def validate_project(mapper, connection, target):
    """Validar projeto antes de inserir/atualizar"""
    target.validate()

@event.listens_for(ProjectStep, 'before_insert')
@event.listens_for(ProjectStep, 'before_update')
def validate_project_step(mapper, connection, target):
    """Validar etapa antes de inserir/atualizar"""
    target.validate()

@event.listens_for(ProjectStep, 'after_update')
def update_project_completion(mapper, connection, target):
    """Atualizar completion do projeto quando etapa muda"""
    if target.project:
        target.project.update_completion_percentage()