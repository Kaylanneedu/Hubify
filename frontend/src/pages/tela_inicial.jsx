import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getRecursos, deleteRecurso } from '../services/api';

export default function TelaInicial() {
  const [recursos, setRecursos] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const limit = 10;

  async function carregar() {
    setLoading(true);
    try {
      const data = await getRecursos((page - 1) * limit, limit, search);
      setRecursos(data.items);
      setTotal(data.total);
    } catch (error) {
      alert('Erro ao carregar recursos: ' + error.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    carregar();
  }, [page, search]);

  async function handleDelete(id) {
    if (!confirm('Tem certeza que deseja excluir?')) return;
    try {
      await deleteRecurso(id);
      carregar();
    } catch {
      alert('Erro ao excluir');
    }
  }

  const totalPages = Math.ceil(total / limit);

  const buttonStyle = {
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    padding: '8px 12px',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
    transition: 'background-color 0.2s',
    marginRight: '5px'
  };

  const iconButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#45a049',
    padding: '8px 12px'
  };

  return (
    <div style={{ 
      padding: '20px 30px', 
      width: '100%', 
      boxSizing: 'border-box',
      backgroundColor: '#f9f9f9'
    }}>
      <h1>Recursos Educacionais</h1>

      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        marginBottom: '20px',
        flexWrap: 'wrap',
        gap: '10px'
      }}>
        <Link to="/novo">
          <button style={{ ...buttonStyle, backgroundColor: '#2196F3' }}>
            ➕ Novo Recurso
          </button>
        </Link>
        <input
          type="text"
          placeholder="Buscar por título..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
          style={{ 
            width: '300px', 
            padding: '8px', 
            borderRadius: '4px', 
            border: '1px solid #ccc',
            maxWidth: '100%'
          }}
        />
      </div>

      {loading && <p>Carregando...</p>}

      {/* Tabela de recursos */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: '0 10px' }}>
          <thead>
            <tr style={{ backgroundColor: '#f2f2f2' }}>
              <th style={{ padding: '12px', textAlign: 'left' }}>Título</th>
              <th style={{ padding: '12px', textAlign: 'left' }}>Tipo</th>
              <th style={{ padding: '12px', textAlign: 'left' }}>Ações</th>
            </tr>
          </thead>
          <tbody>
            {recursos.map((r) => (
              <tr key={r.id} style={{ 
                boxShadow: '0 2px 5px rgba(0,0,0,0.1)', 
                borderRadius: '8px', 
                backgroundColor: 'white' 
              }}>
                <td style={{ padding: '12px', borderTopLeftRadius: '8px', borderBottomLeftRadius: '8px' }}>
                  {r.titulo}
                </td>
                <td style={{ padding: '12px' }}>{r.tipo}</td>
                <td style={{ padding: '12px', borderTopRightRadius: '8px', borderBottomRightRadius: '8px' }}>
                  <Link to={`/editar/${r.id}`}>
                    <button 
                      style={buttonStyle}
                      onMouseEnter={(e) => e.target.style.backgroundColor = '#45a049'}
                      onMouseLeave={(e) => e.target.style.backgroundColor = '#4CAF50'}
                    >
                      ✏️ Editar
                    </button>
                  </Link>
                  <button
                    onClick={() => handleDelete(r.id)}
                    style={{ ...buttonStyle, backgroundColor: '#f44336', marginLeft: '5px' }}
                    onMouseEnter={(e) => e.target.style.backgroundColor = '#d32f2f'}
                    onMouseLeave={(e) => e.target.style.backgroundColor = '#f44336'}
                  >
                    🗑️ Excluir
                  </button>
                </td>
              </tr>
            ))}
            {recursos.length === 0 && !loading && (
              <tr>
                <td colSpan="3" style={{ textAlign: 'center', padding: '20px' }}>
                  Nenhum recurso encontrado.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Paginação */}
      {totalPages > 1 && (
        <div style={{ 
          marginTop: '20px', 
          display: 'flex', 
          justifyContent: 'center', 
          gap: '10px',
          alignItems: 'center'
        }}>
          <button 
            disabled={page <= 1} 
            onClick={() => setPage(page - 1)}
            style={page <= 1 ? { ...buttonStyle, backgroundColor: '#ccc', cursor: 'not-allowed' } : buttonStyle}
          >
            Anterior
          </button>
          <span>
            Página {page} de {totalPages}
          </span>
          <button 
            disabled={page >= totalPages} 
            onClick={() => setPage(page + 1)}
            style={page >= totalPages ? { ...buttonStyle, backgroundColor: '#ccc', cursor: 'not-allowed' } : buttonStyle}
          >
            Próxima
          </button>
        </div>
      )}
    </div>
  );
}