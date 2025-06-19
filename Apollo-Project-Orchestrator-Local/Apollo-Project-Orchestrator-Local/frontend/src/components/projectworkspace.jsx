import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Button } from '@/components/ui/button.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import { Progress } from '@/components/ui/progress.jsx';
import { Alert, AlertDescription } from '@/components/ui/alert.jsx';
import { 
  FileText, 
  Upload, 
  MessageSquare, 
  Database, 
  Settings, 
  Code, 
  TestTube, 
  Rocket,
  CheckCircle,
  Brain,
  Loader2,
  FileUp,
  X,
  ArrowLeft,
  Calendar,
  Clock,
  User
} from 'lucide-react';

const ProjectWorkspace = ({ 
  selectedProject, 
  onProjectUpdate, 
  currentStep, 
  onStepChange,
  projectSteps 
}) => {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [isAIProcessing, setIsAIProcessing] = useState(false);
  const [aiResults, setAiResults] = useState(null);
  const [error, setError] = useState('');

  // Inicializar dados do projeto selecionado
  useEffect(() => {
    if (selectedProject) {
      setUploadedFiles(selectedProject.uploaded_files || []);
      setAiResults(selectedProject.ai_analysis);
    }
  }, [selectedProject]);

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
    if (selectedProject && onProjectUpdate) {
      const updatedProject = { 
        ...selectedProject, 
        uploaded_files: updatedFiles 
      };
      onProjectUpdate(updatedProject);
    }
  };

  const handleRemoveFile = (fileId) => {
    const updatedFiles = uploadedFiles.filter(f => f.id !== fileId);
    setUploadedFiles(updatedFiles);

    // Atualizar projeto
    if (selectedProject && onProjectUpdate) {
      const updatedProject = { 
        ...selectedProject, 
        uploaded_files: updatedFiles 
      };
      onProjectUpdate(updatedProject);
    }
  };

  const simulateAIAnalysis = async (files, projectData) => {
    // Simular delay de processamento
    await new Promise(resolve => setTimeout(resolve, 3000));
    
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

  const handleAIAnalysis = async () => {
    if (uploadedFiles.length === 0) {
      setError('Por favor, faça upload de pelo menos um documento antes de solicitar a análise da IA.');
      return;
    }

    setIsAIProcessing(true);
    setError('');

    try {
      const analysis = await simulateAIAnalysis(uploadedFiles, {
        name: selectedProject.name,
        objective: selectedProject.objective,
        description: selectedProject.description || ''
      });

      setAiResults(analysis);

      // Atualizar projeto com resultados da IA
      if (selectedProject && onProjectUpdate) {
        const updatedProject = { 
          ...selectedProject, 
          ai_analysis: analysis,
          ai_questions: analysis.questions
        };
        onProjectUpdate(updatedProject);
      }

    } catch (error) {
      console.error('Erro na análise da IA:', error);
      setError(`Erro ao processar análise da IA: ${error.message}`);
    } finally {
      setIsAIProcessing(false);
    }
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
              <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 max-w-4xl">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <label className="text-xs font-medium text-orange-600 uppercase tracking-wide">Nome do Projeto</label>
                    <p className="text-sm font-semibold text-gray-800 mt-1">{selectedProject.name}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <label className="text-xs font-medium text-orange-600 uppercase tracking-wide">Cliente</label>
                    <p className="text-sm font-semibold text-gray-800 mt-1">{selectedProject.client}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <label className="text-xs font-medium text-orange-600 uppercase tracking-wide">Responsável</label>
                    <p className="text-sm font-semibold text-gray-800 mt-1">{selectedProject.responsible}</p>
                  </div>
                  <div className="bg-white p-4 rounded-lg shadow-sm">
                    <label className="text-xs font-medium text-orange-600 uppercase tracking-wide">Prioridade</label>
                    <div className="mt-1">
                      <Badge className={`${getPriorityColor(selectedProject.priority)} text-white text-xs`}>
                        {getPriorityLabel(selectedProject.priority)}
                      </Badge>
                    </div>
                  </div>
                </div>
                <div className="mt-4 bg-white p-4 rounded-lg shadow-sm">
                  <label className="text-xs font-medium text-orange-600 uppercase tracking-wide">Objetivo</label>
                  <p className="text-sm font-semibold text-gray-800 mt-1">{selectedProject.objective}</p>
                </div>
                {selectedProject.description && (
                  <div className="mt-4 bg-white p-4 rounded-lg shadow-sm">
                    <label className="text-xs font-medium text-orange-600 uppercase tracking-wide">Descrição</label>
                    <p className="text-sm font-semibold text-gray-800 mt-1">{selectedProject.description}</p>
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
            <div className="border-2 border-dashed border-orange-300 rounded-lg p-8 text-center hover:border-orange-400 transition-colors bg-orange-50">
              <FileUp className="h-12 w-12 text-orange-500 mx-auto mb-4" />
              <div className="space-y-2">
                <p className="text-lg font-medium text-orange-800">Arraste arquivos aqui ou clique para selecionar</p>
                <p className="text-sm text-orange-600">
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
                    <div key={file.id} className="flex items-center justify-between p-4 bg-white rounded-lg border border-orange-200 shadow-sm">
                      <div className="flex items-center space-x-3">
                        <FileText className="h-5 w-5 text-orange-500" />
                        <div>
                          <p className="text-sm font-medium text-gray-900">{file.name}</p>
                          <p className="text-xs text-gray-600">
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
      <div className="text-center py-12">
        <FileText className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">Selecione um projeto para visualizar o workspace</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
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
                onClick={() => onStepChange(index)}
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
                    {index + 1}
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
          onClick={() => onStepChange(Math.max(0, currentStep - 1))}
          disabled={currentStep === 0}
          className="border-gray-300 text-gray-700 hover:bg-gray-100"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Etapa Anterior
        </Button>
        
        <Button
          onClick={() => onStepChange(Math.min(projectSteps.length - 1, currentStep + 1))}
          disabled={currentStep === projectSteps.length - 1}
          className="bg-orange-500 hover:bg-orange-600 text-white"
        >
          Próxima Etapa
          <Rocket className="h-4 w-4 ml-2" />
        </Button>
      </div>
    </div>
  );
};

export default ProjectWorkspace;