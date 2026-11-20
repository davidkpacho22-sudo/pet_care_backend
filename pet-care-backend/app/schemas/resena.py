from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ResenaBase(BaseModel):
    id_veterinaria: int
    id_pedido: Optional[int] = None
    calificacion: int = Field(ge=1, le=5)
    comentario: Optional[str] = None


class ResenaCreate(ResenaBase):
    pass


class ResenaUpdate(BaseModel):
    calificacion: Optional[int] = Field(default=None, ge=1, le=5)
    comentario: Optional[str] = None


class ResenaResponse(ResenaBase):
    id_resena: int
    id_usuario: int
    fecha_creacion: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)