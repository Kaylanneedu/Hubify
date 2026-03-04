from sqlmodel import Field, SQLModel
from enum import Enum
from typing import Optional
from datetime import datetime

class Tipo(str, Enum):
    video = "video"
    pdf = "pdf"
    link = "link"

class Recurso(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(max_length = 200)
    descricao: Optional[str] = None
    tipo: Tipo
    link: Optional[str] = Field(default=None, max_length=500)
    tags: Optional[str] = None

    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow,
                                           sa_column_kwargs={"onupdate": datetime.utcnow})