from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.resena import Resena
from app.models.veterinaria import Veterinaria
from app.schemas.resena import ResenaCreate, ResenaUpdate


def get_resena(db: Session, id_resena: int) -> Optional[Resena]:
    return db.query(Resena).filter(Resena.id_resena == id_resena).first()


def get_resenas_by_veterinaria(db: Session, id_veterinaria: int) -> List[Resena]:
    return db.query(Resena).filter(Resena.id_veterinaria == id_veterinaria).all()


def _actualizar_calificacion_promedio(db: Session, id_veterinaria: int) -> None:
    """Recalcula y guarda el promedio de calificaciones de una veterinaria."""
    promedio = (
        db.query(func.avg(Resena.calificacion))
        .filter(Resena.id_veterinaria == id_veterinaria)
        .scalar()
    )
    veterinaria = db.query(Veterinaria).filter(Veterinaria.id_veterinaria == id_veterinaria).first()
    if veterinaria:
        veterinaria.calificacion_promedio = round(promedio, 2) if promedio is not None else 0
        db.commit()


def create_resena(db: Session, data: ResenaCreate, id_usuario: int) -> Resena:
    nueva = Resena(**data.model_dump(), id_usuario=id_usuario)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    _actualizar_calificacion_promedio(db, data.id_veterinaria)
    return nueva


def update_resena(db: Session, resena: Resena, data: ResenaUpdate) -> Resena:
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(resena, campo, valor)
    db.commit()
    db.refresh(resena)
    _actualizar_calificacion_promedio(db, resena.id_veterinaria)
    return resena


def delete_resena(db: Session, resena: Resena) -> None:
    id_veterinaria = resena.id_veterinaria
    db.delete(resena)
    db.commit()
    _actualizar_calificacion_promedio(db, id_veterinaria)