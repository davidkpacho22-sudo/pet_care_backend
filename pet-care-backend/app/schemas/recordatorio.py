from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ---------- Recordatorio ----------
class RecordatorioBase(BaseModel):
    id_mascota: int
    tipo: str
    descripcion: Optional[str] = None
    fecha_programada: date
    frecuencia: Optional[str] = None


class RecordatorioCreate(RecordatorioBase):
    pass


class RecordatorioUpdate(BaseModel):
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_programada: Optional[date] = None
    frecuencia: Optional[str] = None
    notificado: Optional[bool] = None


class RecordatorioResponse(RecordatorioBase):
    id_recordatorio: int
    notificado: bool

    model_config = ConfigDict(from_attributes=True)


# ---------- Medicamento ----------
class MedicamentoBase(BaseModel):
    id_mascota: int
    id_recordatorio: Optional[int] = None
    nombre: str
    dosis: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    observaciones: Optional[str] = None


class MedicamentoCreate(MedicamentoBase):
    pass


class MedicamentoUpdate(BaseModel):
    nombre: Optional[str] = None
    dosis: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    observaciones: Optional[str] = None
    id_recordatorio: Optional[int] = None


class MedicamentoResponse(MedicamentoBase):
    id_medicamento: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Vacuna ----------
class VacunaBase(BaseModel):
    id_mascota: int
    id_recordatorio: Optional[int] = None
    nombre: str
    fecha_aplicacion: Optional[date] = None
    fecha_proxima_dosis: Optional[date] = None
    observaciones: Optional[str] = None


class VacunaCreate(VacunaBase):
    pass


class VacunaUpdate(BaseModel):
    nombre: Optional[str] = None
    fecha_aplicacion: Optional[date] = None
    fecha_proxima_dosis: Optional[date] = None
    observaciones: Optional[str] = None
    id_recordatorio: Optional[int] = None


class VacunaResponse(VacunaBase):
    id_vacuna: int

    model_config = ConfigDict(from_attributes=True)