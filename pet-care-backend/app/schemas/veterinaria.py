from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ---------- Veterinaria ----------
class VeterinariaBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None


class VeterinariaCreate(VeterinariaBase):
    pass


class VeterinariaUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None


class VeterinariaResponse(VeterinariaBase):
    id_veterinaria: int
    calificacion_promedio: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)


# ---------- Profesional ----------
class ProfesionalBase(BaseModel):
    nombre_completo: str
    especialidad: Optional[str] = None
    numero_registro: Optional[str] = None


class ProfesionalCreate(ProfesionalBase):
    id_veterinaria: int


class ProfesionalUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    especialidad: Optional[str] = None
    numero_registro: Optional[str] = None


class ProfesionalResponse(ProfesionalBase):
    id_profesional: int
    id_veterinaria: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Cita Veterinaria ----------
class CitaVeterinariaBase(BaseModel):
    id_mascota: int
    id_profesional: int
    id_veterinaria: int
    fecha: datetime
    motivo: Optional[str] = None


class CitaVeterinariaCreate(CitaVeterinariaBase):
    pass


class CitaVeterinariaUpdate(BaseModel):
    fecha: Optional[datetime] = None
    estado: Optional[str] = None
    motivo: Optional[str] = None


class CitaVeterinariaResponse(CitaVeterinariaBase):
    id_cita: int
    estado: str
    fecha_creacion: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)