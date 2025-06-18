const API_BASE_URL = 'http://localhost:5000/api/auth';

export const ApiService = {
  login: async (data) => {
    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return await response.json();
    } catch (error) {
      return { error: 'Erro ao conectar com a API.' };
    }
  },

  register: async (data) => {
    try {
      const response = await fetch(`${API_BASE_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return await response.json();
    } catch (error) {
      return { error: 'Erro ao conectar com a API.' };
    }
  }
};
