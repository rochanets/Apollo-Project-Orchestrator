import React, { useState } from 'react';
import { Button } from '@/components/ui/button.jsx';
import { Input } from '@/components/ui/input.jsx';
import { Label } from '@/components/ui/label.jsx';
import { Textarea } from '@/components/ui/textarea.jsx';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx';
import { X } from 'lucide-react';

const CreateProjectModal = ({ isOpen, onClose, onProjectCreated, editingProject }) => {
  const [formData, setFormData] = useState({
    name: editingProject?.name || '',
    client: editingProject?.client || '',
    responsible: editingProject?.responsible || '',
    objective: editingProject?.objective || '',
    description: editingProject?.description || '',
    priority: editingProject?.priority || 'medium'
    // status será sempre 'active' no envio, não precisa aqui
  });

  const [errors, setErrors] = useState({});

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Limpar erro do campo quando o usuário começar a digitar
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Nome do projeto é obrigatório';
    }

    if (!formData.client.trim()) {
      newErrors.client = 'Cliente é obrigatório';
    }

    if (!formData.responsible.trim()) {
      newErrors.responsible = 'Responsável é obrigatório';
    }

    if (!formData.objective.trim()) {
      newErrors.objective = 'Objetivo é obrigatório';
    }

    // Validação de datas
    if (formData.start_date && formData.deadline) {
      const startDate = new Date(formData.start_date);
      const deadlineDate = new Date(formData.deadline);

      if (startDate >= deadlineDate) {
        newErrors.deadline = 'Prazo final deve ser posterior à data de início';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('handleSubmit chamado', formData);

    if (!validateForm()) {
      return;
    }

    const cleanData = {
      name: formData.name,
      client: formData.client,
      responsible: formData.responsible,
      objective: formData.objective,
      description: formData.description,
      priority: formData.priority,
      status: 'active',
      start_date: formData.start_date,
      deadline: formData.deadline
    };

    console.log('Enviando para onProjectCreated:', cleanData, !!editingProject);
    onProjectCreated(cleanData, !!editingProject);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b border-orange-200 bg-orange-50">
          <h2 className="text-xl font-semibold text-orange-800">
            {editingProject ? 'Editar Projeto' : 'Criar Novo Projeto'}
          </h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            className="text-orange-600 hover:text-orange-800 hover:bg-orange-100"
          >
            <X className="h-5 w-5" />
          </Button>
        </div>

        <div className="overflow-y-auto max-h-[calc(90vh-140px)]">
          <form onSubmit={handleSubmit} className="p-6 space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <Label htmlFor="name" className="text-orange-700 font-medium">Nome do Projeto *</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  placeholder="Ex: Sistema de Vendas"
                  className={`mt-1 border-orange-300 focus:border-orange-500 focus:ring-orange-500 text-orange-800 placeholder-orange-400 ${errors.name ? 'border-red-500' : ''
                    }`}
                />
                {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
              </div>

              <div>
                <Label htmlFor="client" className="text-orange-700 font-medium">Cliente *</Label>
                <Input
                  id="client"
                  value={formData.client}
                  onChange={(e) => handleInputChange('client', e.target.value)}
                  placeholder="Ex: Empresa ABC"
                  className={`mt-1 border-orange-300 focus:border-orange-500 focus:ring-orange-500 text-orange-800 placeholder-orange-400 ${errors.client ? 'border-red-500' : ''
                    }`}
                />
                {errors.client && <p className="text-red-500 text-sm mt-1">{errors.client}</p>}
              </div>

              <div>
                <Label htmlFor="responsible" className="text-orange-700 font-medium">Responsável *</Label>
                <Input
                  id="responsible"
                  value={formData.responsible}
                  onChange={(e) => handleInputChange('responsible', e.target.value)}
                  placeholder="Ex: João Silva"
                  className={`mt-1 border-orange-300 focus:border-orange-500 focus:ring-orange-500 text-orange-800 placeholder-orange-400 ${errors.responsible ? 'border-red-500' : ''
                    }`}
                />
                {errors.responsible && <p className="text-red-500 text-sm mt-1">{errors.responsible}</p>}
              </div>

              <div>
                <Label htmlFor="priority" className="text-orange-700 font-medium">Prioridade</Label>
                <Select value={formData.priority} onValueChange={(value) => handleInputChange('priority', value)}>
                  <SelectTrigger className="mt-1 border-orange-300 focus:border-orange-500 focus:ring-orange-500 text-orange-800">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Baixa</SelectItem>
                    <SelectItem value="medium">Média</SelectItem>
                    <SelectItem value="high">Alta</SelectItem>
                    <SelectItem value="urgent">Urgente</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="start_date" className="text-orange-700 font-medium">Data de Início</Label>
                <Input
                  id="start_date"
                  type="date"
                  value={formData.start_date}
                  onChange={(e) => handleInputChange('start_date', e.target.value)}
                  className="mt-1 border-orange-300 focus:border-orange-500 focus:ring-orange-500 text-orange-800"
                />
              </div>

              <div>
                <Label htmlFor="deadline" className="text-orange-700 font-medium">Prazo Final</Label>
                <Input
                  id="deadline"
                  type="date"
                  value={formData.deadline}
                  onChange={(e) => handleInputChange('deadline', e.target.value)}
                  className={`mt-1 border-orange-300 focus:border-orange-500 focus:ring-orange-500 text-orange-800 ${errors.deadline ? 'border-red-500' : ''
                    }`}
                />
                {errors.deadline && <p className="text-red-500 text-sm mt-1">{errors.deadline}</p>}
              </div>
            </div>

            <div>
              <Label htmlFor="objective" className="text-orange-700 font-medium">Objetivo *</Label>
              <Textarea
                id="objective"
                value={formData.objective}
                onChange={(e) => handleInputChange('objective', e.target.value)}
                placeholder="Descreva o objetivo principal do projeto..."
                rows={3}
                className={`mt-1 border-orange-300 focus:border-orange-500 focus:ring-orange-500 text-orange-800 placeholder-orange-400 ${errors.objective ? 'border-red-500' : ''
                  }`}
              />
              {errors.objective && <p className="text-red-500 text-sm mt-1">{errors.objective}</p>}
            </div>

            <div>
              <Label htmlFor="description" className="text-orange-700 font-medium">Descrição (Opcional)</Label>
              <Textarea
                id="description"
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                placeholder="Informações adicionais sobre o projeto..."
                rows={3}
                className="mt-1 border-orange-300 focus:border-orange-500 focus:ring-orange-500 text-orange-800 placeholder-orange-400"
              />
            </div>

            <div className="flex justify-end space-x-3 pt-6 border-t border-orange-200">
              <Button
                type="button"
                variant="outline"
                onClick={onClose}
                className="border-orange-300 text-orange-700 hover:bg-orange-100"
              >
                Cancelar
              </Button>
              <Button
                type="submit"
                className="bg-orange-500 hover:bg-orange-600 text-white"
              >
                {editingProject ? 'Atualizar Projeto' : 'Criar Projeto'}
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CreateProjectModal;

