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
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"""
    Você é um assistente pedagógico. Gere uma descrição curta (máx 300 caracteres) 
    e 3 tags para um recurso educacional com título "{titulo}" e tipo "{tipo}".

    A resposta deve ser APENAS um objeto JSON válido no formato:
    {{"descricao": "descrição aqui", "tags": ["tag1", "tag2", "tag3"]}}

    Não inclua nenhum texto adicional, nem markdown.
    """

    try:
        start = time.time()
        import asyncio
        response = await asyncio.to_thread(model.generate_content, prompt)
        latency = time.time() - start

        texto = response.text
        texto = texto.replace('```json', '').replace('```', '').strip()

        resultado = json.loads(texto)

        if "descricao" not in resultado or "tags" not in resultado:
            raise ValueError("Resposta da IA não contém os campos esperados")

        # Log estruturado
        logger.info(f"IA Request | Título={titulo} | Latência={latency:.2f}s | Tokens={response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 'N/A'}")

        return resultado

    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON da IA: {e}. Resposta recebida: {texto if 'texto' in locals() else 'N/A'}")
        return {
            "descricao": f"Descrição para {titulo} (falha na IA)",
            "tags": [titulo.split()[0].lower(), tipo.value, "fallback"]
        }
    except Exception as e:
        logger.error(f"Erro na chamada da IA: {type(e).__name__} - {str(e)}")
        return {
            "descricao": f"Descrição para {titulo} (erro)",
            "tags": [titulo.split()[0].lower(), tipo.value, "erro"]
        }