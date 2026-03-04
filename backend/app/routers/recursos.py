from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import Optional
from .. import crud, schemas
from ..database import get_session

router = APIRouter(prefix="/recursos", tags=["Recursos"])

@router.get("/", response_model=schemas.PaginatedResponse)
async def listar_recursos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """Lista todos os recursos com paginação e busca opcional"""
    return crud.get_recursos(session, skip=skip, limit=limit, search=search)

@router.get("/{recurso_id}", response_model=schemas.RecursoResponse)
async def obter_recurso(recurso_id: int,session: Session = Depends(get_session)):
    """retorna recurso específico"""
    db_recurso = crud.get_recurso(session, recurso_id)
    if not db_recurso:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    return db_recurso

@router.post("/", response_model=schemas.RecursoResponse)
async def create_recurso(recurso: schemas.RecursoCreate, session: Session = Depends(get_session)):
    """Cria um recurso"""
    return crud.create_recurso(session, recurso)

@router.put("/{recurso_id}", response_model=schemas.RecursoResponse)
async def update_recurso(recurso_id: int,recurso: schemas.RecursoUpdate, session: Session = Depends(get_session)):
    """Atualiza um recurso"""
    db_recurso = crud.update_recurso(session, recurso_id, recurso)
    if not db_recurso:
        raise HTTPException(status_code=404, detail="Recurso não encontrado para atualização")
    
    return db_recurso

@router.delete("/{recurso_id}")
async def delete_recurso(recurso_id: int, session: Session = Depends(get_session)):
    """Deleta recurso"""
    deletado = crud.delete_recurso(session, recurso_id)
    if not deletado:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    
    return {"message": "Recurso deletado com sucesso"}