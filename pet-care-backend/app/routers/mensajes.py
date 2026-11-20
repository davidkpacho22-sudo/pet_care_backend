from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.mensaje import MensajeCreate, MensajeResponse
from app.crud.mensaje import create_mensaje, get_conversacion, get_mensaje, marcar_como_leido
from app.crud.usuario import get_usuario_by_correo

router = APIRouter(prefix="/mensajes", tags=["Mensajería"])


@router.post("/", response_model=MensajeResponse, status_code=status.HTTP_201_CREATED)
def enviar_mensaje(
    data: MensajeCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    if data.id_destinatario == usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes enviarte un mensaje a ti mismo")

    return create_mensaje(db, data, id_remitente=usuario_actual.id_usuario)


@router.get("/conversacion/{id_otro_usuario}", response_model=List[MensajeResponse])
def ver_conversacion(
    id_otro_usuario: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    """Devuelve el hilo completo de mensajes entre el usuario autenticado y otro usuario."""
    return get_conversacion(db, usuario_actual.id_usuario, id_otro_usuario)


@router.patch("/{id_mensaje}/leido", response_model=MensajeResponse)
def marcar_mensaje_leido(
    id_mensaje: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    mensaje = get_mensaje(db, id_mensaje)
    if not mensaje:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensaje no encontrado")
    if mensaje.id_destinatario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo el destinatario puede marcarlo como leído")
    return marcar_como_leido(db, mensaje)