from sqlmodel import Session, select
from sqlalchemy import or_
from typing import Optional
from . import models, schemas


def get_recurso(session: Session, recurso_id: int):
    """Retorna um recurso"""
    return session.get(models.Recurso, recurso_id)

def get_recursos(session: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None):
    """Retorna varios recursos"""
    query = select(models.Recurso)
    if search:
        query = query.where(
            or_(
                models.Recurso.titulo.contains(search),
                models.Recurso.descricao.contains(search),
                models.Recurso.tags.contains(search)
            )
        )
    total = len(session.exec(query).all())
    
    items = session.exec(query.offset(skip).limit(limit)).all() # Aplica paginação
    return {
        "total": total,
        "page": (skip // limit) + 1,
        "per_page": limit,
        "items": items
    }

def create_recurso(session: Session, recurso: schemas.RecursoCreate):
    """Cria um recurso"""
    db_recurso = models.Recurso(**recurso.model_dump())
    session.add(db_recurso)
    session.commit()
    session.refresh(db_recurso)
    return db_recurso

def update_recurso(session: Session, recurso_id: int, recurso: schemas.RecursoUpdate):
    """Atualiza um recurso existente."""
    db_recurso = session.get(models.Recurso, recurso_id)
    if not db_recurso:
        return None
    update_data = recurso.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_recurso, key, value)
    session.add(db_recurso)
    session.commit()
    session.refresh(db_recurso)
    return db_recurso

def delete_recurso(session: Session, recurso_id: int):
    """deleta um recurso"""
    db_recurso = session.get(models.Recurso, recurso_id)
    if db_recurso:
        session.delete(db_recurso)
        session.commit()
        return True
    return False

    