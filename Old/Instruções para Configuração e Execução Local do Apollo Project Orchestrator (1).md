# Instruções para Configuração e Execução Local do Apollo Project Orchestrator (Atualizado)

Este documento contém as instruções detalhadas para configurar e executar o projeto Apollo Project Orchestrator (Frontend e Backend) em sua máquina local.

## Pré-requisitos

Certifique-se de ter os seguintes softwares instalados em sua máquina:

*   **Node.js e npm (ou pnpm):** Para o Frontend (React).
    *   Recomendado: [Node.js LTS](https://nodejs.org/en/download/)
    *   Instale pnpm: `npm install -g pnpm`
*   **Python 3.9+ e pip:** Para o Backend (Flask).
    *   Recomendado: [Python.org](https://www.python.org/downloads/)
*   **Git:** Para clonar o repositório (opcional, se você já baixou os arquivos).
    *   [Git-SCM](https://git-scm.com/downloads)

## Estrutura do Projeto

Após descompactar os arquivos, você terá duas pastas principais:

*   `apollo-project-orchestrator`: Contém o código-fonte do Frontend (React).
*   `apollo-backend`: Contém o código-fonte do Backend (Flask).

Recomenda-se colocar ambas as pastas dentro de `C:\Users\hfnetto\OneDrive - Stefanini\Documents\GitHub`.

```
C:\Users\hfnetto\OneDrive - Stefanini\Documents\GitHub
├── apollo-project-orchestrator
└── apollo-backend
```

## Configuração e Execução do Backend (Flask)

1.  **Navegue até a pasta do Backend:**

    ```powershell
    cd C:\Users\hfnetto\OneDrive - Stefanini\Documents\GitHub\apollo-backend
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**

    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**

    ```powershell
    pip install -r requirements.txt
    ```

    *Nota: O arquivo `requirements.txt` foi gerado automaticamente e contém todas as dependências necessárias.* 

4.  **Configure as variáveis de ambiente:**

    Crie um arquivo `.env` na raiz da pasta `apollo-backend` com o seguinte conteúdo:

    ```dotenv
    SECRET_KEY=sua_chave_secreta_aqui
    JWT_SECRET_KEY=sua_chave_jwt_secreta_aqui
    ```

    *Substitua `sua_chave_secreta_aqui` e `sua_chave_jwt_secreta_aqui` por valores aleatórios e seguros. Você pode gerar chaves aleatórias online ou usar um gerador de senhas.* 

5.  **Inicialize e aplique as migrações do banco de dados:**

    *   **Crie o diretório do banco de dados (se não existir):**

        ```powershell
        New-Item -ItemType Directory -Force -Path .\src\database
        ```

    *   **Remova o banco de dados existente (se houver):**

        ```powershell
        Remove-Item -Path .\src\database\apollo.db -ErrorAction SilentlyContinue
        ```
        *Se o arquivo não existir, o comando não retornará erro. Isso é esperado.* 

    *   **Remova o diretório de migrações (se houver):**

        ```powershell
        Remove-Item -Path .\migrations -Recurse -Force -ErrorAction SilentlyContinue
        ```
        *Se o diretório não existir, o comando não retornará erro. Isso é esperado.* 

    *   **Inicialize o Flask-Migrate:**

        ```powershell
        $env:FLASK_APP = "src/main.py"
        $env:FLASK_DEBUG = "1"
        flask db init
        ```

    *   **Crie a migração inicial:**

        ```powershell
        flask db migrate -m "Initial migration with final corrected relationships"
        ```

    *   **Aplique as migrações:**

        ```powershell
        flask db upgrade
        ```

6.  **Insira o usuário no banco de dados (opcional, se você não conseguir cadastrar via interface):**

    *   Crie um arquivo chamado `insert_user.py` na raiz da pasta `apollo-backend` com o seguinte conteúdo:

        ```python
        from src.models.database import db, User
        from src.main import app
        from werkzeug.security import generate_password_hash

        with app.app_context():
            # Verificar se o usuário já existe para evitar duplicidade
            existing_user = User.query.filter_by(email=\'hfnetto@stefanini.om\').first()
            if not existing_user:
                user = User(
                    name=\'hfnetto\',
                    email=\'hfnetto@stefanini.om\',
                    password_hash=generate_password_hash(\'teste123\')
                )
                db.session.add(user)
                db.session.commit()
                print(\'Usuário hfnetto@stefanini.om adicionado com sucesso.\')
            else:
                print(\'Usuário hfnetto@stefanini.om já existe no banco de dados.\')
        ```

    *   Execute o script:

        ```powershell
        python insert_user.py
        ```

7.  **Inicie o servidor Backend:**

    ```powershell
    flask run --host=0.0.0.0 --port=5000
    ```

    O backend estará acessível em `http://localhost:5000`.

## Configuração e Execução do Frontend (React)

1.  **Navegue até a pasta do Frontend:**

    ```powershell
    cd C:\Users\hfnetto\OneDrive - Stefanini\Documents\GitHub\apollo-project-orchestrator
    ```

2.  **Instale as dependências:**

    ```powershell
    pnpm install
    ```

3.  **Configure a URL da API:**

    Abra o arquivo `src/services/api.js` e certifique-se de que a `API_BASE_URL` esteja apontando para o seu backend local:

    ```javascript
    // Configuração da API
    const API_BASE_URL = \'http://localhost:5000/api\';
    ```

4.  **Inicie o servidor Frontend:**

    ```powershell
    pnpm run dev --host
    ```

    O frontend estará acessível em `http://localhost:5173` (ou outra porta disponível, que será exibida no terminal).

## Testando a Aplicação

1.  Certifique-se de que tanto o Backend quanto o Frontend estejam rodando.
2.  Abra seu navegador e acesse a URL do Frontend (ex: `http://localhost:5173`).
3.  Você poderá usar o email `hfnetto@stefanini.om` e a senha `teste123` para fazer login (se você executou o passo 6 do Backend).

Se tiver qualquer problema durante a configuração, por favor, me informe!


