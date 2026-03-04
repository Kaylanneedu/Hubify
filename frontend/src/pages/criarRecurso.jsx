import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createRecurso, getRecurso, updateRecurso, gerarSugestaoIA } from '../services/api';

export default function CriarRecurso() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    titulo: '',
    descricao: '',
    tipo: 'video',
    link: '',
    tags: '',
  });
  const [loadingIA, setLoadingIA] = useState(false);
  const [errorIA, setErrorIA] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (id) {
      getRecurso(id).then((data) => {
        setForm({
          titulo: data.titulo,
          descricao: data.descricao || '',
          tipo: data.tipo,
          link: data.link || '',
          tags: data.tags || '',
        });
      }).catch(() => alert('Erro ao carregar recurso'));
    }
  }, [id]);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleGerarDescricao() {
    if (!form.titulo.trim()) {
      alert('Preencha o título primeiro');
      return;
    }
    setLoadingIA(true);
    setErrorIA('');
    try {
      const resposta = await gerarSugestaoIA(form.titulo, form.tipo);
      setForm((prev) => ({
        ...prev,
        descricao: resposta.descricao,
        tags: resposta.tags,
      }));
    } catch (error) {
      setErrorIA('Erro ao gerar sugestão. Tente novamente.');
    } finally {
      setLoadingIA(false);
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSaving(true);
    try {
      if (id) {
        await updateRecurso(id, form);
      } else {
        await createRecurso(form);
      }
      navigate('/');
    } catch (error) {
      alert('Erro ao salvar recurso');
    } finally {
      setSaving(false);
    }
  }

  return (
    <div style={{ 
      padding: '20px 30px', 
      maxWidth: '800px',  // Opcional: limite para formulário não ficar muito largo
      width: '100%', 
      boxSizing: 'border-box',
      margin: '0 auto'    // Centraliza o formulário, mas não a página inteira
    }}>
      <h1>{id ? 'Editar Recurso' : 'Novo Recurso'}</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="titulo">Título *</label>
          <input
            type="text"
            id="titulo"
            name="titulo"
            value={form.titulo}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="tipo">Tipo</label>
          <select
            id="tipo"
            name="tipo"
            value={form.tipo}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          >
            <option value="video">Vídeo</option>
            <option value="pdf">PDF</option>
            <option value="link">Link</option>
          </select>
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="link">Link (opcional)</label>
          <input
            type="url"
            id="link"
            name="link"
            value={form.link}
            onChange={handleChange}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="descricao">Descrição</label>
          <textarea
            id="descricao"
            name="descricao"
            value={form.descricao}
            onChange={handleChange}
            rows="4"
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="tags">Tags (separadas por vírgula)</label>
          <input
            type="text"
            id="tags"
            name="tags"
            value={form.tags}
            onChange={handleChange}
            placeholder="ex: matemática, vídeo, educação"
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <button
            type="button"
            onClick={handleGerarDescricao}
            disabled={loadingIA}
            style={{ padding: '10px 15px', marginRight: '10px' }}
          >
            {loadingIA ? '🤖 Gerando...' : '🤖 Gerar Descrição com IA'}
          </button>
          {errorIA && <span style={{ color: 'red' }}>{errorIA}</span>}
        </div>

        <div>
          <button type="submit" disabled={saving} style={{ padding: '10px 20px' }}>
            {saving ? 'Salvando...' : 'Salvar'}
          </button>
          <button type="button" onClick={() => navigate('/')} style={{ padding: '10px 20px', marginLeft: '10px' }}>
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}