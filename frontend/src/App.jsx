import { BrowserRouter, Routes, Route } from 'react-router-dom';
import TelaInicial from './pages/tela_inicial';
import CriarRecurso from './pages/criarRecurso';
import './App.css';

function Header() {
  return (
    <header style={{
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      padding: '15px 30px',
      backgroundColor: '#f5f5f5',
      borderBottom: '2px solid #4CAF50',
      width: '100%',
      boxSizing: 'border-box'
    }}>
      <span style={{ fontSize: '2rem' }}>📚</span>
      <h1 style={{ margin: 0, color: '#333' }}>Hubify</h1>
    </header>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<TelaInicial />} />
        <Route path="/novo" element={<CriarRecurso />} />
        <Route path="/editar/:id" element={<CriarRecurso />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;