from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# ---------- Producto ----------
class ProductoBase(BaseModel):
    id_veterinaria: int
    nombre: str
    descripcion: Optional[str] = None
    precio_compra: Optional[Decimal] = None
    precio_venta: Decimal
    stock: int = 0


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_compra: Optional[Decimal] = None
    precio_venta: Optional[Decimal] = None
    stock: Optional[int] = None


class ProductoResponse(ProductoBase):
    id_producto: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Detalle Carrito ----------
class DetalleCarritoCreate(BaseModel):
    id_producto: int
    cantidad: int = 1


class DetalleCarritoResponse(BaseModel):
    id_detalle: int
    id_producto: int
    cantidad: int
    precio_unitario: Decimal

    model_config = ConfigDict(from_attributes=True)


# ---------- Carrito ----------
class CarritoResponse(BaseModel):
    id_carrito: int
    id_usuario: int
    fecha_creacion: Optional[datetime] = None
    detalles: List[DetalleCarritoResponse] = []

    model_config = ConfigDict(from_attributes=True)


# ---------- Pedido ----------
class PedidoCreate(BaseModel):
    id_carrito: int
    direccion_entrega: str
    metodo_pago: Optional[str] = None


class PedidoUpdate(BaseModel):
    estado: Optional[str] = None
    direccion_entrega: Optional[str] = None
    metodo_pago: Optional[str] = None


class PedidoResponse(BaseModel):
    id_pedido: int
    id_carrito: int
    id_usuario: int
    direccion_entrega: str
    estado: str
    metodo_pago: Optional[str] = None
    total: Decimal
    fecha_creacion: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)