from typing import Optional, List
from pydantic import BaseModel
from enum import Enum
from .models import Tipo
from datetime import datetime

class RecursoBase(BaseModel):
    titulo: str 
    descricao: Optional[str] = None
    tipo: Tipo
    link: Optional[str] = None
    tags: Optional[str] = None

class RecursoCreate(RecursoBase):
    pass

class RecursoUpdate(RecursoBase):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    tipo: Optional[Tipo] = None
    link: Optional[str] = None
    tags: Optional[str] = None

    class Config:
        from_attributes = True

class RecursoResponse(RecursoBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: List[RecursoResponse]


class IASolicitacao(BaseModel):
    titulo: str
    tipo: Tipo

class IAResponse(BaseModel):
    descricao: str
    tags: str  