from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.recordatorio import Recordatorio, Medicamento, Vacuna
from app.schemas.recordatorio import (
    RecordatorioCreate, RecordatorioUpdate,
    MedicamentoCreate, MedicamentoUpdate,
    VacunaCreate, VacunaUpdate,
)


# ---------- Recordatorio ----------
def get_recordatorio(db: Session, id_recordatorio: int) -> Optional[Recordatorio]:
    return db.query(Recordatorio).filter(Recordatorio.id_recordatorio == id_recordatorio).first()


def get_recordatorios_by_mascota(db: Session, id_mascota: int) -> List[Recordatorio]:
    return db.query(Recordatorio).filter(Recordatorio.id_mascota == id_mascota).all()


def create_recordatorio(db: Session, data: RecordatorioCreate) -> Recordatorio:
    nuevo = Recordatorio(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_recordatorio(db: Session, recordatorio: Recordatorio, data: RecordatorioUpdate) -> Recordatorio:
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(recordatorio, campo, valor)
    db.commit()
    db.refresh(recordatorio)
    return recordatorio


def delete_recordatorio(db: Session, recordatorio: Recordatorio) -> None:
    db.delete(recordatorio)
    db.commit()


# ---------- Medicamento ----------
def get_medicamento(db: Session, id_medicamento: int) -> Optional[Medicamento]:
    return db.query(Medicamento).filter(Medicamento.id_medicamento == id_medicamento).first()


def get_medicamentos_by_mascota(db: Session, id_mascota: int) -> List[Medicamento]:
    return db.query(Medicamento).filter(Medicamento.id_mascota == id_mascota).all()


def create_medicamento(db: Session, data: MedicamentoCreate) -> Medicamento:
    nuevo = Medicamento(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_medicamento(db: Session, medicamento: Medicamento, data: MedicamentoUpdate) -> Medicamento:
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(medicamento, campo, valor)
    db.commit()
    db.refresh(medicamento)
    return medicamento


def delete_medicamento(db: Session, medicamento: Medicamento) -> None:
    db.delete(medicamento)
    db.commit()


# ---------- Vacuna ----------
def get_vacuna(db: Session, id_vacuna: int) -> Optional[Vacuna]:
    return db.query(Vacuna).filter(Vacuna.id_vacuna == id_vacuna).first()


def get_vacunas_by_mascota(db: Session, id_mascota: int) -> List[Vacuna]:
    return db.query(Vacuna).filter(Vacuna.id_mascota == id_mascota).all()


def create_vacuna(db: Session, data: VacunaCreate) -> Vacuna:
    nueva = Vacuna(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def update_vacuna(db: Session, vacuna: Vacuna, data: VacunaUpdate) -> Vacuna:
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(vacuna, campo, valor)
    db.commit()
    db.refresh(vacuna)
    return vacuna


def delete_vacuna(db: Session, vacuna: Vacuna) -> None:
    db.delete(vacuna)
    db.commit()