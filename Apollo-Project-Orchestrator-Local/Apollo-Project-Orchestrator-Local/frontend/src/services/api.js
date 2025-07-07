const API_BASE_URL = 'http://localhost:5000/api';

export const ApiService = {
  // Health check
  async health() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('Health check failed:', error);
      return { error: error.message };
    }
  },

  // Login
  async login(credentials) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();

      if (!response.ok) {
        return { error: data.message || 'Erro no login' };
      }

      return {
        success: true,
        user: data.user,
        token: data.token,
        message: data.message
      };
    } catch (error) {
      console.error('Login error:', error);
      return { error: 'Erro de conexão com o servidor' };
    }
  },

  // Register
  async register(userData) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (!response.ok) {
        return { error: data.message || 'Erro no cadastro' };
      }

      return {
        success: true,
        user: data.user,
        token: data.token,
        message: data.message
      };
    } catch (error) {
      console.error('Register error:', error);
      return { error: 'Erro de conexão com o servidor' };
    }
  },

  // Verify token
  async verifyToken(token) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/verify`, {
        method: 'POST', // Mudança importante: deve ser POST
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const data = await response.json();
        return { error: data.message || 'Token inválido' };
      }

      const data = await response.json();
      return {
        success: true,
        user: data.user
      };
    } catch (error) {
      console.error('Token verification error:', error);
      return { error: 'Erro de conexão com o servidor' };
    }
  },

  // Projects
  async getProjects(token) {

    // console.log('Fetching projects with token:', token);

    try {
      const response = await fetch(`${API_BASE_URL}/projects`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        return { error: data.message || 'Erro ao carregar projetos' };
      }

      return { success: true, projects: data.projects };
    } catch (error) {
      console.error('Get projects error:', error);
      return { error: 'Erro de conexão com o servidor' };
    }
  },

  async createProject(projectData, token) {
  try {
    alert('Vai enviar para o backend: ' + JSON.stringify(projectData));
    console.log('Vai enviar para o backend:', projectData);

    const response = await fetch(`${API_BASE_URL}/projects`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(projectData),
    });

    const data = await response.json();

    if (!response.ok) {
      return { error: data.message || 'Erro ao criar projeto' };
    }

    return {
      success: true,
      project: data.project,
      message: data.message
    };
  } catch (error) {
    console.error('Create project error:', error);
    return { error: 'Erro de conexão com o servidor' };
  }
},

  async updateProject(projectId, projectData, token) {
    try {
      const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(projectData),
      });

      const data = await response.json();

      if (!response.ok) {
        return { error: data.message || 'Erro ao atualizar projeto' };
      }

      return {
        success: true,
        project: data.project,
        message: data.message
      };
    } catch (error) {
      console.error('Update project error:', error);
      return { error: 'Erro de conexão com o servidor' };
    }
  },

  async deleteProject(projectId, token) {
    try {
      const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        return { error: data.message || 'Erro ao excluir projeto' };
      }

      return {
        success: true,
        message: data.message
      };
    } catch (error) {
      console.error('Delete project error:', error);
      return { error: 'Erro de conexão com o servidor' };
    }
  },

  // AI Analysis
  async analyzeDocuments(token) {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({}),
      });

      const data = await response.json();

      if (!response.ok) {
        return { error: data.message || 'Erro na análise da IA' };
      }

      return { success: true, analysis: data };
    } catch (error) {
      console.error('AI analysis error:', error);
      return { error: 'Erro de conexão com o servidor' };
    }
  }
};