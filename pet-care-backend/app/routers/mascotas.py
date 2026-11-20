from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.mascota import MascotaCreate, MascotaUpdate, MascotaResponse
from app.crud.mascota import (
    get_mascota,
    get_mascotas_by_usuario,
    create_mascota,
    update_mascota,
    delete_mascota,
)

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])


def _verificar_propietario(mascota, usuario_actual: Usuario):
    """Lanza 403 si la mascota no pertenece al usuario autenticado."""
    if mascota.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso sobre esta mascota",
        )


@router.post("/", response_model=MascotaResponse, status_code=status.HTTP_201_CREATED)
def crear_mascota(
    mascota_data: MascotaCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    """Crea una mascota asociada al usuario autenticado (id tomado del JWT, no del body)."""
    return create_mascota(db, mascota_data, id_usuario=usuario_actual.id_usuario)


@router.get("/", response_model=List[MascotaResponse])
def listar_mis_mascotas(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    """Lista solo las mascotas del usuario autenticado."""
    return get_mascotas_by_usuario(db, usuario_actual.id_usuario)


@router.get("/{id_mascota}", response_model=MascotaResponse)
def obtener_mascota(
    id_mascota: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    mascota = get_mascota(db, id_mascota)
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
    _verificar_propietario(mascota, usuario_actual)
    return mascota


@router.patch("/{id_mascota}", response_model=MascotaResponse)
def actualizar_mascota(
    id_mascota: int,
    mascota_data: MascotaUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    mascota = get_mascota(db, id_mascota)
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
    _verificar_propietario(mascota, usuario_actual)
    return update_mascota(db, mascota, mascota_data)


@router.delete("/{id_mascota}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mascota(
    id_mascota: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    mascota = get_mascota(db, id_mascota)
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
    _verificar_propietario(mascota, usuario_actual)
    delete_mascota(db, mascota)
    return None