-- Script de inicialização para ambiente de desenvolvimento do Apollo

-- Inserir usuários de teste
INSERT INTO users (name, email, password_hash, user_level, email_verified, is_active, company, role) 
VALUES 
  (
    'Developer Admin', 
    'dev@apollo.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLkYU1RyOewBfYS', 
    'admin', 
    true, 
    true,
    'Apollo Team',
    'Desenvolvedor'
  ),
  (
    'User Test', 
    'user@apollo.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLkYU1RyOewBfYS', 
    'user', 
    true, 
    true,
    'Empresa Teste',
    'Analista'
  ),
  (
    'Cliente Demo', 
    'cliente@apollo.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewLkYU1RyOewBfYS', 
    'user', 
    true, 
    true,
    'Cliente Corp',
    'Gerente de Projetos'
  )
ON CONFLICT (email) DO NOTHING;

-- Inserir projetos de exemplo
INSERT INTO projects (name, client, responsible, objective, description, owner_id, status, priority, estimated_hours)
SELECT 
  'Sistema de Gestão Apollo',
  'Apollo Technologies',
  'Equipe de Desenvolvimento',
  'Criar um sistema completo de gestão de projetos com IA integrada para otimizar o workflow de desenvolvimento',
  'Este projeto visa desenvolver uma plataforma moderna que utiliza inteligência artificial para auxiliar na gestão de projetos de software, desde a concepção até o deploy.',
  u.id,
  'active',
  'high',
  320
FROM users u WHERE u.email = 'dev@apollo.com'
ON CONFLICT DO NOTHING;

INSERT INTO projects (name, client, responsible, objective, description, owner_id, status, priority, estimated_hours)
SELECT 
  'Portal de E-commerce',
  'Loja Virtual XYZ',
  'Time de Frontend',
  'Desenvolver um portal de e-commerce responsivo com sistema de pagamentos integrado',
  'Criação de uma loja virtual completa com catálogo de produtos, carrinho de compras, sistema de pagamentos e painel administrativo.',
  u.id,
  'active',
  'medium',
  160
FROM users u WHERE u.email = 'user@apollo.com'
ON CONFLICT DO NOTHING;

INSERT INTO projects (name, client, responsible, objective, description, owner_id, status, priority, estimated_hours)
SELECT 
  'API de Microserviços',
  'Tech Solutions Inc',
  'Arquiteto de Software',
  'Implementar arquitetura de microserviços para sistema legado',
  'Migração de sistema monolítico para arquitetura de microserviços usando containers Docker e orquestração Kubernetes.',
  u.id,
  'paused',
  'urgent',
  240
FROM users u WHERE u.email = 'cliente@apollo.com'
ON CONFLICT DO NOTHING;

-- Inserir etapas para o primeiro projeto
INSERT INTO project_steps (project_id, step_number, step_name, description, status, estimated_hours)
SELECT 
  p.id,
  0,
  'Cadastro do Projeto',
  'Definição inicial do escopo e objetivos do projeto',
  'completed',
  8
FROM projects p WHERE p.name = 'Sistema de Gestão Apollo';

INSERT INTO project_steps (project_id, step_number, step_name, description, status, estimated_hours)
SELECT 
  p.id,
  1,
  'Análise de Requisitos',
  'Levantamento detalhado dos requisitos funcionais e não-funcionais',
  'completed',
  40
FROM projects p WHERE p.name = 'Sistema de Gestão Apollo';

INSERT INTO project_steps (project_id, step_number, step_name, description, status, estimated_hours)
SELECT 
  p.id,
  2,
  'Design da Arquitetura',
  'Definição da arquitetura do sistema e tecnologias a serem utilizadas',
  'in_progress',
  32
FROM projects p WHERE p.name = 'Sistema de Gestão Apollo';

INSERT INTO project_steps (project_id, step_number, step_name, description, status, estimated_hours)
SELECT 
  p.id,
  3,
  'Desenvolvimento Backend',
  'Implementação das APIs e lógica de negócio',
  'pending',
  120
FROM projects p WHERE p.name = 'Sistema de Gestão Apollo';

INSERT INTO project_steps (project_id, step_number, step_name, description, status, estimated_hours)
SELECT 
  p.id,
  4,
  'Desenvolvimento Frontend',
  'Criação da interface de usuário responsiva',
  'pending',
  80
FROM projects p WHERE p.name = 'Sistema de Gestão Apollo';

INSERT INTO project_steps (project_id, step_number, step_name, description, status, estimated_hours)
SELECT 
  p.id,
  5,
  'Testes e QA',
  'Testes unitários, integração e aceitação do usuário',
  'pending',
  40
FROM projects p WHERE p.name = 'Sistema de Gestão Apollo';

-- Inserir permissões de projeto
INSERT INTO project_permissions (project_id, user_id, permission_level, granted_by)
SELECT 
  p.id,
  owner.id,
  'owner',
  owner.id
FROM projects p
JOIN users owner ON p.owner_id = owner.id
ON CONFLICT (project_id, user_id) DO NOTHING;

-- Adicionar permissões colaborativas
INSERT INTO project_permissions (project_id, user_id, permission_level, granted_by)
SELECT 
  p.id,
  u.id,
  'editor',
  p.owner_id
FROM projects p
CROSS JOIN users u
WHERE u.email != (SELECT email FROM users WHERE id = p.owner_id)
  AND u.user_level = 'user'
ON CONFLICT (project_id, user_id) DO NOTHING;

-- Atualizar completion_percentage dos projetos baseado nas etapas
UPDATE projects 
SET completion_percentage = (
  SELECT COALESCE(
    ROUND(
      (COUNT(CASE WHEN ps.status = 'completed' THEN 1 END) * 100.0) / COUNT(*)
    ), 0
  )
  FROM project_steps ps 
  WHERE ps.project_id = projects.id
)
WHERE id IN (SELECT DISTINCT project_id FROM project_steps);

-- Inserir alguns logs de auditoria de exemplo
INSERT INTO audit_logs (user_id, action, resource_type, resource_id, details, ip_address, user_agent, success)
SELECT 
  u.id,
  'user_login',
  'user',
  u.id,
  '{"login_method": "email_password"}',
  '127.0.0.1',
  'Mozilla/5.0 (Development Environment)',
  true
FROM users u
WHERE u.email IN ('dev@apollo.com', 'user@apollo.com');

INSERT INTO audit_logs (user_id, action, resource_type, resource_id, details, ip_address, user_agent, success)
SELECT 
  p.owner_id,
  'project_created',
  'project',
  p.id,
  JSON_BUILD_OBJECT('name', p.name, 'client', p.client),
  '127.0.0.1',
  'Mozilla/5.0 (Development Environment)',
  true
FROM projects p;

-- Comentários finais
-- Senhas para todos os usuários de teste: Test123!@#
-- Emails:
-- - dev@apollo.com (Admin)
-- - user@apollo.com (User)  
-- - cliente@apollo.com (User)