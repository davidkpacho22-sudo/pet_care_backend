from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario
from app.schemas.producto import (
    ProductoCreate, ProductoUpdate, ProductoResponse,
    DetalleCarritoCreate, CarritoResponse,
    PedidoCreate, PedidoUpdate, PedidoResponse,
)
from app.crud.producto import (
    get_producto, get_productos, get_productos_by_veterinaria, create_producto, update_producto, delete_producto,
    get_or_create_carrito_activo, get_carrito, agregar_producto_a_carrito, eliminar_detalle_carrito,
    crear_pedido_desde_carrito, get_pedido, get_pedidos_by_usuario, update_pedido,
)
from app.crud.veterinaria import get_veterinaria

router = APIRouter(tags=["Productos y Compras"])


# ---------- Productos (lectura pública, escritura requiere login) ----------
@router.get("/productos", response_model=List[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return get_productos(db)


@router.get("/productos/{id_producto}", response_model=ProductoResponse)
def obtener_producto(id_producto: int, db: Session = Depends(get_db)):
    producto = get_producto(db, id_producto)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return producto


@router.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(
    data: ProductoCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    if not get_veterinaria(db, data.id_veterinaria):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Veterinaria no encontrada")
    return create_producto(db, data)


@router.patch("/productos/{id_producto}", response_model=ProductoResponse)
def actualizar_producto(
    id_producto: int,
    data: ProductoUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    producto = get_producto(db, id_producto)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return update_producto(db, producto, data)


@router.delete("/productos/{id_producto}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    id_producto: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    producto = get_producto(db, id_producto)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    delete_producto(db, producto)
    return None


# ---------- Carrito (siempre del usuario autenticado) ----------
@router.get("/carrito", response_model=CarritoResponse)
def ver_mi_carrito(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    carrito = get_or_create_carrito_activo(db, usuario_actual.id_usuario)
    return carrito


@router.post("/carrito/items", response_model=CarritoResponse, status_code=status.HTTP_201_CREATED)
def agregar_item_al_carrito(
    data: DetalleCarritoCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    producto = get_producto(db, data.id_producto)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    if producto.stock < data.cantidad:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock insuficiente")

    carrito = get_or_create_carrito_activo(db, usuario_actual.id_usuario)
    agregar_producto_a_carrito(db, carrito, producto, data.cantidad)
    db.refresh(carrito)
    return carrito


@router.delete("/carrito/items/{id_detalle}", response_model=CarritoResponse)
def quitar_item_del_carrito(
    id_detalle: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    carrito = get_or_create_carrito_activo(db, usuario_actual.id_usuario)
    detalle = next((d for d in carrito.detalles if d.id_detalle == id_detalle), None)
    if not detalle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ítem no encontrado en tu carrito")
    eliminar_detalle_carrito(db, detalle)
    db.refresh(carrito)
    return carrito


# ---------- Pedidos ----------
@router.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    data: PedidoCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    carrito = get_carrito(db, data.id_carrito)
    if not carrito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")
    if carrito.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre este carrito")
    if not carrito.detalles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El carrito está vacío")

    return crear_pedido_desde_carrito(db, carrito, data)


@router.get("/pedidos", response_model=List[PedidoResponse])
def listar_mis_pedidos(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return get_pedidos_by_usuario(db, usuario_actual.id_usuario)


@router.get("/pedidos/{id_pedido}", response_model=PedidoResponse)
def obtener_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    pedido = get_pedido(db, id_pedido)
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    if pedido.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre este pedido")
    return pedido


@router.patch("/pedidos/{id_pedido}", response_model=PedidoResponse)
def actualizar_pedido(
    id_pedido: int,
    data: PedidoUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    pedido = get_pedido(db, id_pedido)
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    if pedido.id_usuario != usuario_actual.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso sobre este pedido")
    return update_pedido(db, pedido, data)