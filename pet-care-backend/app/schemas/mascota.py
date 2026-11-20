from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MascotaBase(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str] = None
    peso: Optional[Decimal] = None
    fecha_nacimiento: Optional[date] = None
    chip: Optional[str] = None
    alergias: Optional[str] = None
    condiciones_medicas: Optional[str] = None


class MascotaCreate(MascotaBase):
    """Datos que el cliente envía para crear una mascota (el dueño se toma del token JWT)."""
    pass


class MascotaUpdate(BaseModel):
    """Todos los campos opcionales, para permitir actualizaciones parciales."""
    nombre: Optional[str] = None
    especie: Optional[str] = None
    raza: Optional[str] = None
    peso: Optional[Decimal] = None
    fecha_nacimiento: Optional[date] = None
    chip: Optional[str] = None
    alergias: Optional[str] = None
    condiciones_medicas: Optional[str] = None


class MascotaResponse(MascotaBase):
    id_mascota: int
    id_usuario: int

    model_config = ConfigDict(from_attributes=True)