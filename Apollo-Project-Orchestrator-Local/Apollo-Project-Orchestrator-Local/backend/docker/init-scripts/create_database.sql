-- Script de inicialização do banco de dados PostgreSQL para Apollo Project Orchestrator

-- =============================================================================
-- EXTENSÕES NECESSÁRIAS
-- =============================================================================

-- UUID para gerar identificadores únicos
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Estatísticas de consulta para monitoramento
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Extensão para criptografia adicional (opcional)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =============================================================================
-- ESQUEMAS
-- =============================================================================

-- Criar esquema principal do Apollo
CREATE SCHEMA IF NOT EXISTS apollo;

-- =============================================================================
-- CONFIGURAÇÕES DE PERMISSÕES
-- =============================================================================

-- Garantir permissões completas para o usuário apollo
GRANT ALL PRIVILEGES ON SCHEMA apollo TO apollo;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA apollo TO apollo;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA apollo TO apollo;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA apollo TO apollo;

-- Configurar permissões padrão para objetos futuros
ALTER DEFAULT PRIVILEGES IN SCHEMA apollo 
    GRANT ALL PRIVILEGES ON TABLES TO apollo;
    
ALTER DEFAULT PRIVILEGES IN SCHEMA apollo 
    GRANT ALL PRIVILEGES ON SEQUENCES TO apollo;
    
ALTER DEFAULT PRIVILEGES IN SCHEMA apollo 
    GRANT ALL PRIVILEGES ON FUNCTIONS TO apollo;

-- =============================================================================
-- CONFIGURAÇÕES DE PERFORMANCE E SEGURANÇA
-- =============================================================================

-- Configurações de performance
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

-- Configurações de logging
ALTER SYSTEM SET log_statement = 'mod';
ALTER SYSTEM SET log_min_duration_statement = 1000;
ALTER SYSTEM SET log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h ';

-- Configurações de segurança
ALTER SYSTEM SET ssl = 'off'; -- Desabilitado para desenvolvimento
ALTER SYSTEM SET password_encryption = 'scram-sha-256';

-- =============================================================================
-- CONFIGURAÇÕES ESPECÍFICAS DO APOLLO
-- =============================================================================

-- Configurar timezone
ALTER SYSTEM SET timezone = 'America/Sao_Paulo';

-- Configurações de encoding
ALTER SYSTEM SET lc_messages = 'en_US.utf8';
ALTER SYSTEM SET lc_monetary = 'pt_BR.utf8';
ALTER SYSTEM SET lc_numeric = 'pt_BR.utf8';
ALTER SYSTEM SET lc_time = 'pt_BR.utf8';

-- =============================================================================
-- FUNÇÕES UTILITÁRIAS
-- =============================================================================

-- Função para atualizar timestamp automaticamente
CREATE OR REPLACE FUNCTION apollo.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Função para gerar slugs
CREATE OR REPLACE FUNCTION apollo.slugify(value TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN lower(
        regexp_replace(
            regexp_replace(
                regexp_replace(value, '[^a-zA-Z0-9\s-]', '', 'g'),
                '\s+', '-', 'g'
            ),
            '-+', '-', 'g'
        )
    );
END;
$$ language 'plpgsql' IMMUTABLE;

-- =============================================================================
-- ÍNDICES PADRÃO PARA PERFORMANCE
-- =============================================================================

-- Os índices específicos serão criados pelas migrações do Flask-Migrate
-- mas aqui definimos alguns índices básicos que sempre são úteis

-- Índices para timestamps (muito comum em queries)
-- Estes serão criados automaticamente quando as tabelas existirem

-- =============================================================================
-- CONFIGURAÇÕES DE BACKUP E MANUTENÇÃO
-- =============================================================================

-- Configurar autovacuum para manter performance
ALTER SYSTEM SET autovacuum_vacuum_scale_factor = 0.1;
ALTER SYSTEM SET autovacuum_analyze_scale_factor = 0.05;

-- =============================================================================
-- USUÁRIOS E ROLES ADICIONAIS (OPCIONAL)
-- =============================================================================

-- Criar role de leitura para relatórios (se necessário)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'apollo_readonly') THEN
        CREATE ROLE apollo_readonly;
        GRANT CONNECT ON DATABASE apollo_db TO apollo_readonly;
        GRANT USAGE ON SCHEMA apollo TO apollo_readonly;
        GRANT SELECT ON ALL TABLES IN SCHEMA apollo TO apollo_readonly;
        ALTER DEFAULT PRIVILEGES IN SCHEMA apollo 
            GRANT SELECT ON TABLES TO apollo_readonly;
    END IF;
END
$$;

-- =============================================================================
-- CONFIGURAÇÕES FINAIS
-- =============================================================================

-- Recarregar configurações (algumas só aplicam após restart)
SELECT pg_reload_conf();

-- Log de conclusão
DO $$
BEGIN
    RAISE NOTICE 'Apollo Project Orchestrator database initialized successfully!';
    RAISE NOTICE 'Database: apollo_db';
    RAISE NOTICE 'Schema: apollo';
    RAISE NOTICE 'User: apollo';
    RAISE NOTICE 'Extensions: uuid-ossp, pg_stat_statements, pgcrypto';
END
$$;