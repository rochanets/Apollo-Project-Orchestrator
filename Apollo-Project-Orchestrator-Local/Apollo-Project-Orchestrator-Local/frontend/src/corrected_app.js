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
import ProjectWorkspace from './components/ProjectWorkspace.jsx';
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

function App() {
  // Estados principais
  const [projects, setProjects] = useState(initialMockProjects);
  const [selectedProject, setSelectedProject] = useState(initialMockProjects[0]);
  const [currentStep, setCurrentStep] = useState(initialMockProjects[0]?.current_step || 0);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const [backendStatus, setBackendStatus] = useState('checking');

  // Verificação de status do backend
  useEffect(() => {
    const checkBackend = async () => {
      const health = await ApiService.health();
      setBackendStatus(health.error ? 'offline' : 'online');
    };
    
    checkBackend();
    
    // Verificar a cada 30 segundos
    const interval = setInterval(checkBackend, 30000);
    return () => clearInterval(interval);
  }, []);

  // Atualizar currentStep quando selectedProject mudar
  useEffect(() => {
    if (selectedProject) {
      setCurrentStep(selectedProject.current_step || 0);
    }
  }, [selectedProject?.id]);

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
    setCurrentStep(newStep);
    updateProjectStep(newStep);
  };

  const updateProjectStep = (step) => {
    if (selectedProject) {
      const updatedProject = { ...selectedProject, current_step: step };
      const updatedProjects = projects.map(p => 
        p.id === selectedProject.id ? updatedProject : p
      );
      setProjects(updatedProjects);
      setSelectedProject(updatedProject);
    }
  };

  const handleProjectUpdate = (updatedProject) => {
    const updatedProjects = projects.map(p => 
      p.id === updatedProject.id ? updatedProject : p
    );
    setProjects(updatedProjects);
    setSelectedProject(updatedProject);
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
      {/* Alerta de Backend Offline */}
      {backendStatus === 'offline' && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
          <div className="flex">
            <div className="ml-3">
              <p className="text-sm text-yellow-700">
                ⚠️ Backend desconectado - Funcionando em modo offline com dados simulados
              </p>
            </div>
          </div>
        </div>
      )}

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
            <ProjectWorkspace
              selectedProject={selectedProject}
              onProjectUpdate={handleProjectUpdate}
              currentStep={currentStep}
              onStepChange={handleStepChange}
              projectSteps={projectSteps}
            />
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