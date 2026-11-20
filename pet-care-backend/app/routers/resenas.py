from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.resena import ResenaCreate, ResenaUpdate, ResenaResponse
from app.crud.resena import get_resena, get_resenas_by_veterinaria, create_resena, update_resena, delete_resena
from app.crud.veterinaria import get_veterinaria
from app.crud.producto import get_pedido

router = APIRouter(prefix="/resenas", tags=["Reseñas"])


@router.get("/veterinaria/{id_veterinaria}", response_model=List[ResenaResponse])
def listar_resenas_de_veterinaria(id_veterinaria: int, db: Session = Depends(get_db)):
    """Lectura pública: cualquiera puede ver las reseñas de una veterinaria."""
    if not get_veterinaria(db, id_veterinaria):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinaria no encontrada")
    return get_resenas_by_veterinaria(db, id_veterinaria)


@router.post("/", response_model=ResenaResponse, status_code=status.HTTP_201_CREATED)
def crear_resena(
    data: ResenaCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    if not get_veterinaria(db, data.id_veterinaria):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinaria no encontrada")

    if data.id_pedido is not None:
        pedido = get_pedido(db, data.id_pedido)
        if not pedido:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
        if pedido.id_usuario != usuario_actual.id_usuario:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre este pedido")

    return create_resena(db, data, id_usuario=usuario_actual.id_usuario)


@router.patch("/{id_resena}", response_model=ResenaResponse)
def actualizar_resena(
    id_resena: int,
    data: ResenaUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    resena = get_resena(db, id_resena)
    if not resena:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reseña no encontrada")
    if resena.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre esta reseña")
    return update_resena(db, resena, data)


@router.delete("/{id_resena}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_resena(
    id_resena: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    resena = get_resena(db, id_resena)
    if not resena:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reseña no encontrada")
    if resena.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre esta reseña")
    delete_resena(db, resena)
    return None