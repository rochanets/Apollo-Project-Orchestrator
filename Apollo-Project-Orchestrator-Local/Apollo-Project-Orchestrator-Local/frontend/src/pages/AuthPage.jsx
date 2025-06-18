import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { ApiService } from '../services/api';

const AuthPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');

  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    company: '',
    role: ''
  });
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    // Validação de confirmação de senha
    if (!isLoginMode && form.password !== confirmPassword) {
      setError("As senhas não coincidem.");
      setLoading(false);
      return;
    }

    try {
      const response = isLoginMode
        ? await ApiService.login({ email: form.email, password: form.password })
        : await ApiService.register(form);

      if (response.error) {
        setError(response.error);
      } else {
        if (isLoginMode) {
          login(response.user);
          navigate('/app');
        } else {
          setSuccess("Cadastro realizado com sucesso! Faça login para continuar.");
          // Limpa campos de cadastro após sucesso
          setForm({
            name: '',
            email: '',
            password: '',
            company: '',
            role: ''
          });
          setConfirmPassword('');
          setIsLoginMode(true);
        }
      }
    } catch (err) {
      setError('Erro de conexão com o servidor.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="card w-full max-w-md animate-fade-in">
        <div className="card-header text-center">
          <h2 className="text-2xl font-bold text-primary mb-2">
            {isLoginMode ? 'Entrar' : 'Cadastrar'}
          </h2>
          <p className="text-muted-foreground">Gestão Inteligente de Projetos</p>
        </div>
        <div className="card-content">
          {error && <div className="alert alert-error mb-4">{error}</div>}
          {success && <div className="alert alert-success mb-4">{success}</div>}

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLoginMode && (
              <>
                <div>
                  <label className="form-label">Nome</label>
                  <input
                    name="name"
                    placeholder="Nome completo"
                    className="form-input"
                    value={form.name}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div>
                  <label className="form-label">Célula (número)</label>
                  <input
                    name="company"
                    placeholder="Célula"
                    className="form-input"
                    value={form.company}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label className="form-label">Cargo (opcional)</label>
                  <input
                    name="role"
                    placeholder="Cargo"
                    className="form-input"
                    value={form.role}
                    onChange={handleChange}
                  />
                </div>
              </>
            )}
            <div>
              <label className="form-label">Email</label>
              <input
                name="email"
                type="email"
                placeholder="Email"
                className="form-input"
                value={form.email}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <label className="form-label">Senha</label>
              <input
                name="password"
                type="password"
                placeholder="Senha"
                className="form-input"
                value={form.password}
                onChange={handleChange}
                required
              />
            </div>
            {!isLoginMode && (
              <div>
                <label className="form-label">Confirmar Senha</label>
                <input
                  name="confirmPassword"
                  type="password"
                  placeholder="Confirme a senha"
                  className="form-input"
                  value={confirmPassword}
                  onChange={e => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
            )}
            <button type="submit" className="btn-primary w-full" disabled={loading}>
              {loading ? 'Carregando...' : isLoginMode ? 'Entrar' : 'Cadastrar'}
            </button>
          </form>
          <div className="text-center mt-4">
            <span>
              {isLoginMode ? 'Não tem uma conta?' : 'Já tem uma conta?'}{' '}
            </span>
            <button
              type="button"
              className="btn-secondary ml-2"
              onClick={() => {
                setIsLoginMode(!isLoginMode);
                setError('');
                setSuccess('');
              }}
            >
              {isLoginMode ? 'Cadastrar' : 'Entrar'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
