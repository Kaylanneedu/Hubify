#  Hubify - Hub Inteligente de Recursos Educacionais

##  Descrição

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

###  Integrações
- Gemini API (IA para geração de descrição e tags)

###  Ferramentas
- Git
- GitHub

---
# Como Rodar o Projeto

## Clonar o Repositório

git clone https://github.com/seuusuario/hubify.git
cd hubify 

#Configurar arquivos de ambiente(na raiz do projeto) e edite as variavel com a sua chave de API onde é ordenado e tambem no url do front normalmente 
copy .env.exemplo backend\.env
copy .env.exemplo.front frontend\.env

#Configurar Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload 

#Configurar Frontend
cd frontend
npm install
npm run dev



