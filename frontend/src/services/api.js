const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request(endpoint, options = {}) {
  const res = await fetch(`${API_URL}${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || `Erro ${res.status}`);
  }
  return res.json();
}

// Recursos
export const getRecursos = (skip = 0, limit = 10, search = '') => {
  const params = new URLSearchParams({ skip, limit, search });
  return request(`/recursos?${params}`);
};

export const getRecurso = (id) => request(`/recursos/${id}`);

export const createRecurso = (data) =>
  request('/recursos', { method: 'POST', body: JSON.stringify(data) });

export const updateRecurso = (id, data) =>
  request(`/recursos/${id}`, { method: 'PUT', body: JSON.stringify(data) });

export const deleteRecurso = (id) =>
  request(`/recursos/${id}`, { method: 'DELETE' });

// IA
export const gerarSugestaoIA = (titulo, tipo) =>
  request('/ia/sugestao', {
    method: 'POST',
    body: JSON.stringify({ titulo, tipo }),
  });