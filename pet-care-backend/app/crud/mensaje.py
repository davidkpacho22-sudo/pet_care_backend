from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.models.mensaje import Mensaje
from app.schemas.mensaje import MensajeCreate


def create_mensaje(db: Session, data: MensajeCreate, id_remitente: int) -> Mensaje:
    nuevo = Mensaje(**data.model_dump(), id_remitente=id_remitente)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def get_conversacion(db: Session, id_usuario_actual: int, id_otro_usuario: int) -> List[Mensaje]:
    """Todos los mensajes entre dos usuarios, en cualquier dirección, ordenados por fecha."""
    return (
        db.query(Mensaje)
        .filter(
            or_(
                and_(Mensaje.id_remitente == id_usuario_actual, Mensaje.id_destinatario == id_otro_usuario),
                and_(Mensaje.id_remitente == id_otro_usuario, Mensaje.id_destinatario == id_usuario_actual),
            )
        )
        .order_by(Mensaje.fecha_envio.asc())
        .all()
    )


def get_mensaje(db: Session, id_mensaje: int):
    return db.query(Mensaje).filter(Mensaje.id_mensaje == id_mensaje).first()


def marcar_como_leido(db: Session, mensaje: Mensaje) -> Mensaje:
    mensaje.leido = True
    db.commit()
    db.refresh(mensaje)
    return mensaje