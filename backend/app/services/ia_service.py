import google.generativeai as genai
import os
import json
import time
from loguru import logger
from ..config import settings
from ..models import Tipo

async def descricao_IA(titulo: str, tipo: Tipo):
    """Gera uma descrIção de um recurso educacional usando IA Gemini
       Retorna um dicionario com 'descrição' e 'tags'
    """
    if not settings.GEMINI_API_KEY:
        logger.warning("Chave Gemini não configurada. Usando modo simulação")
        return {
            "descricao": f"Simulação: Descrição para '{titulo}' do tipo '{tipo}'",
            "tags": ["simulacao"]
        }
    
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""

    Voce é um assistente pedagógico de IA da API Hubify. Seu trabalho
    é gerar uma descrição curta e precisa com no (máximo 300 caracteres) 
    sobre um recurso educacional com base nos recursos:

    Titulo: {titulo} 
    Tipo: {tipo} 
  
    Lembre que a resposta deve ser APENAS com um objeto JSON válido no formato:
    {{
        "descricao": "Aqui vai a descrição gerada pela IA",
        "tags": ["tag1", "tag2", "tag3"]
    }}

    As tags devem ser funcionais e exatamente 3.
    Não inclua nada adicional que não foi pedido, nem Markdown.
    """

    try:
        start = time.time()
        import asyncio
        response = await asyncio.to_thread(model.generate_content, prompt)
        latency = time.time() - start

        # Extrair texto e remover possíveis marcações de código
        texto = response.text
        texto = texto.replace('```json', '').replace('```', '').strip()

        # Tentar parsear JSON
        resultado = json.loads(texto)

        # Validar se tem os campos esperados
        if "descricao" not in resultado or "tags" not in resultado:
            raise ValueError("Resposta da IA não contém os campos esperados")

        # Log estruturado
        logger.info(f"IA Request | Título={titulo} | Latência={latency:.2f}s | Tokens={response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 'N/A'}")

        return resultado

    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON da IA: {e}. Resposta recebida: {texto if 'texto' in locals() else 'N/A'}")
        # Fallback para simulação
        return {
            "descricao": f"Descrição para {titulo} (falha na IA)",
            "tags": [titulo.split()[0].lower(), tipo.value, "fallback"]
        }
    except Exception as e:
        logger.error(f"Erro na chamada da IA: {e}")
        return {
            "descricao": f"Descrição para {titulo} (erro)",
            "tags": [titulo.split()[0].lower(), tipo.value, "erro"]}