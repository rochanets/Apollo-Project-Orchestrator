import { createContext, useContext, useEffect, useState } from 'react';
import { ApiService } from '../services/api.js';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Verificar se o usuário já está autenticado ao carregar
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('apollo_token');
        const userData = localStorage.getItem('apollo_user');
        
        if (token && userData) {
          // Verificar se o token ainda é válido no backend
          const result = await ApiService.verifyToken(token);
          
          if (result.success) {
            setUser(result.user);
          } else {
            // Token inválido, limpar storage
            console.warn('Token inválido:', result.error);
            localStorage.removeItem('apollo_token');
            localStorage.removeItem('apollo_user');
            setUser(null);
          }
        }
      } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
        // Em caso de erro, limpar dados
        localStorage.removeItem('apollo_token');
        localStorage.removeItem('apollo_user');
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (credentials) => {
    try {
      setLoading(true);
      
      const result = await ApiService.login(credentials);
      
      if (result.error) {
        return { success: false, error: result.error };
      }
      
      // Login bem-sucedido
      localStorage.setItem('apollo_user', JSON.stringify(result.user));
      localStorage.setItem('apollo_token', result.token);
      setUser(result.user);
      
      return { success: true, message: result.message };
    } catch (error) {
      console.error('Erro no login:', error);
      return { success: false, error: 'Erro interno no login' };
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setLoading(true);
      
      const result = await ApiService.register(userData);
      
      if (result.error) {
        return { success: false, error: result.error };
      }
      
      // Cadastro bem-sucedido - não fazer login automático
      return { 
        success: true, 
        message: result.message || 'Cadastro realizado com sucesso! Faça login para continuar.' 
      };
    } catch (error) {
      console.error('Erro no registro:', error);
      return { success: false, error: 'Erro interno no cadastro' };
    } finally {
      setLoading(false);
    }
  };

  const requestPasswordReset = async (email) => {
    try {
      setLoading(true);
      
      // Simular envio de email de recuperação
      // Em um sistema real, isso enviaria um email com link de reset
      return { 
        success: true, 
        message: `Um email de recuperação foi enviado para ${email}. Verifique sua caixa de entrada.` 
      };
    } catch (error) {
      console.error('Erro na recuperação de senha:', error);
      return { success: false, error: 'Erro ao solicitar recuperação de senha' };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('apollo_user');
    localStorage.removeItem('apollo_token');
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      loading, 
      login, 
      register, 
      requestPasswordReset,
      logout 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);