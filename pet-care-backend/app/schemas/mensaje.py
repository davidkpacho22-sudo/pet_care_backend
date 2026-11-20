from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MensajeCreate(BaseModel):
    id_destinatario: int
    id_veterinaria: Optional[int] = None
    id_cita: Optional[int] = None
    contenido: str


class MensajeResponse(BaseModel):
    id_mensaje: int
    id_remitente: int
    id_destinatario: int
    id_veterinaria: Optional[int] = None
    id_cita: Optional[int] = None
    contenido: str
    leido: bool
    fecha_envio: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)