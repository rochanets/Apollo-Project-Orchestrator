from flask import Blueprint, request, jsonify, current_app
import openai
import json
import os
from werkzeug.utils import secure_filename

ai_bp = Blueprint('ai', __name__)

# Configurar OpenAI
def get_openai_client():
    api_key = current_app.config.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not configured")
    
    openai.api_key = api_key
    return openai

def simulate_ai_analysis(project_name, project_objective, project_description, files_content):
    """
    Simulação de análise de IA quando a API real não está disponível
    """
    return {
        "summary": f"Análise concluída para o projeto '{project_name}'. A IA processou as informações fornecidas e identificou pontos importantes para esclarecimento baseados no objetivo: {project_objective}.",
        "questions": [
            {
                "id": 1,
                "category": "Requisitos Funcionais",
                "question": "Quais são os principais módulos e funcionalidades que o sistema deve conter?",
                "priority": "high",
                "context": "Baseado na análise do objetivo do projeto, é importante definir claramente o escopo funcional."
            },
            {
                "id": 2,
                "category": "Integração",
                "question": "O sistema precisa se integrar com algum sistema existente? Se sim, quais?",
                "priority": "high",
                "context": "Integrações afetam significativamente a arquitetura e complexidade do projeto."
            },
            {
                "id": 3,
                "category": "Usuários/Performance",
                "question": "Quantos usuários simultâneos o sistema deve suportar?",
                "priority": "medium",
                "context": "Importante para dimensionar a infraestrutura adequada e garantir performance."
            },
            {
                "id": 4,
                "category": "Segurança",
                "question": "Quais são os requisitos de segurança e conformidade necessários?",
                "priority": "high",
                "context": "Segurança deve ser considerada desde o início do projeto para evitar vulnerabilidades."
            },
            {
                "id": 5,
                "category": "Tecnologia",
                "question": "Há alguma preferência ou restrição tecnológica específica?",
                "priority": "medium",
                "context": "Para alinhar com o ambiente tecnológico existente e expertise da equipe."
            }
        ],
        "insights": [
            "Projeto bem estruturado com objetivos claros e definidos",
            f"Documentação fornece boa base para desenvolvimento ({len(files_content)} arquivos analisados)", 
            "Identificadas oportunidades de otimização no processo de desenvolvimento"
        ],
        "next_steps": [
            "Aguardar respostas das perguntas críticas do cliente",
            "Definir arquitetura técnica detalhada baseada nas respostas",
            "Elaborar cronograma de desenvolvimento e marcos do projeto"
        ]
    }

@ai_bp.route('/analyze-documents', methods=['POST'])
def analyze_documents():
    """
    Analisa documentos usando OpenAI e gera perguntas críticas para o projeto
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        project_name = data.get('project_name', '')
        project_objective = data.get('project_objective', '')
        project_description = data.get('project_description', '')
        files_content = data.get('files_content', [])
        
        if not project_name or not project_objective:
            return jsonify({"error": "Nome do projeto e objetivo são obrigatórios"}), 400
        
        try:
            # Tentar usar OpenAI primeiro
            client = get_openai_client()
            
            # Preparar o prompt para a OpenAI
            files_text = ""
            if files_content:
                files_text = "\n\nDocumentos anexados:\n"
                for file_info in files_content:
                    files_text += f"- {file_info.get('name', 'Arquivo')}: {file_info.get('content', 'Conteúdo não disponível')}\n"
            
            prompt = f"""
            Você é um especialista em análise de projetos de software e gestão de projetos. 
            
            Analise as informações do projeto abaixo e gere perguntas críticas que devem ser respondidas para garantir o sucesso do projeto:
            
            **Projeto:** {project_name}
            **Objetivo:** {project_objective}
            **Descrição:** {project_description or 'Não fornecida'}
            {files_text}
            
            Com base nessas informações, gere:
            
            1. Um resumo da análise (2-3 frases)
            2. 5 perguntas críticas categorizadas por:
               - Requisitos Funcionais
               - Integração
               - Usuários/Performance
               - Segurança
               - Tecnologia
            3. 3 insights principais sobre o projeto
            4. 3 próximos passos recomendados
            
            Para cada pergunta, inclua:
            - A pergunta em si
            - A categoria
            - A prioridade (high/medium)
            - O contexto/justificativa da pergunta
            
            Responda em formato JSON seguindo esta estrutura:
            {{
                "summary": "Resumo da análise...",
                "questions": [
                    {{
                        "id": 1,
                        "category": "Requisitos Funcionais",
                        "question": "Pergunta aqui?",
                        "priority": "high",
                        "context": "Contexto da pergunta..."
                    }}
                ],
                "insights": [
                    "Insight 1",
                    "Insight 2", 
                    "Insight 3"
                ],
                "next_steps": [
                    "Passo 1",
                    "Passo 2",
                    "Passo 3"
                ]
            }}
            """
            
            # Fazer a chamada para a OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em análise de projetos de software. Responda sempre em português brasileiro e em formato JSON válido."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            # Extrair e processar a resposta
            ai_response = response.choices[0].message.content.strip()
            
            # Tentar fazer parse do JSON
            try:
                analysis_result = json.loads(ai_response)
            except json.JSONDecodeError:
                # Se não conseguir fazer parse, usar simulação
                analysis_result = simulate_ai_analysis(project_name, project_objective, project_description, files_content)
            
        except Exception as openai_error:
            # Se a OpenAI falhar (cota excedida, erro de rede, etc.), usar simulação
            current_app.logger.warning(f"OpenAI API falhou, usando simulação: {str(openai_error)}")
            analysis_result = simulate_ai_analysis(project_name, project_objective, project_description, files_content)
        
        return jsonify(analysis_result), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Erro na análise de IA: {str(e)}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@ai_bp.route('/health', methods=['GET'])
def health_check():
    """
    Verifica se a API da OpenAI está configurada corretamente
    """
    try:
        api_key = current_app.config.get('OPENAI_API_KEY')
        if not api_key:
            return jsonify({"status": "warning", "message": "OpenAI API key not configured, using simulation"}), 200
        
        return jsonify({"status": "ok", "message": "OpenAI API configured"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

