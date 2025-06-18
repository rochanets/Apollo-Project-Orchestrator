from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(100))
    role = db.Column(db.String(50))
    user_level = db.Column(db.String(20), default='user')  # 'admin' ou 'user'
    email_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
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
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'company': self.company,
            'role': self.role,
            'user_level': self.user_level,
            'email_verified': self.email_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    client = db.Column(db.String(100), nullable=False)
    responsible = db.Column(db.String(100), nullable=False)
    objective = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='active')  # 'active', 'paused', 'completed', 'cancelled'
    priority = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high', 'urgent'
    current_step = db.Column(db.Integer, default=0)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    github_repo_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relacionamentos
    permissions = db.relationship('ProjectPermission', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    steps = db.relationship('ProjectStep', backref='project', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
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
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class ProjectPermission(db.Model):
    __tablename__ = 'project_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    permission_level = db.Column(db.String(20), nullable=False)  # 'owner', 'editor', 'viewer'
    granted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('project_id', 'user_id'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'permission_level': self.permission_level,
            'granted_by': self.granted_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ProjectStep(db.Model):
    __tablename__ = 'project_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    step_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'in_progress', 'completed', 'skipped'
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    __table_args__ = (db.UniqueConstraint('project_id', 'step_number'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'step_number': self.step_number,
            'step_name': self.step_name,
            'description': self.description,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'notes': self.notes
        }

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)  # 'user', 'project', 'permission'
    resource_id = db.Column(db.Integer)
    details = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


