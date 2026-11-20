from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.veterinaria import Veterinaria, Profesional, CitaVeterinaria
from app.schemas.veterinaria import (
    VeterinariaCreate, VeterinariaUpdate,
    ProfesionalCreate, ProfesionalUpdate,
    CitaVeterinariaCreate, CitaVeterinariaUpdate,
)


# ---------- Veterinaria ----------
def get_veterinaria(db: Session, id_veterinaria: int) -> Optional[Veterinaria]:
    return db.query(Veterinaria).filter(Veterinaria.id_veterinaria == id_veterinaria).first()


def get_veterinarias(db: Session) -> List[Veterinaria]:
    return db.query(Veterinaria).all()


def create_veterinaria(db: Session, data: VeterinariaCreate) -> Veterinaria:
    nueva = Veterinaria(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def update_veterinaria(db: Session, veterinaria: Veterinaria, data: VeterinariaUpdate) -> Veterinaria:
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(veterinaria, campo, valor)
    db.commit()
    db.refresh(veterinaria)
    return veterinaria


def delete_veterinaria(db: Session, veterinaria: Veterinaria) -> None:
    db.delete(veterinaria)
    db.commit()


# ---------- Profesional ----------
def get_profesional(db: Session, id_profesional: int) -> Optional[Profesional]:
    return db.query(Profesional).filter(Profesional.id_profesional == id_profesional).first()


def get_profesionales_by_veterinaria(db: Session, id_veterinaria: int) -> List[Profesional]:
    return db.query(Profesional).filter(Profesional.id_veterinaria == id_veterinaria).all()


def create_profesional(db: Session, data: ProfesionalCreate) -> Profesional:
    nuevo = Profesional(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_profesional(db: Session, profesional: Profesional, data: ProfesionalUpdate) -> Profesional:
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(profesional, campo, valor)
    db.commit()
    db.refresh(profesional)
    return profesional


def delete_profesional(db: Session, profesional: Profesional) -> None:
    db.delete(profesional)
    db.commit()


# ---------- Cita Veterinaria ----------
def get_cita(db: Session, id_cita: int) -> Optional[CitaVeterinaria]:
    return db.query(CitaVeterinaria).filter(CitaVeterinaria.id_cita == id_cita).first()


def get_citas_by_mascota(db: Session, id_mascota: int) -> List[CitaVeterinaria]:
    return db.query(CitaVeterinaria).filter(CitaVeterinaria.id_mascota == id_mascota).all()


def create_cita(db: Session, data: CitaVeterinariaCreate) -> CitaVeterinaria:
    nueva = CitaVeterinaria(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def update_cita(db: Session, cita: CitaVeterinaria, data: CitaVeterinariaUpdate) -> CitaVeterinaria:
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(cita, campo, valor)
    db.commit()
    db.refresh(cita)
    return cita


def delete_cita(db: Session, cita: CitaVeterinaria) -> None:
    db.delete(cita)
    db.commit()