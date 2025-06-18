import React, { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Progress } from '@/components/ui/progress.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import { Alert, AlertDescription } from '@/components/ui/alert.jsx';
import { 
  CheckCircle, 
  Circle, 
  FolderOpen, 
  Plus, 
  Settings,
  User,
  FileText,
  Upload,
  MessageSquare,
  Database,
  Code,
  TestTube,
  Rocket,
  Trash2,
  Edit,
  Calendar,
  Clock,
  ArrowLeft,
  FileUp,
  X,
  Brain,
  Loader2
} from 'lucide-react';
import apolloLogo from './assets/apollo-logo.png';
import CreateProjectModal from './components/CreateProjectModal.jsx';
import { ApiService } from './services/api.js';
import './App.css';

// Dados das etapas do projeto
const projectSteps = [
  { id: 0, title: 'Cadastro do Projeto', icon: FileText, description: 'Informações básicas do projeto' },
  { id: 1, title: 'Upload de Documentos', icon: Upload, description: 'Anexar documentação do projeto' },
  { id: 2, title: 'Geração de Perguntas', icon: MessageSquare, description: 'IA gera perguntas críticas' },
  { id: 3, title: 'Coleta de Informações', icon: Database, description: 'Documentação e esclarecimentos' },
  { id: 4, title: 'Análise Técnica', icon: Settings, description: 'Levantamento do ambiente' },
  { id: 5, title: 'Execução do Projeto', icon: Code, description: 'Desenvolvimento automatizado' },
  { id: 6, title: 'Testes', icon: TestTube, description: 'Testes integrados e correções' },
  { id: 7, title: 'Go Live', icon: Rocket, description: 'Documentação final e deploy' }
];

// Dados de exemplo para projetos (simulando dados do backend)
const initialMockProjects = [
  {
    id: 1,
    name: 'Sistema de Gestão Comercial',
    client: 'Empresa ABC',
    responsible: 'João Silva',
    objective: 'Desenvolver sistema para gestão de vendas e estoque',
    description: 'Sistema completo para controle de vendas, estoque e relatórios gerenciais',
    status: 'active',
    priority: 'high',
    current_step: 2,
    start_date: '2024-01-15',
    deadline: '2024-06-15',
    created_at: '2024-01-15T10:00:00Z',
    uploaded_files: [
      {
        id: 1,
        name: 'Requisitos_Sistema_Gestao.pdf',
        size: 2048576,
        type: 'application/pdf',
        uploadDate: '2024-01-15T10:30:00Z'
      },
      {
        id: 2,
        name: 'Especificacoes_Tecnicas.docx',
        size: 1024000,
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        uploadDate: '2024-01-15T11:00:00Z'
      }
    ],
    ai_questions: [],
    ai_analysis: null
  },
  {
    id: 2,
    name: 'Portal do Cliente',
    client: 'Empresa XYZ',
    responsible: 'Maria Santos',
    objective: 'Portal web para autoatendimento de clientes',
    description: 'Plataforma online para que clientes possam acessar informações e serviços',
    status: 'active',
    priority: 'medium',
    current_step: 4,
    start_date: '2024-01-10',
    deadline: '2024-05-10',
    created_at: '2024-01-10T14:30:00Z',
    uploaded_files: [
      {
        id: 3,
        name: 'Wireframes_Portal.pdf',
        size: 3072000,
        type: 'application/pdf',
        uploadDate: '2024-01-10T15:00:00Z'
      }
    ],
    ai_questions: [],
    ai_analysis: null
  }
];

// Simulação de IA para análise de documentos
const simulateAIAnalysis = async (files, projectData) => {
  // Simular delay de processamento
  await new Promise(resolve => setTimeout(resolve, 3000));
  
  // Gerar perguntas baseadas no tipo de projeto e documentos
  const questions = [
    {
      id: 1,
      category: 'Requisitos Funcionais',
      question: 'Quais são os principais módulos que o sistema deve conter?',
      priority: 'high',
      context: 'Baseado na análise dos documentos, identifiquei a necessidade de definir melhor a arquitetura modular.'
    },
    {
      id: 2,
      category: 'Integração',
      question: 'O sistema precisa se integrar com algum sistema existente? Se sim, quais?',
      priority: 'high',
      context: 'Para garantir a compatibilidade e fluxo de dados adequado.'
    },
    {
      id: 3,
      category: 'Usuários',
      question: 'Quantos usuários simultâneos o sistema deve suportar?',
      priority: 'medium',
      context: 'Importante para dimensionar a infraestrutura adequada.'
    },
    {
      id: 4,
      category: 'Segurança',
      question: 'Quais são os requisitos de segurança e conformidade necessários?',
      priority: 'high',
      context: 'Considerando as melhores práticas de segurança para sistemas comerciais.'
    },
    {
      id: 5,
      category: 'Tecnologia',
      question: 'Há alguma preferência ou restrição tecnológica específica?',
      priority: 'medium',
      context: 'Para alinhar com o ambiente tecnológico existente da empresa.'
    }
  ];

  return {
    summary: `Análise concluída para o projeto "${projectData.name}". Foram identificados ${files.length} documentos relevantes que fornecem informações sobre requisitos, escopo e objetivos do projeto.`,
    questions: questions,
    insights: [
      'Projeto bem estruturado com objetivos claros',
      'Documentação fornece boa base para desenvolvimento',
      'Identificadas oportunidades de otimização no processo'
    ],
    next_steps: [
      'Aguardar respostas das perguntas críticas',
      'Definir arquitetura técnica detalhada',
      'Elaborar cronograma de desenvolvimento'
    ]
  };
};

function App() {
  // Sistema de logs para debug
  const logStateChange = (action, oldValue, newValue, source) => {
    const logData = {
      action,
      oldValue,
      newValue,
      source,
      timestamp: new Date().toISOString(),
      currentStepRef: currentStepRef.current,
      isProcessing: isProcessingRef.current,
      stepLocked: stepLockRef.current,
      stack: new Error().stack
    };
    
    console.log(`🔍 [DEBUG] ${action}:`, logData);
    
    // Em produção, também enviar logs para um serviço de monitoramento
    if (window.location.hostname !== 'localhost') {
      // Logs mais detalhados para produção
      console.log(`🌐 [PRODUCTION] ${action}:`, {
        ...logData,
        userAgent: navigator.userAgent,
        url: window.location.href,
        selectedProjectId: selectedProject?.id,
        projectsCount: projects.length
      });
    }
  };

  // Refs para controle rigoroso de estado
  const currentStepRef = useRef(initialMockProjects[0]?.current_step || 0);
  const isProcessingRef = useRef(false);
  const stepLockRef = useRef(false);

  const [projects, setProjects] = useState(initialMockProjects);
  const [selectedProject, setSelectedProject] = useState(initialMockProjects[0]);
  const [currentStep, setCurrentStep] = useState(() => {
    const initialStep = initialMockProjects[0]?.current_step || 0;
    currentStepRef.current = initialStep;
    logStateChange('INITIAL_CURRENT_STEP', null, initialStep, 'useState initialization');
    return initialStep;
  });
  const [error, setError] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [isAIProcessing, setIsAIProcessing] = useState(false);
  const [aiResults, setAiResults] = useState(null);

  // Wrapper para setCurrentStep com logs e proteção
  const setCurrentStepWithLog = (newStep, source = 'unknown') => {
    // Verificar se há um lock ativo
    if (stepLockRef.current && source !== 'manual_navigation') {
      logStateChange('STEP_CHANGE_BLOCKED', currentStep, newStep, `${source} - blocked by lock`);
      return false;
    }

    const oldStep = currentStep;
    logStateChange('CURRENT_STEP_CHANGE', oldStep, newStep, source);
    currentStepRef.current = newStep;
    setCurrentStep(newStep);
    return true;
  };

  // Função para bloquear mudanças de etapa
  const lockStepChanges = (reason) => {
    stepLockRef.current = true;
    logStateChange('STEP_LOCK_ACTIVATED', false, true, reason);
  };

  // Função para desbloquear mudanças de etapa
  const unlockStepChanges = (reason) => {
    stepLockRef.current = false;
    logStateChange('STEP_LOCK_DEACTIVATED', true, false, reason);
  };

  // Atualizar currentStep quando selectedProject mudar APENAS na inicialização
  useEffect(() => {
    logStateChange('USEEFFECT_TRIGGERED', 'selectedProject change', selectedProject?.id, 'useEffect dependency');
    
    // PROTEÇÃO ADICIONAL: Não executar se há processamento ativo
    if (isProcessingRef.current) {
      logStateChange('USEEFFECT_BLOCKED', 'blocked due to active processing', selectedProject?.id, 'useEffect protection');
      return;
    }

    if (selectedProject) {
      // IMPORTANTE: NÃO atualizar currentStep automaticamente
      // Isso estava causando o avanço automático de etapa
      setUploadedFiles(selectedProject.uploaded_files || []);
      setAiResults(selectedProject.ai_analysis);
      logStateChange('USEEFFECT_COMPLETED', 'files and ai results updated WITHOUT changing currentStep', null, 'useEffect execution');
    }
  }, [selectedProject?.id]); // Mudança: usar selectedProject.id ao invés de selectedProject completo

  // useEffect adicional para monitorar mudanças inesperadas de currentStep
  useEffect(() => {
    // Sincronizar ref com state
    currentStepRef.current = currentStep;
    logStateChange('CURRENT_STEP_SYNC', 'syncing ref with state', currentStep, 'useEffect sync');
  }, [currentStep]);

  const handleProjectCreated = (projectData, isEditing = false) => {
    if (isEditing) {
      // Atualizar projeto existente
      const updatedProjects = projects.map(p => 
        p.id === projectData.id ? projectData : p
      );
      setProjects(updatedProjects);
      
      if (selectedProject && selectedProject.id === projectData.id) {
        setSelectedProject(projectData);
      }
    } else {
      // Criar novo projeto
      const newProject = {
        ...projectData,
        id: Date.now(),
        current_step: 0,
        uploaded_files: [],
        ai_questions: [],
        ai_analysis: null
      };
      
      const updatedProjects = [...projects, newProject];
      setProjects(updatedProjects);
      setSelectedProject(newProject);
    }
    
    setShowCreateModal(false);
    setEditingProject(null);
  };

  const handleDeleteProject = (projectId) => {
    if (window.confirm('Tem certeza que deseja excluir este projeto? Esta ação não pode ser desfeita.')) {
      const updatedProjects = projects.filter(p => p.id !== projectId);
      setProjects(updatedProjects);
      
      if (selectedProject && selectedProject.id === projectId) {
        setSelectedProject(updatedProjects[0] || null);
      }
    }
  };

  const handleEditProject = (project) => {
    setEditingProject(project);
    setShowCreateModal(true);
  };

  const handleStepChange = (newStep) => {
    logStateChange('HANDLE_STEP_CHANGE_CALLED', currentStep, newStep, 'handleStepChange function');
    
    // Verificar se há um lock ativo
    if (stepLockRef.current) {
      logStateChange('STEP_CHANGE_BLOCKED_BY_LOCK', currentStep, newStep, 'handleStepChange - blocked by lock');
      return;
    }

    if (newStep < currentStep) {
      // Confirmação para voltar etapas
      if (window.confirm('Tem certeza que deseja voltar para uma etapa anterior? Isso pode afetar o progresso do projeto.')) {
        setCurrentStepWithLog(newStep, 'manual_navigation');
        updateProjectStep(newStep);
      }
    } else {
      setCurrentStepWithLog(newStep, 'manual_navigation');
      updateProjectStep(newStep);
    }
  };

  const updateProjectStep = (step) => {
    logStateChange('UPDATE_PROJECT_STEP_CALLED', selectedProject?.current_step, step, 'updateProjectStep function');
    if (selectedProject) {
      const updatedProject = { ...selectedProject, current_step: step };
      const updatedProjects = projects.map(p => 
        p.id === selectedProject.id ? updatedProject : p
      );
      setProjects(updatedProjects);
      setSelectedProject(updatedProject);
      logStateChange('UPDATE_PROJECT_STEP_COMPLETED', 'project updated', step, 'updateProjectStep completion');
    }
  };

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    const newFiles = files.map(file => ({
      id: Date.now() + Math.random(),
      name: file.name,
      size: file.size,
      type: file.type,
      uploadDate: new Date().toISOString(),
      file: file
    }));

    const updatedFiles = [...uploadedFiles, ...newFiles];
    setUploadedFiles(updatedFiles);

    // Atualizar projeto
    if (selectedProject) {
      const updatedProject = { ...selectedProject, uploaded_files: updatedFiles };
      const updatedProjects = projects.map(p => 
        p.id === selectedProject.id ? updatedProject : p
      );
      setProjects(updatedProjects);
      setSelectedProject(updatedProject);
    }
  };

  const handleRemoveFile = (fileId) => {
    const updatedFiles = uploadedFiles.filter(f => f.id !== fileId);
    setUploadedFiles(updatedFiles);

    // Atualizar projeto
    if (selectedProject) {
      const updatedProject = { ...selectedProject, uploaded_files: updatedFiles };
      const updatedProjects = projects.map(p => 
        p.id === selectedProject.id ? updatedProject : p
      );
      setProjects(updatedProjects);
      setSelectedProject(updatedProject);
    }
  };

  const handleAIAnalysis = async () => {
    logStateChange('HANDLE_AI_ANALYSIS_STARTED', 'AI analysis initiated', currentStep, 'handleAIAnalysis start');
    
    if (uploadedFiles.length === 0) {
      setError('Por favor, faça upload de pelo menos um documento antes de solicitar a análise da IA.');
      return;
    }

    // BLOQUEAR mudanças de etapa durante o processamento
    lockStepChanges('AI analysis in progress');
    
    setIsAIProcessing(true);
    setError('');
    isProcessingRef.current = true;

    try {
      // IMPORTANTE: Salvar currentStep atual para garantir que não mude
      const currentStepBeforeAnalysis = currentStepRef.current;
      logStateChange('CURRENT_STEP_SAVED', 'saving current step before analysis', currentStepBeforeAnalysis, 'step protection');

      // Usar simulação local diretamente para evitar problemas de API
      logStateChange('AI_SIMULATION_STARTED', 'using local simulation', null, 'simulation fallback');
      
      const analysis = await simulateAIAnalysis(uploadedFiles, {
        project_name: selectedProject.name,
        project_objective: selectedProject.objective,
        project_description: selectedProject.description || ''
      });

      logStateChange('AI_SIMULATION_SUCCESS', 'simulation completed', analysis, 'simulation response');
      setAiResults(analysis);

      // Atualizar projeto com resultados da IA (SEM alterar current_step)
      if (selectedProject) {
        logStateChange('AI_PROJECT_UPDATE_START', 'updating project with AI results', selectedProject.current_step, 'project update');
        
        const updatedProject = { 
          ...selectedProject, 
          ai_analysis: analysis,
          ai_questions: analysis.questions,
          // GARANTIR que current_step não mude
          current_step: currentStepBeforeAnalysis
        };
        
        // Atualizar apenas o array de projetos, sem alterar selectedProject
        const updatedProjects = projects.map(p => 
          p.id === selectedProject.id ? updatedProject : p
        );
        setProjects(updatedProjects);
        
        logStateChange('AI_PROJECT_UPDATE_COMPLETE', 'project updated without changing selectedProject', updatedProject.current_step, 'project update complete');
        
        // VERIFICAÇÃO ADICIONAL: Garantir que currentStep não mudou
        if (currentStepRef.current !== currentStepBeforeAnalysis) {
          logStateChange('STEP_CHANGE_DETECTED', 'unexpected step change detected, reverting', currentStepRef.current, 'step protection');
          setCurrentStepWithLog(currentStepBeforeAnalysis, 'step protection - reverting unexpected change');
        }
      }

      // DELAY adicional para garantir que tudo foi processado
      await new Promise(resolve => setTimeout(resolve, 500));
      
      logStateChange('AI_ANALYSIS_COMPLETE', 'analysis completed successfully', currentStepRef.current, 'completion');

    } catch (error) {
      console.error('Erro na análise da IA:', error);
      setError(`Erro ao processar análise da IA: ${error.message}`);
      logStateChange('AI_ANALYSIS_ERROR', 'error occurred', error.message, 'error handling');
    } finally {
      setIsAIProcessing(false);
      isProcessingRef.current = false;
      
      // DESBLOQUEAR mudanças de etapa após delay adicional
      setTimeout(() => {
        unlockStepChanges('AI analysis completed');
        logStateChange('HANDLE_AI_ANALYSIS_FINISHED', 'AI analysis completed', currentStepRef.current, 'handleAIAnalysis end');
      }, 1000);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Não definido';
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const getDaysUntilDeadline = (deadline) => {
    if (!deadline) return null;
    const today = new Date();
    const deadlineDate = new Date(deadline);
    const diffTime = deadlineDate - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getPriorityLabel = (priority) => {
    switch (priority) {
      case 'urgent': return 'Urgente';
      case 'high': return 'Alta';
      case 'medium': return 'Média';
      case 'low': return 'Baixa';
      default: return 'Não definida';
    }
  };

  const renderStepContent = () => {
    const step = projectSteps[currentStep];
    
    switch (currentStep) {
      case 0:
        return (
          <div className="space-y-6">
            <div className="flex items-center space-x-3">
              <FileText className="h-8 w-8 text-orange-500" />
              <div>
                <h3 className="text-xl font-semibold text-gray-900">Cadastro do Projeto</h3>
                <p className="text-gray-600">Informações básicas do projeto foram definidas</p>
              </div>
            </div>
            
            {selectedProject && (
              <div className="bg-white p-4 rounded-lg border border-gray-200 max-w-4xl">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Nome do Projeto</label>
                    <p className="text-sm text-gray-900 mt-1">{selectedProject.name}</p>
                  </div>
                  <div>
                    <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Cliente</label>
                    <p className="text-sm text-gray-900 mt-1">{selectedProject.client}</p>
                  </div>
                  <div>
                    <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Responsável</label>
                    <p className="text-sm text-gray-900 mt-1">{selectedProject.responsible}</p>
                  </div>
                  <div>
                    <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Prioridade</label>
                    <div className="mt-1">
                      <Badge className={`${getPriorityColor(selectedProject.priority)} text-white text-xs`}>
                        {getPriorityLabel(selectedProject.priority)}
                      </Badge>
                    </div>
                  </div>
                </div>
                <div className="mt-3">
                  <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Objetivo</label>
                  <p className="text-sm text-gray-900 mt-1">{selectedProject.objective}</p>
                </div>
                {selectedProject.description && (
                  <div className="mt-3">
                    <label className="text-xs font-medium text-gray-600 uppercase tracking-wide">Descrição</label>
                    <p className="text-sm text-gray-900 mt-1">{selectedProject.description}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        );

      case 1:
        return (
          <div className="space-y-6">
            <div className="flex items-center space-x-3">
              <Upload className="h-8 w-8 text-orange-500" />
              <div>
                <h3 className="text-xl font-semibold text-gray-900">Upload de Documentos</h3>
                <p className="text-gray-600">Anexe a documentação relevante do projeto</p>
              </div>
            </div>

            {/* Área de Upload */}
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-orange-400 transition-colors">
              <FileUp className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <div className="space-y-2">
                <p className="text-lg font-medium text-gray-900">Arraste arquivos aqui ou clique para selecionar</p>
                <p className="text-sm text-gray-500">
                  Formatos aceitos: PDF, DOC, DOCX, TXT, XLS, XLSX, PPT, PPTX
                </p>
                <input
                  type="file"
                  multiple
                  accept=".pdf,.doc,.docx,.txt,.xls,.xlsx,.ppt,.pptx"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-orange-500 hover:bg-orange-600 cursor-pointer"
                >
                  Selecionar Arquivos
                </label>
              </div>
            </div>

            {/* Lista de Arquivos */}
            {uploadedFiles.length > 0 && (
              <div className="space-y-4">
                <h4 className="text-lg font-medium text-gray-900">Arquivos Enviados ({uploadedFiles.length})</h4>
                <div className="space-y-2">
                  {uploadedFiles.map((file) => (
                    <div key={file.id} className="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200">
                      <div className="flex items-center space-x-3">
                        <FileText className="h-5 w-5 text-gray-500" />
                        <div>
                          <p className="text-sm font-medium text-gray-900">{file.name}</p>
                          <p className="text-xs text-gray-500">
                            {formatFileSize(file.size)} • {formatDate(file.uploadDate)}
                          </p>
                        </div>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleRemoveFile(file.id)}
                        className="text-red-500 hover:text-red-700 hover:bg-red-50"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );

      case 2:
        return (
          <div className="space-y-6 bg-white p-6 rounded-lg">
            <div className="flex items-center space-x-3">
              <MessageSquare className="h-8 w-8 text-orange-500" />
              <div>
                <h3 className="text-xl font-semibold text-gray-900">Geração de Perguntas</h3>
                <p className="text-gray-600">IA gera perguntas críticas</p>
              </div>
            </div>

            {!aiResults && !isAIProcessing && (
              <div className="text-center py-8">
                <Brain className="h-16 w-16 text-orange-500 mx-auto mb-4" />
                <h4 className="text-lg font-medium text-gray-900 mb-2">Análise de IA Disponível</h4>
                <p className="text-gray-600 mb-6">
                  A IA pode analisar os documentos enviados e gerar perguntas críticas para o projeto.
                </p>
                <Button
                  onClick={handleAIAnalysis}
                  className="bg-orange-500 hover:bg-orange-600 text-white"
                  disabled={uploadedFiles.length === 0}
                >
                  <Brain className="h-4 w-4 mr-2" />
                  Iniciar Análise da IA
                </Button>
                {uploadedFiles.length === 0 && (
                  <p className="text-sm text-red-500 mt-2">
                    É necessário fazer upload de documentos antes de iniciar a análise.
                  </p>
                )}
              </div>
            )}

            {isAIProcessing && (
              <div className="text-center py-8">
                <Loader2 className="h-16 w-16 text-orange-500 mx-auto mb-4 animate-spin" />
                <h4 className="text-lg font-medium text-gray-900 mb-2">Analisando Documentos...</h4>
                <p className="text-gray-600">
                  A IA está processando os documentos e gerando perguntas críticas. Isso pode levar alguns momentos.
                </p>
              </div>
            )}

            {aiResults && (
              <div className="space-y-6">
                <Alert>
                  <Brain className="h-4 w-4" />
                  <AlertDescription>
                    {aiResults.summary}
                  </AlertDescription>
                </Alert>

                <div className="bg-white p-6 rounded-lg border border-gray-200">
                  <h4 className="text-lg font-medium text-gray-900 mb-4">Perguntas Críticas Geradas</h4>
                  <div className="space-y-4">
                    {aiResults.questions.map((q) => (
                      <div key={q.id} className="bg-white p-4 rounded-lg border">
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-1">
                              <Badge variant="outline" className="text-xs">
                                {q.category}
                              </Badge>
                              <Badge 
                                className={`text-xs ${
                                  q.priority === 'high' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                                }`}
                              >
                                {q.priority === 'high' ? 'Alta Prioridade' : 'Média Prioridade'}
                              </Badge>
                            </div>
                            <h5 className="font-medium text-gray-900">{q.question}</h5>
                            <p className="text-sm text-gray-600 mt-1">{q.context}</p>
                            
                            {/* Campo de resposta */}
                            <div className="mt-3">
                              <textarea
                                placeholder="Digite sua resposta aqui..."
                                className="w-full p-3 border border-gray-300 rounded-md text-sm resize-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                                rows={3}
                              />
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h5 className="font-medium text-blue-900 mb-2">Insights da Análise</h5>
                    <ul className="text-sm text-blue-800 space-y-1">
                      {aiResults.insights.map((insight, index) => (
                        <li key={index}>• {insight}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="bg-green-50 p-4 rounded-lg">
                    <h5 className="font-medium text-green-900 mb-2">Próximos Passos</h5>
                    <ul className="text-sm text-green-800 space-y-1">
                      {aiResults.next_steps.map((step, index) => (
                        <li key={index}>• {step}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Botão para salvar respostas */}
                <div className="flex justify-center mt-6">
                  <Button
                    className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-2"
                    onClick={() => {
                      // Aqui você pode implementar a lógica para salvar as respostas
                      alert('Respostas salvas! Agora você pode avançar para a próxima etapa.');
                    }}
                  >
                    Salvar Respostas
                  </Button>
                </div>
              </div>
            )}
          </div>
        );

      default:
        return (
          <div className="text-center py-12">
            <step.icon className="h-16 w-16 text-orange-500 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">{step.title}</h3>
            <p className="text-gray-600">{step.description}</p>
            <p className="text-sm text-gray-500 mt-4">
              Esta funcionalidade será implementada em breve.
            </p>
          </div>
        );
    }
  };

  if (!selectedProject) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <FolderOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Nenhum projeto selecionado</h2>
          <p className="text-gray-600 mb-6">Crie um novo projeto para começar</p>
          <Button
            onClick={() => setShowCreateModal(true)}
            className="bg-orange-500 hover:bg-orange-600 text-white"
          >
            <Plus className="h-4 w-4 mr-2" />
            Criar Projeto
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <img src={apolloLogo} alt="Apollo" className="h-10 w-10" />
              <div>
                <h1 className="text-xl font-bold text-orange-600">Apollo Project Orchestrator</h1>
                <p className="text-sm text-gray-600">Gestão Inteligente de Projetos</p>
              </div>
            </div>
            <div className="text-right">
              <h2 className="text-lg font-semibold text-gray-900">Sistema de Gestão de Projetos</h2>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <div className="w-80 bg-gray-900 min-h-screen p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-white">Meus Projetos</h2>
            <Button
              onClick={() => setShowCreateModal(true)}
              size="sm"
              className="bg-orange-500 hover:bg-orange-600 text-white"
            >
              <Plus className="h-4 w-4 mr-1" />
              Novo
            </Button>
          </div>

          <div className="space-y-3">
            {projects.map((project) => {
              const daysLeft = getDaysUntilDeadline(project.deadline);
              const isSelected = selectedProject && selectedProject.id === project.id;
              
              return (
                <div
                  key={project.id}
                  onClick={() => setSelectedProject(project)}
                  className={`p-4 rounded-lg cursor-pointer transition-colors ${
                    isSelected 
                      ? 'bg-orange-100 border-2 border-orange-300' 
                      : 'bg-gray-800 hover:bg-gray-700 border-2 border-transparent'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className={`font-medium ${isSelected ? 'text-orange-900' : 'text-white'}`}>
                      {project.name}
                    </h3>
                    <div className="flex space-x-1">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleEditProject(project);
                        }}
                        className={`h-6 w-6 p-0 ${
                          isSelected 
                            ? 'text-orange-600 hover:text-orange-800 hover:bg-orange-200' 
                            : 'text-gray-400 hover:text-white hover:bg-gray-600'
                        }`}
                      >
                        <Edit className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteProject(project.id);
                        }}
                        className={`h-6 w-6 p-0 ${
                          isSelected 
                            ? 'text-red-600 hover:text-red-800 hover:bg-red-100' 
                            : 'text-gray-400 hover:text-red-400 hover:bg-gray-600'
                        }`}
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                  
                  <p className={`text-sm mb-3 ${isSelected ? 'text-orange-700' : 'text-gray-300'}`}>
                    {project.client}
                  </p>
                  
                  <div className="flex items-center space-x-2 mb-2">
                    <Calendar className={`h-3 w-3 ${isSelected ? 'text-orange-600' : 'text-gray-400'}`} />
                    <span className={`text-xs ${isSelected ? 'text-orange-700' : 'text-gray-400'}`}>
                      {formatDate(project.start_date)}
                    </span>
                    <Clock className={`h-3 w-3 ${isSelected ? 'text-orange-600' : 'text-gray-400'}`} />
                    <span className={`text-xs ${
                      daysLeft !== null && daysLeft < 7 
                        ? 'text-red-500 font-medium' 
                        : isSelected ? 'text-orange-700' : 'text-gray-400'
                    }`}>
                      {daysLeft !== null ? `${daysLeft} dias` : 'Sem prazo'}
                      {daysLeft !== null && daysLeft < 0 && ' (Vencido)'}
                    </span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      isSelected ? 'bg-orange-200 text-orange-800' : 'bg-gray-700 text-gray-300'
                    }`}>
                      Em andamento
                    </span>
                    <div className="flex items-center space-x-1">
                      <div className={`w-2 h-2 rounded-full ${getPriorityColor(project.priority)}`}></div>
                      <span className={`text-xs ${isSelected ? 'text-orange-700' : 'text-gray-400'}`}>
                        Etapa {project.current_step + 1}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-8">
          <div className="max-w-6xl mx-auto">
            {/* Project Header */}
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <h1 className="text-2xl font-bold text-gray-900">{selectedProject.name}</h1>
                <Badge className="text-sm">
                  Etapa {currentStep + 1} de {projectSteps.length}
                </Badge>
              </div>

              {/* Progress Bar com Foguete */}
              <div className="relative">
                <Progress 
                  value={(currentStep / (projectSteps.length - 1)) * 100} 
                  className="h-3 mb-6"
                />
                {/* Foguete */}
                <div 
                  className="absolute top-0 transform -translate-y-1 transition-all duration-500 ease-in-out"
                  style={{ 
                    left: `${(currentStep / (projectSteps.length - 1)) * 100}%`,
                    transform: `translateX(-50%) translateY(-8px)`
                  }}
                >
                  <div className="bg-orange-500 rounded-full p-2 shadow-lg">
                    <Rocket className="h-4 w-4 text-white transform rotate-45" />
                  </div>
                </div>
              </div>

              {/* Steps */}
              <div className="grid grid-cols-4 gap-4 mb-8">
                {projectSteps.map((step, index) => {
                  const StepIcon = step.icon;
                  const isCompleted = index < currentStep;
                  const isCurrent = index === currentStep;
                  
                  return (
                    <div
                      key={step.id}
                      onClick={() => handleStepChange(index)}
                      className={`p-3 rounded-lg border-2 cursor-pointer transition-all ${
                        isCurrent
                          ? 'border-orange-500 bg-orange-50'
                          : isCompleted
                          ? 'border-green-500 bg-green-50'
                          : 'border-gray-200 bg-white hover:border-gray-300'
                      }`}
                    >
                      <div className="flex items-center space-x-2 mb-2">
                        <div className={`p-1 rounded-full ${
                          isCurrent
                            ? 'bg-orange-500'
                            : isCompleted
                            ? 'bg-green-500'
                            : 'bg-gray-300'
                        }`}>
                          {isCompleted ? (
                            <CheckCircle className="h-4 w-4 text-white" />
                          ) : (
                            <StepIcon className={`h-4 w-4 ${
                              isCurrent ? 'text-white' : 'text-gray-600'
                            }`} />
                          )}
                        </div>
                        <span className={`text-xs font-medium ${
                          isCurrent ? 'text-orange-700' : isCompleted ? 'text-green-700' : 'text-gray-600'
                        }`}>
                          {index}
                        </span>
                      </div>
                      <h3 className={`text-sm font-medium mb-1 ${
                        isCurrent ? 'text-orange-900' : isCompleted ? 'text-green-900' : 'text-gray-900'
                      }`}>
                        {step.title}
                      </h3>
                      <p className={`text-xs ${
                        isCurrent ? 'text-orange-600' : isCompleted ? 'text-green-600' : 'text-gray-500'
                      }`}>
                        {step.description}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Step Content */}
            <Card>
              <CardContent className="p-8">
                {error && (
                  <Alert className="mb-6 border-red-200 bg-red-50">
                    <AlertDescription className="text-red-800">
                      {error}
                    </AlertDescription>
                  </Alert>
                )}
                
                {renderStepContent()}
              </CardContent>
            </Card>

            {/* Navigation */}
            <div className="flex justify-between mt-8">
              <Button
                variant="outline"
                onClick={() => handleStepChange(Math.max(0, currentStep - 1))}
                disabled={currentStep === 0}
                className="border-gray-300 text-gray-700 hover:bg-gray-100"
              >
                <ArrowLeft className="h-4 w-4 mr-2" />
                Etapa Anterior
              </Button>
              
              <Button
                onClick={() => handleStepChange(Math.min(projectSteps.length - 1, currentStep + 1))}
                disabled={currentStep === projectSteps.length - 1}
                className="bg-orange-500 hover:bg-orange-600 text-white"
              >
                Próxima Etapa
                <Rocket className="h-4 w-4 ml-2" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal */}
      <CreateProjectModal
        isOpen={showCreateModal}
        onClose={() => {
          setShowCreateModal(false);
          setEditingProject(null);
        }}
        onProjectCreated={handleProjectCreated}
        editingProject={editingProject}
      />
    </div>
  );
}

export default App;

