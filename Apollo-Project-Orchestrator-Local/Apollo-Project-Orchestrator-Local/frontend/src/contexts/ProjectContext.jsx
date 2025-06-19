// src/contexts/ProjectContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { apiService } from '../services/api';
import { toast } from 'sonner';

const ProjectContext = createContext();

export const useProject = () => {
  const context = useContext(ProjectContext);
  if (!context) {
    throw new Error('useProject must be used within a ProjectProvider');
  }
  return context;
};

export const ProjectProvider = ({ children }) => {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [files, setFiles] = useState([]);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentStep, setCurrentStep] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);

  // Project steps
  const projectSteps = [
    { id: 'setup', name: 'Configuração', description: 'Configurar projeto básico' },
    { id: 'upload', name: 'Upload de Arquivos', description: 'Carregar arquivos do projeto' },
    { id: 'validation', name: 'Validação', description: 'Validar arquivos carregados' },
    { id: 'analysis', name: 'Análise', description: 'Analisar estrutura do projeto' },
    { id: 'optimization', name: 'Otimização', description: 'Sugerir melhorias' },
    { id: 'documentation', name: 'Documentação', description: 'Gerar documentação' },
    { id: 'deployment', name: 'Deploy', description: 'Preparar para deploy' },
    { id: 'completion', name: 'Finalização', description: 'Projeto concluído' }
  ];

  // Load project data on mount
  useEffect(() => {
    if (id) {
      loadProject();
      loadFiles();
    }
  }, [id]);

  const loadProject = async () => {
    try {
      setLoading(true);
      const response = await apiService.getProject(id);
      
      if (response.success) {
        setProject(response.data);
        setCurrentStep(response.data.currentStep || 0);
      } else {
        throw new Error(response.message || 'Erro ao carregar projeto');
      }
    } catch (error) {
      console.error('Load project error:', error);
      toast.error('Erro ao carregar projeto');
    } finally {
      setLoading(false);
    }
  };

  const loadFiles = async () => {
    try {
      const response = await apiService.getFiles(id);
      if (response.success) {
        setFiles(response.data || []);
      }
    } catch (error) {
      console.error('Load files error:', error);
    }
  };

  const loadAnalysisResults = async () => {
    try {
      const response = await apiService.getAnalysisResults(id);
      if (response.success) {
        setAnalysisResults(response.data);
      }
    } catch (error) {
      console.error('Load analysis error:', error);
    }
  };

  const updateProject = async (updates) => {
    try {
      const response = await apiService.updateProject(id, updates);
      if (response.success) {
        setProject(prev => ({ ...prev, ...updates }));
        toast.success('Projeto atualizado com sucesso');
        return { success: true };
      } else {
        throw new Error(response.message || 'Erro ao atualizar projeto');
      }
    } catch (error) {
      console.error('Update project error:', error);
      toast.error('Erro ao atualizar projeto');
      return { success: false, error: error.message };
    }
  };

  const uploadFiles = async (fileList) => {
    try {
      setIsProcessing(true);
      const uploadPromises = Array.from(fileList).map(file => 
        apiService.uploadFile(id, file)
      );
      
      const results = await Promise.all(uploadPromises);
      const successful = results.filter(r => r.success);
      
      if (successful.length > 0) {
        await loadFiles(); // Reload files list
        toast.success(`${successful.length} arquivo(s) enviado(s) com sucesso`);
      }
      
      const failed = results.filter(r => !r.success);
      if (failed.length > 0) {
        toast.error(`${failed.length} arquivo(s) falharam no upload`);
      }
      
      return { success: successful.length > 0, uploaded: successful.length };
    } catch (error) {
      console.error('Upload files error:', error);
      toast.error('Erro ao enviar arquivos');
      return { success: false, error: error.message };
    } finally {
      setIsProcessing(false);
    }
  };

  const deleteFile = async (fileId) => {
    try {
      const response = await apiService.deleteFile(fileId);
      if (response.success) {
        setFiles(prev => prev.filter(f => f.id !== fileId));
        toast.success('Arquivo removido com sucesso');
        return { success: true };
      } else {
        throw new Error(response.message || 'Erro ao remover arquivo');
      }
    } catch (error) {
      console.error('Delete file error:', error);
      toast.error('Erro ao remover arquivo');
      return { success: false, error: error.message };
    }
  };

  const analyzeProject = async () => {
    try {
      setIsProcessing(true);
      const response = await apiService.analyzeProject(id);
      
      if (response.success) {
        await loadAnalysisResults();
        toast.success('Análise concluída com sucesso');
        return { success: true, data: response.data };
      } else {
        throw new Error(response.message || 'Erro na análise');
      }
    } catch (error) {
      console.error('Analyze project error:', error);
      toast.error('Erro ao analisar projeto');
      return { success: false, error: error.message };
    } finally {
      setIsProcessing(false);
    }
  };

  const nextStep = async () => {
    if (currentStep < projectSteps.length - 1) {
      const newStep = currentStep + 1;
      const updateResult = await updateProject({ currentStep: newStep });
      if (updateResult.success) {
        setCurrentStep(newStep);
      }
      return updateResult;
    }
    return { success: false, error: 'Já está na última etapa' };
  };

  const previousStep = async () => {
    if (currentStep > 0) {
      const newStep = currentStep - 1;
      const updateResult = await updateProject({ currentStep: newStep });
      if (updateResult.success) {
        setCurrentStep(newStep);
      }
      return updateResult;
    }
    return { success: false, error: 'Já está na primeira etapa' };
  };

  const goToStep = async (stepIndex) => {
    if (stepIndex >= 0 && stepIndex < projectSteps.length) {
      const updateResult = await updateProject({ currentStep: stepIndex });
      if (updateResult.success) {
        setCurrentStep(stepIndex);
      }
      return updateResult;
    }
    return { success: false, error: 'Etapa inválida' };
  };

  const value = {
    // Data
    project,
    files,
    analysisResults,
    loading,
    isProcessing,
    
    // Steps
    projectSteps,
    currentStep,
    currentStepData: projectSteps[currentStep],
    
    // Actions
    loadProject,
    loadFiles,
    loadAnalysisResults,
    updateProject,
    uploadFiles,
    deleteFile,
    analyzeProject,
    
    // Navigation
    nextStep,
    previousStep,
    goToStep,
  };

  return (
    <ProjectContext.Provider value={value}>
      {children}
    </ProjectContext.Provider>
  );
};