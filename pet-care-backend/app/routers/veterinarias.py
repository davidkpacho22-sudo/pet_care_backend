from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.veterinaria import (
    VeterinariaCreate, VeterinariaUpdate, VeterinariaResponse,
    ProfesionalCreate, ProfesionalUpdate, ProfesionalResponse,
    CitaVeterinariaCreate, CitaVeterinariaUpdate, CitaVeterinariaResponse,
)
from app.crud.veterinaria import (
    get_veterinaria, get_veterinarias, create_veterinaria, update_veterinaria, delete_veterinaria,
    get_profesional, get_profesionales_by_veterinaria, create_profesional, update_profesional, delete_profesional,
    get_cita, get_citas_by_mascota, create_cita, update_cita, delete_cita,
)
from app.crud.mascota import get_mascota

router = APIRouter(prefix="/veterinarias", tags=["Veterinarias"])


# ---------- Veterinaria (lectura pública, escritura requiere login) ----------
@router.get("/", response_model=List[VeterinariaResponse])
def listar_veterinarias(db: Session = Depends(get_db)):
    return get_veterinarias(db)


@router.get("/{id_veterinaria}", response_model=VeterinariaResponse)
def obtener_veterinaria(id_veterinaria: int, db: Session = Depends(get_db)):
    veterinaria = get_veterinaria(db, id_veterinaria)
    if not veterinaria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinaria no encontrada")
    return veterinaria


@router.post("/", response_model=VeterinariaResponse, status_code=status.HTTP_201_CREATED)
def crear_veterinaria(
    data: VeterinariaCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return create_veterinaria(db, data)


@router.patch("/{id_veterinaria}", response_model=VeterinariaResponse)
def actualizar_veterinaria(
    id_veterinaria: int,
    data: VeterinariaUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    veterinaria = get_veterinaria(db, id_veterinaria)
    if not veterinaria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinaria no encontrada")
    return update_veterinaria(db, veterinaria, data)


@router.delete("/{id_veterinaria}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_veterinaria(
    id_veterinaria: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    veterinaria = get_veterinaria(db, id_veterinaria)
    if not veterinaria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinaria no encontrada")
    delete_veterinaria(db, veterinaria)
    return None


# ---------- Profesionales (anidados bajo veterinaria) ----------
@router.get("/{id_veterinaria}/profesionales", response_model=List[ProfesionalResponse])
def listar_profesionales(id_veterinaria: int, db: Session = Depends(get_db)):
    return get_profesionales_by_veterinaria(db, id_veterinaria)


@router.post("/{id_veterinaria}/profesionales", response_model=ProfesionalResponse, status_code=status.HTTP_201_CREATED)
def crear_profesional(
    id_veterinaria: int,
    data: ProfesionalCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    veterinaria = get_veterinaria(db, id_veterinaria)
    if not veterinaria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinaria no encontrada")
    if data.id_veterinaria != id_veterinaria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id_veterinaria no coincide con la URL")
    return create_profesional(db, data)


@router.patch("/profesionales/{id_profesional}", response_model=ProfesionalResponse)
def actualizar_profesional(
    id_profesional: int,
    data: ProfesionalUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    profesional = get_profesional(db, id_profesional)
    if not profesional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesional no encontrado")
    return update_profesional(db, profesional, data)


@router.delete("/profesionales/{id_profesional}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_profesional(
    id_profesional: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    profesional = get_profesional(db, id_profesional)
    if not profesional:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesional no encontrado")
    delete_profesional(db, profesional)
    return None


# ---------- Citas veterinarias ----------
@router.post("/citas", response_model=CitaVeterinariaResponse, status_code=status.HTTP_201_CREATED)
def crear_cita(
    data: CitaVeterinariaCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    # Verifica que la mascota exista y sea del usuario autenticado
    mascota = get_mascota(db, data.id_mascota)
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
    if mascota.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre esta mascota")

    if not get_profesional(db, data.id_profesional):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profesional no encontrado")
    if not get_veterinaria(db, data.id_veterinaria):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinaria no encontrada")

    return create_cita(db, data)


@router.get("/citas/mascota/{id_mascota}", response_model=List[CitaVeterinariaResponse])
def listar_citas_de_mascota(
    id_mascota: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    mascota = get_mascota(db, id_mascota)
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
    if mascota.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre esta mascota")
    return get_citas_by_mascota(db, id_mascota)


@router.patch("/citas/{id_cita}", response_model=CitaVeterinariaResponse)
def actualizar_cita(
    id_cita: int,
    data: CitaVeterinariaUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    cita = get_cita(db, id_cita)
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    return update_cita(db, cita, data)


@router.delete("/citas/{id_cita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(
    id_cita: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    cita = get_cita(db, id_cita)
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    delete_cita(db, cita)
    return None