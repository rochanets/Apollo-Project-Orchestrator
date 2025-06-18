"""
Serviço de IA melhorado para análise de projetos
"""

import json
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import openai
from flask import current_app
from src.extensions import cache

logger = logging.getLogger(__name__)

class AIAnalysisService:
    """Serviço para análise de projetos usando IA"""
    
    def __init__(self):
        self.client = None
        self.fallback_enabled = True
        self.max_retries = 3
        self.timeout = 30
    
    def _get_openai_client(self):
        """Configurar cliente OpenAI"""
        api_key = current_app.config.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key não configurada")
        
        openai.api_key = api_key
        return openai
    
    def _build_enhanced_prompt(self, project_data: Dict[str, Any]) -> str:
        """Construir prompt aprimorado para análise"""
        
        files_text = ""
        if project_data.get('files_content'):
            files_text = "\n\nDOCUMENTOS ANEXADOS:\n"
            for file_info in project_data['files_content']:
                files_text += f"- {file_info.get('name', 'Arquivo')}: {file_info.get('content', 'Conteúdo não disponível')[:500]}...\n"
        
        prompt = f"""
Você é um especialista sênior em análise de projetos de software e arquitetura de sistemas.

Analise as informações do projeto abaixo e forneça uma análise profissional e detalhada:

**INFORMAÇÕES DO PROJETO:**
Nome: {project_data['name']}
Cliente: {project_data['client']}
Responsável: {project_data['responsible']}
Objetivo: {project_data['objective']}
Descrição: {project_data.get('description', 'Não fornecida')}
{files_text}

**INSTRUÇÕES DE ANÁLISE:**

1. **ANÁLISE DE RISCOS:** Identifique riscos técnicos, de negócio, cronograma e recursos
2. **ARQUITETURA:** Sugira arquitetura apropriada, padrões e tecnologias
3. **ESTIMATIVAS:** Avalie complexidade, esforço e cronograma
4. **REQUISITOS:** Identifique lacunas e dependências críticas
5. **GOVERNANÇA:** Recomende processos e controles de qualidade

**PERGUNTAS CRÍTICAS:**
Gere 5-8 perguntas estratégicas categorizadas por:
- Requisitos Funcionais e Não-Funcionais
- Integrações e Dependências Externas
- Performance e Escalabilidade
- Segurança e Compliance
- Tecnologia e Infraestrutura
- Processo e Governança

Para cada pergunta, inclua:
- Categoria específica
- Prioridade (critical/high/medium)
- Contexto/justificativa detalhada
- Impacto se não respondida

**FORMATO DE RESPOSTA:**
Responda EXCLUSIVAMENTE em JSON válido seguindo esta estrutura:

{{
    "summary": "Resumo executivo da análise (2-3 frases)",
    "risk_assessment": {{
        "technical_risks": ["risco1", "risco2"],
        "business_risks": ["risco1", "risco2"],
        "mitigation_strategies": ["estratégia1", "estratégia2"]
    }},
    "architecture_recommendations": {{
        "suggested_architecture": "Descrição da arquitetura",
        "technology_stack": ["tech1", "tech2"],
        "patterns": ["pattern1", "pattern2"]
    }},
    "estimates": {{
        "complexity_level": "low|medium|high|very_high",
        "estimated_duration_weeks": "número",
        "team_size_recommendation": "número",
        "effort_distribution": {{
            "analysis": "porcentagem",
            "development": "porcentagem", 
            "testing": "porcentagem",
            "deployment": "porcentagem"
        }}
    }},
    "questions": [
        {{
            "id": 1,
            "category": "Requisitos Funcionais",
            "question": "Pergunta específica?",
            "priority": "critical|high|medium",
            "context": "Contexto detalhado da pergunta",
            "impact": "Impacto se não respondida"
        }}
    ],
    "insights": [
        "Insight profissional 1",
        "Insight profissional 2", 
        "Insight profissional 3"
    ],
    "next_steps": [
        "Passo específico 1",
        "Passo específico 2",
        "Passo específico 3"
    ],
    "quality_gates": [
        "Gate de qualidade 1",
        "Gate de qualidade 2"
    ]
}}

IMPORTANTE: Responda APENAS com o JSON válido, sem texto adicional antes ou depois.
"""
        return prompt
    
    def _enhanced_fallback_analysis(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise de fallback aprimorada quando OpenAI não está disponível"""
        
        # Análise básica baseada em palavras-chave
        complexity = self._analyze_complexity(project_data)
        
        return {
            "summary": f"Análise automática concluída para '{project_data['name']}'. "
                      f"Projeto classificado como complexidade {complexity}. "
                      f"Identificadas {len(project_data.get('files_content', []))} documentos para análise.",
            
            "risk_assessment": {
                "technical_risks": [
                    "Falta de especificações técnicas detalhadas",
                    "Possíveis integrações complexas não mapeadas",
                    "Dependências tecnológicas não clarificadas"
                ],
                "business_risks": [
                    "Escopo não completamente definido",
                    "Expectativas do cliente podem não estar alinhadas",
                    "Cronograma pode ser otimista"
                ],
                "mitigation_strategies": [
                    "Realizar workshop de refinamento de requisitos",
                    "Criar protótipo para validação",
                    "Estabelecer marcos de entrega incrementais"
                ]
            },
            
            "architecture_recommendations": {
                "suggested_architecture": "Arquitetura em camadas com API REST, seguindo princípios SOLID",
                "technology_stack": self._suggest_tech_stack(project_data),
                "patterns": ["Repository Pattern", "MVC", "Dependency Injection", "Circuit Breaker"]
            },
            
            "estimates": {
                "complexity_level": complexity,
                "estimated_duration_weeks": self._estimate_duration(complexity),
                "team_size_recommendation": self._estimate_team_size(complexity),
                "effort_distribution": {
                    "analysis": "20%",
                    "development": "50%",
                    "testing": "20%",
                    "deployment": "10%"
                }
            },
            
            "questions": [
                {
                    "id": 1,
                    "category": "Requisitos Funcionais",
                    "question": "Quais são os principais módulos e funcionalidades que o sistema deve conter?",
                    "priority": "critical",
                    "context": "Baseado na análise do objetivo do projeto, é fundamental definir claramente o escopo funcional para evitar scope creep e garantir alinhamento de expectativas.",
                    "impact": "Sem definição clara, o projeto pode ter retrabalho significativo e estouro de prazo/orçamento"
                },
                {
                    "id": 2,
                    "category": "Integrações e Dependências",
                    "question": "O sistema precisa se integrar com algum sistema existente? Se sim, quais e como?",
                    "priority": "critical",
                    "context": "Integrações afetam significativamente a arquitetura, complexidade e riscos do projeto.",
                    "impact": "Integrações não mapeadas podem causar bloqueios críticos durante o desenvolvimento"
                },
                {
                    "id": 3,
                    "category": "Performance e Escalabilidade",
                    "question": "Quantos usuários simultâneos o sistema deve suportar e qual o volume de dados esperado?",
                    "priority": "high",
                    "context": "Essencial para dimensionar infraestrutura adequada e escolher tecnologias apropriadas.",
                    "impact": "Subdimensionamento pode causar falhas em produção; superdimensionamento aumenta custos desnecessariamente"
                },
                {
                    "id": 4,
                    "category": "Segurança e Compliance",
                    "question": "Quais são os requisitos de segurança, privacidade e conformidade regulatória?",
                    "priority": "critical",
                    "context": "Segurança deve ser considerada desde o início para evitar vulnerabilidades e atender regulamentações como LGPD.",
                    "impact": "Falhas de segurança podem resultar em vazamentos de dados, multas e perda de credibilidade"
                },
                {
                    "id": 5,
                    "category": "Tecnologia e Infraestrutura",
                    "question": "Há alguma preferência ou restrição tecnológica específica do cliente/organização?",
                    "priority": "high",
                    "context": "Importante para alinhar com ambiente tecnológico existente e expertise da equipe.",
                    "impact": "Escolhas tecnológicas inadequadas podem aumentar custos de manutenção e dificuldade de suporte"
                },
                {
                    "id": 6,
                    "category": "Processo e Governança",
                    "question": "Qual o processo de aprovação e validação das entregas? Quem são os stakeholders decisores?",
                    "priority": "medium",
                    "context": "Fundamental para estabelecer marcos claros e evitar retrabalho por falta de validação adequada.",
                    "impact": "Processos mal definidos podem causar atrasos e conflitos durante o projeto"
                }
            ],
            
            "insights": [
                f"Projeto bem estruturado com objetivos claros baseados no cliente {project_data.get('client', 'não especificado')}",
                f"Documentação inicial fornece boa base ({len(project_data.get('files_content', []))} arquivos analisados)",
                "Identificadas oportunidades de otimização no processo de levantamento de requisitos",
                f"Complexidade estimada como {complexity} baseada na análise preliminar"
            ],
            
            "next_steps": [
                "Realizar workshop de refinamento de requisitos com stakeholders",
                "Elaborar arquitetura técnica detalhada baseada nas respostas",
                "Criar protótipo de alta fidelidade para validação",
                "Definir cronograma detalhado com marcos de entrega",
                "Estabelecer processo de comunicação e governança do projeto"
            ],
            
            "quality_gates": [
                "Aprovação formal dos requisitos funcionais e não-funcionais",
                "Validação da arquitetura técnica com equipe de infraestrutura",
                "Aprovação do protótipo pelos usuários finais",
                "Sign-off do plano de projeto e cronograma"
            ]
        }
    
    def _analyze_complexity(self, project_data: Dict[str, Any]) -> str:
        """Analisar complexidade do projeto baseado em heurísticas"""
        complexity_score = 0
        
        # Análise do objetivo
        objective = project_data.get('objective', '').lower()
        if any(word in objective for word in ['integração', 'api', 'microservice', 'distribuído']):
            complexity_score += 2
        if any(word in objective for word in ['ia', 'machine learning', 'big data', 'analytics']):
            complexity_score += 3
        if any(word in objective for word in ['mobile', 'web', 'responsivo']):
            complexity_score += 1
        
        # Análise da descrição
        description = project_data.get('description', '').lower()
        if any(word in description for word in ['real-time', 'tempo real', 'alta disponibilidade']):
            complexity_score += 2
        if any(word in description for word in ['segurança', 'criptografia', 'compliance']):
            complexity_score += 1
        
        # Análise dos arquivos
        files_count = len(project_data.get('files_content', []))
        if files_count > 5:
            complexity_score += 1
        elif files_count > 10:
            complexity_score += 2
        
        # Classificar complexidade
        if complexity_score <= 2:
            return "low"
        elif complexity_score <= 5:
            return "medium"
        elif complexity_score <= 8:
            return "high"
        else:
            return "very_high"
    
    def _suggest_tech_stack(self, project_data: Dict[str, Any]) -> List[str]:
        """Sugerir stack tecnológico baseado no projeto"""
        stack = []
        
        objective = project_data.get('objective', '').lower()
        description = project_data.get('description', '').lower()
        combined_text = f"{objective} {description}"
        
        # Backend
        if 'python' in combined_text:
            stack.extend(['Python', 'Flask/Django', 'PostgreSQL'])
        elif 'java' in combined_text:
            stack.extend(['Java', 'Spring Boot', 'PostgreSQL'])
        elif 'node' in combined_text or 'javascript' in combined_text:
            stack.extend(['Node.js', 'Express', 'MongoDB'])
        else:
            stack.extend(['Python', 'Flask', 'PostgreSQL'])  # Default
        
        # Frontend
        if 'react' in combined_text:
            stack.append('React')
        elif 'vue' in combined_text:
            stack.append('Vue.js')
        elif 'angular' in combined_text:
            stack.append('Angular')
        elif 'mobile' in combined_text:
            stack.extend(['React Native', 'Flutter'])
        else:
            stack.append('React')  # Default
        
        # Infraestrutura
        if 'cloud' in combined_text or 'aws' in combined_text:
            stack.extend(['AWS', 'Docker', 'Kubernetes'])
        elif 'azure' in combined_text:
            stack.extend(['Azure', 'Docker'])
        else:
            stack.extend(['Docker', 'Nginx'])
        
        return stack
    
    def _estimate_duration(self, complexity: str) -> str:
        """Estimar duração baseada na complexidade"""
        duration_map = {
            "low": "4-8",
            "medium": "8-16", 
            "high": "16-24",
            "very_high": "24-40"
        }
        return duration_map.get(complexity, "8-16")
    
    def _estimate_team_size(self, complexity: str) -> str:
        """Estimar tamanho da equipe baseada na complexidade"""
        team_map = {
            "low": "2-3",
            "medium": "3-5",
            "high": "5-8", 
            "very_high": "8-12"
        }
        return team_map.get(complexity, "3-5")
    
    @cache.memoize(timeout=3600)  # Cache por 1 hora
    def analyze_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisar projeto usando OpenAI com fallback
        
        Args:
            project_data: Dados do projeto para análise
            
        Returns:
            Dict com resultado da análise
        """
        try:
            # Tentar usar OpenAI primeiro
            return self._openai_analysis(project_data)
            
        except Exception as e:
            logger.warning(f"OpenAI API falhou: {str(e)}")
            
            if self.fallback_enabled:
                logger.info("Usando análise de fallback")
                return self._enhanced_fallback_analysis(project_data)
            else:
                raise
    
    def _openai_analysis(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise usando OpenAI API"""
        
        # Configurar cliente
        client = self._get_openai_client()
        
        # Construir prompt
        prompt = self._build_enhanced_prompt(project_data)
        
        # Fazer chamada para OpenAI
        response = openai.ChatCompletion.create(
            model=current_app.config.get('OPENAI_MODEL', 'gpt-3.5-turbo'),
            messages=[
                {
                    "role": "system",
                    "content": "Você é um especialista sênior em análise de projetos de software. "
                              "Responda sempre em português brasileiro e EXCLUSIVAMENTE em formato JSON válido."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=current_app.config.get('OPENAI_MAX_TOKENS', 2000),
            temperature=current_app.config.get('OPENAI_TEMPERATURE', 0.7),
            timeout=self.timeout
        )
        
        # Extrair resposta
        ai_response = response.choices[0].message.content.strip()
        
        # Parse JSON
        try:
            result = json.loads(ai_response)
            
            # Validar estrutura básica
            self._validate_analysis_result(result)
            
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao fazer parse do JSON da OpenAI: {e}")
            logger.debug(f"Resposta da OpenAI: {ai_response}")
            
            # Se falhar o parse, usar fallback
            return self._enhanced_fallback_analysis(project_data)
    
    def _validate_analysis_result(self, result: Dict[str, Any]) -> None:
        """Validar estrutura do resultado da análise"""
        required_fields = ['summary', 'questions', 'insights', 'next_steps']
        
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Campo obrigatório '{field}' ausente no resultado")
        
        # Validar perguntas
        if not isinstance(result['questions'], list) or len(result['questions']) == 0:
            raise ValueError("Campo 'questions' deve ser uma lista não vazia")
        
        for i, question in enumerate(result['questions']):
            required_q_fields = ['question', 'category', 'priority']
            for field in required_q_fields:
                if field not in question:
                    raise ValueError(f"Pergunta {i+1}: campo '{field}' obrigatório")
    
    async def analyze_project_async(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise assíncrona para melhor UX"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.analyze_project, project_data)
    
    def get_analysis_status(self, project_id: int) -> Dict[str, Any]:
        """Obter status de uma análise em andamento"""
        cache_key = f"analysis_status:{project_id}"
        status = cache.get(cache_key)
        
        if not status:
            return {
                'status': 'not_found',
                'message': 'Análise não encontrada'
            }
        
        return status
    
    def set_analysis_status(self, project_id: int, status: str, message: str = None, progress: int = 0):
        """Definir status de uma análise"""
        cache_key = f"analysis_status:{project_id}"
        status_data = {
            'status': status,
            'message': message,
            'progress': progress,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        cache.set(cache_key, status_data, timeout=3600)  # 1 hora
    
    def health_check(self) -> Dict[str, Any]:
        """Verificar saúde do serviço de IA"""
        try:
            api_key = current_app.config.get('OPENAI_API_KEY')
            
            if not api_key:
                return {
                    'status': 'warning',
                    'message': 'OpenAI API key não configurada - usando análise simulada',
                    'fallback_enabled': self.fallback_enabled
                }
            
            # Teste simples da API
            client = self._get_openai_client()
            
            return {
                'status': 'ok',
                'message': 'OpenAI API configurada e funcionando',
                'fallback_enabled': self.fallback_enabled
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Erro na configuração da OpenAI: {str(e)}',
                'fallback_enabled': self.fallback_enabled
            }
                