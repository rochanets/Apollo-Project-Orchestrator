import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import {
  FolderOpen,
  Plus,
  Trash2,
  Edit,
  Calendar,
  Clock,
  LogOut,
  User
} from 'lucide-react';
import apolloLogo from './assets/apollo-logo.png';
import CreateProjectModal from './components/CreateProjectModal.jsx';
import ProjectWorkspace from './components/ProjectWorkspace.jsx';
import { ApiService } from './services/api.js';
import { useAuth } from './contexts/AuthContext';
import './App.css';

// Dados das etapas do projeto
const projectSteps = [
  { id: 0, title: 'Cadastro do Projeto', icon: 'FileText', description: 'Informações básicas do projeto' },
  { id: 1, title: 'Upload de Documentos', icon: 'Upload', description: 'Anexar documentação do projeto' },
  { id: 2, title: 'Geração de Perguntas', icon: 'MessageSquare', description: 'IA gera perguntas críticas' },
  { id: 3, title: 'Coleta de Informações', icon: 'Database', description: 'Documentação e esclarecimentos' },
  { id: 4, title: 'Análise Técnica', icon: 'Settings', description: 'Levantamento do ambiente' },
  { id: 5, title: 'Execução do Projeto', icon: 'Code', description: 'Desenvolvimento automatizado' },
  { id: 6, title: 'Testes', icon: 'TestTube', description: 'Testes integrados e correções' },
  { id: 7, title: 'Go Live', icon: 'Rocket', description: 'Documentação final e deploy' }
];

function App() {
  const { user, logout } = useAuth();

  // Estados principais da aplicação
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const [backendStatus, setBackendStatus] = useState('checking');
  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState(''); // NOVO ESTADO PARA ERROS DA API

  // Verificação de status do backend
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const health = await ApiService.health();
        setBackendStatus(health.error ? 'offline' : 'online');
      } catch (error) {
        setBackendStatus('offline');
      }
    };

    checkBackend();
    const interval = setInterval(checkBackend, 30000);
    return () => clearInterval(interval);
  }, []
  );

  // Carregar projetos do usuário
  useEffect(() => {
    loadUserProjects();
  }, []);

  const loadUserProjects = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('apollo_token');

      console.log('Loading projects with token:', token);


      if (!token) {
        setProjects([]);
        setSelectedProject(null);
        return;
      }

      const result = await ApiService.getProjects(token);

      if (result.success) {
        setProjects(result.projects);

        // Se há projetos e nenhum está selecionado, selecionar o primeiro
        if (result.projects.length > 0 && !selectedProject) {
          setSelectedProject(result.projects[0]);
          setCurrentStep(result.projects[0].current_step || 0);
        }

        // Se o projeto selecionado não está mais na lista, selecionar o primeiro
        if (selectedProject && !result.projects.find(p => p.id === selectedProject.id)) {
          if (result.projects.length > 0) {
            setSelectedProject(result.projects[0]);
            setCurrentStep(result.projects[0].current_step || 0);
          } else {
            setSelectedProject(null);
            setCurrentStep(0);
          }
        }
      } else {
        console.error('Erro ao carregar projetos:', result.error);
        setProjects([]);
      }
    } catch (error) {
      console.error('Erro ao carregar projetos:', error);
      setProjects([]);
    } finally {
      setLoading(false);
    }
  };

  // Atualizar currentStep quando selectedProject mudar
  useEffect(() => {
    if (selectedProject) {
      setCurrentStep(selectedProject.current_step || 0);
    }
  }, [selectedProject?.id]);

  const handleProjectCreated = async (projectData, isEditing = false) => {
    console.log('handleProjectCreated chamado', projectData, isEditing);
    const token = localStorage.getItem('apollo_token');
    setApiError(''); // Limpa qualquer erro anterior ao tentar criar/editar

    try {
      let result;

      if (isEditing) {
        result = await ApiService.updateProject(projectData.id, projectData, token);
      } else {
        result = await ApiService.createProject(projectData, token);
      }

      if (result.success) {
        await loadUserProjects();

        if (!isEditing && result.project) {
          setSelectedProject(result.project);
          setCurrentStep(result.project.current_step || 0);
        }
        setShowCreateModal(false); // Fecha o modal apenas no sucesso
        setEditingProject(null);
      } else {
        // Se result.success for false, mas não for um erro de rede
        console.error('Erro ao salvar projeto:', result.error);
        // Não usa alert aqui, mas define o erro no estado
        setApiError(result.error || 'Erro desconhecido ao salvar projeto.'); 
        // Não fecha o modal aqui para que o usuário veja o erro
        throw new Error(result.error || 'Erro desconhecido ao salvar projeto.'); // Re-lança para o catch do modal
      }
    } catch (error) {
      // Erro de rede (servidor offline, CORS, etc.)
      console.error('Erro de conexão ao salvar projeto:', error);
      // Não usa alert aqui, mas define o erro no estado
      setApiError('Erro de conexão com o servidor. Verifique sua internet ou o status do backend.'); 
      // Não fecha o modal aqui
      throw error; // Re-lança para o catch do modal
    }
  };

  const handleDeleteProject = async (projectId) => {
    if (window.confirm('Tem certeza que deseja excluir este projeto? Esta ação não pode ser desfeita.')) {
      const token = localStorage.getItem('apollo_token');

      try {
        const result = await ApiService.deleteProject(projectId, token);

        if (result.success) {
          await loadUserProjects();
        } else {
          console.error('Erro ao excluir projeto:', result.error);
          alert(`Erro ao excluir projeto: ${result.error}`);
        }
      } catch (error) {
        console.error('Erro ao excluir projeto:', error);
        alert('Erro de conexão ao excluir projeto');
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

  const updateProjectStep = async (step) => {
    if (selectedProject) {
      const token = localStorage.getItem('apollo_token');

      try {
        const result = await ApiService.updateProject(
          selectedProject.id,
          { ...selectedProject, current_step: step },
          token
        );

        if (result.success) {
          await loadUserProjects();
        } else {
          console.error('Erro ao atualizar etapa:', result.error);
        }
      } catch (error) {
        console.error('Erro ao atualizar etapa:', error);
      }
    }
  };

  const handleProjectUpdate = async (updatedProject) => {
    const token = localStorage.getItem('apollo_token');

    try {
      const result = await ApiService.updateProject(
        updatedProject.id,
        updatedProject,
        token
      );

      if (result.success) {
        await loadUserProjects();
      }
    } catch (error) {
      console.error('Erro ao atualizar projeto:', error);
    }
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

  // Loading screen
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <img src={apolloLogo} alt="Apollo" className="h-16 w-16 mx-auto mb-4 animate-pulse" />
          <p className="text-gray-600">Carregando projetos...</p>
        </div>
      </div>
    );
  }

  // Tela principal se não há projetos
  if (!selectedProject && projects.length === 0) {
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
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <User className="h-4 w-4 text-gray-600" />
                  <span className="text-sm text-gray-700">{user?.name}</span>
                </div>
                <Button
                  onClick={logout}
                  variant="outline"
                  size="sm"
                  className="text-gray-600 hover:text-red-600"
                >
                  <LogOut className="h-4 w-4 mr-1" />
                  Sair
                </Button>
              </div>
            </div>
          </div>
        </header>

        <div className="flex items-center justify-center min-h-[calc(100vh-64px)]">
          <div className="text-center">
            <FolderOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Bem-vindo ao Apollo!</h2>
            <p className="text-gray-600 mb-6">Você ainda não tem projetos. Crie seu primeiro projeto para começar.</p>
            <Button
              onClick={() => setShowCreateModal(true)}
              className="bg-orange-500 hover:bg-orange-600 text-white"
            >
              <Plus className="h-4 w-4 mr-2" />
              Criar Primeiro Projeto
            </Button>
          </div>
        </div>

        <CreateProjectModal
          isOpen={showCreateModal}
          onClose={() => {
            setShowCreateModal(false);
            setEditingProject(null);
            setApiError(''); // Limpa o erro da API ao fechar o modal
          }}
          onProjectCreated={handleProjectCreated}
          apiError={apiError} // PASSA O ERRO PARA O MODAL
          setApiError={setApiError} // PASSA A FUNÇÃO PARA LIMPAR O ERRO
        />
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
                ⚠️ Backend desconectado - Funcionando em modo offline
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
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <User className="h-4 w-4 text-gray-600" />
                <span className="text-sm text-gray-700">{user?.name}</span>
              </div>
              <Button
                onClick={logout}
                variant="outline"
                size="sm"
                className="text-gray-600 hover:text-red-600"
              >
                <LogOut className="h-4 w-4 mr-1" />
                Sair
              </Button>
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
                  className={`p-4 rounded-lg cursor-pointer transition-colors ${isSelected
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
                        className={`h-6 w-6 p-0 ${isSelected
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
                        className={`h-6 w-6 p-0 ${isSelected
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
                    <span className={`text-xs ${daysLeft !== null && daysLeft < 7
                        ? 'text-red-500 font-medium'
                        : isSelected ? 'text-orange-700' : 'text-gray-400'
                      }`}>
                      {daysLeft !== null ? `${daysLeft} dias` : 'Sem prazo'}
                      {daysLeft !== null && daysLeft < 0 && ' (Vencido)'}
                    </span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className={`text-xs px-2 py-1 rounded-full ${isSelected ? 'bg-orange-200 text-orange-800' : 'bg-gray-700 text-gray-300'
                      }`}>
                      Em andamento
                    </span>
                    <div className="flex items-center space-x-1">
                      <div className={`w-2 h-2 rounded-full ${getPriorityColor(project.priority)}`}></div>
                      <span className={`text-xs ${isSelected ? 'text-orange-700' : 'text-gray-400'}`}>
                        Etapa {(project.current_step || 0) + 1}
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
          setApiError(''); // Limpa o erro da API ao fechar o modal
        }}
        onProjectCreated={handleProjectCreated}
        editingProject={editingProject}
        apiError={apiError} // PASSA O ERRO PARA O MODAL
        setApiError={setApiError} // PASSA A FUNÇÃO PARA LIMPAR O ERRO
      />
    </div>
  );
}

export default App;
