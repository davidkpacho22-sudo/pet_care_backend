from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.recordatorio import (
    RecordatorioCreate, RecordatorioUpdate, RecordatorioResponse,
    MedicamentoCreate, MedicamentoUpdate, MedicamentoResponse,
    VacunaCreate, VacunaUpdate, VacunaResponse,
)
from app.crud.recordatorio import (
    get_recordatorio, get_recordatorios_by_mascota, create_recordatorio, update_recordatorio, delete_recordatorio,
    get_medicamento, get_medicamentos_by_mascota, create_medicamento, update_medicamento, delete_medicamento,
    get_vacuna, get_vacunas_by_mascota, create_vacuna, update_vacuna, delete_vacuna,
)
from app.crud.mascota import get_mascota

router = APIRouter(prefix="/recordatorios", tags=["Recordatorios"])


def _verificar_mascota_propia(db: Session, id_mascota: int, usuario_actual: Usuario):
    """Verifica que la mascota exista y pertenezca al usuario autenticado."""
    mascota = get_mascota(db, id_mascota)
    if not mascota:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada")
    if mascota.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre esta mascota")
    return mascota


# ---------- Recordatorios ----------
@router.post("/", response_model=RecordatorioResponse, status_code=status.HTTP_201_CREATED)
def crear_recordatorio(
    data: RecordatorioCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    _verificar_mascota_propia(db, data.id_mascota, usuario_actual)
    return create_recordatorio(db, data)


@router.get("/mascota/{id_mascota}", response_model=List[RecordatorioResponse])
def listar_recordatorios_de_mascota(
    id_mascota: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    _verificar_mascota_propia(db, id_mascota, usuario_actual)
    return get_recordatorios_by_mascota(db, id_mascota)


@router.patch("/{id_recordatorio}", response_model=RecordatorioResponse)
def actualizar_recordatorio(
    id_recordatorio: int,
    data: RecordatorioUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    recordatorio = get_recordatorio(db, id_recordatorio)
    if not recordatorio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recordatorio no encontrado")
    _verificar_mascota_propia(db, recordatorio.id_mascota, usuario_actual)
    return update_recordatorio(db, recordatorio, data)


@router.delete("/{id_recordatorio}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_recordatorio(
    id_recordatorio: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    recordatorio = get_recordatorio(db, id_recordatorio)
    if not recordatorio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recordatorio no encontrado")
    _verificar_mascota_propia(db, recordatorio.id_mascota, usuario_actual)
    delete_recordatorio(db, recordatorio)
    return None


# ---------- Medicamentos ----------
@router.post("/medicamentos", response_model=MedicamentoResponse, status_code=status.HTTP_201_CREATED)
def crear_medicamento(
    data: MedicamentoCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    _verificar_mascota_propia(db, data.id_mascota, usuario_actual)
    return create_medicamento(db, data)


@router.get("/medicamentos/mascota/{id_mascota}", response_model=List[MedicamentoResponse])
def listar_medicamentos_de_mascota(
    id_mascota: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    _verificar_mascota_propia(db, id_mascota, usuario_actual)
    return get_medicamentos_by_mascota(db, id_mascota)


@router.patch("/medicamentos/{id_medicamento}", response_model=MedicamentoResponse)
def actualizar_medicamento(
    id_medicamento: int,
    data: MedicamentoUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    medicamento = get_medicamento(db, id_medicamento)
    if not medicamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicamento no encontrado")
    _verificar_mascota_propia(db, medicamento.id_mascota, usuario_actual)
    return update_medicamento(db, medicamento, data)


@router.delete("/medicamentos/{id_medicamento}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_medicamento(
    id_medicamento: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    medicamento = get_medicamento(db, id_medicamento)
    if not medicamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medicamento no encontrado")
    _verificar_mascota_propia(db, medicamento.id_mascota, usuario_actual)
    delete_medicamento(db, medicamento)
    return None


# ---------- Vacunas ----------
@router.post("/vacunas", response_model=VacunaResponse, status_code=status.HTTP_201_CREATED)
def crear_vacuna(
    data: VacunaCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    _verificar_mascota_propia(db, data.id_mascota, usuario_actual)
    return create_vacuna(db, data)


@router.get("/vacunas/mascota/{id_mascota}", response_model=List[VacunaResponse])
def listar_vacunas_de_mascota(
    id_mascota: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    _verificar_mascota_propia(db, id_mascota, usuario_actual)
    return get_vacunas_by_mascota(db, id_mascota)


@router.patch("/vacunas/{id_vacuna}", response_model=VacunaResponse)
def actualizar_vacuna(
    id_vacuna: int,
    data: VacunaUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    vacuna = get_vacuna(db, id_vacuna)
    if not vacuna:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacuna no encontrada")
    _verificar_mascota_propia(db, vacuna.id_mascota, usuario_actual)
    return update_vacuna(db, vacuna, data)


@router.delete("/vacunas/{id_vacuna}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_vacuna(
    id_vacuna: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    vacuna = get_vacuna(db, id_vacuna)
    if not vacuna:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacuna no encontrada")
    _verificar_mascota_propia(db, vacuna.id_mascota, usuario_actual)
    delete_vacuna(db, vacuna)
    return None