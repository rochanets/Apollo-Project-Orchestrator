# Apollo Project Orchestrator - Backend

## Descrição
Backend da aplicação Apollo Project Orchestrator desenvolvido em Flask com integração OpenAI.

## Funcionalidades
- API RESTful para gestão de projetos
- Integração com OpenAI para análise de documentos
- Sistema de autenticação JWT
- Upload e processamento de arquivos
- Análise de IA com fallback para simulação

## Estrutura
```
src/
├── main.py              # Arquivo principal da aplicação
├── models/
│   └── database.py      # Modelos de dados
└── routes/
    ├── auth.py          # Rotas de autenticação
    ├── projects.py      # Rotas de projetos
    ├── users.py         # Rotas de usuários
    └── ai.py            # Rotas de IA
```

## Instalação
1. Instalar dependências: `pip install -r requirements.txt`
2. Configurar variáveis de ambiente no arquivo `.env`
3. Executar: `python src/main.py`

## Configuração
Edite o arquivo `.env` com suas configurações:
- `OPENAI_API_KEY`: Sua chave da OpenAI
- `SECRET_KEY`: Chave secreta para JWT
- `DATABASE_URL`: URL do banco de dados

## API Endpoints
- `POST /api/auth/login` - Login de usuário
- `GET /api/projects` - Listar projetos
- `POST /api/projects` - Criar projeto
- `POST /api/ai/analyze` - Análise de IA

