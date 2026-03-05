# Hubify - Hub Inteligente de Recursos Educacionais

## Descrição

O **Hubify** é um projeto Fullstack desenvolvido para gerenciamento de recursos educacionais.

O sistema permite:

- ✅ Criar recursos
- ✅ Listar com paginação
- ✅ Buscar por título, descrição ou tags
- ✅ Editar recursos
- ✅ Excluir recursos
- ✅ Gerar automaticamente descrição e tags usando Inteligência Artificial (Gemini API)

---

## Tecnologias Utilizadas

### Backend
- Python
- FastAPI
- SQLite
- Uvicorn

### Frontend
- React
- JavaScript
- CSS

### Integrações
- Gemini API (IA para geração de descrição e tags)

### Ferramentas
- Git
- GitHub

---

# Como Rodar o Projeto

## Clonar o Repositório

```bash
git clone https://github.com/seuusuario/hubify.git
cd hubify
```

## Configurar Arquivos de Ambiente

Copie os arquivos de exemplo e edite as variáveis com sua chave da API e a URL do frontend.

```bash
copy .env.exemplo backend\.env
copy .env.exemplo.front frontend\.env
```

Exemplo de variável no backend (.env):

```env
GEMINI_API_KEY=sua_chave_aqui
FRONTEND_URL=http://localhost:5173
```

## Configurar Backend

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Configurar Frontend

```bash
cd frontend
npm install
npm run dev
```
