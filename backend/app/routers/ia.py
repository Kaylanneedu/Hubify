from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger
from ..models import Tipo
from ..schemas import IAResponse, IASolicitacao
from ..services.ia_service import descricao_IA  

router = APIRouter(prefix="/ia", tags=["IA"])

@router.post("/sugestao", response_model=IAResponse)
async def sugerir_descricao(payload: IASolicitacao):
    try:
        resultado = await descricao_IA(payload.titulo, payload.tipo)
        
        tags_str = ", ".join(resultado["tags"])  
        logger.info(f"Sugestão gerada para título '{payload.titulo}'")
        return {"descricao": resultado["descricao"], "tags": tags_str}
    except Exception as e:
        logger.error(f"Falha ao gerar sugestão: {e}")
        raise HTTPException(status_code=503, detail="Serviço de IA indisponível no momento")