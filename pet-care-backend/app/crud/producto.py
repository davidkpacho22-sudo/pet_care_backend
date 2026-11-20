from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.producto import Producto, CarritoCompras, DetalleCarrito, Pedido
from app.schemas.producto import ProductoCreate, ProductoUpdate, PedidoCreate, PedidoUpdate


# ---------- Producto ----------
def get_producto(db: Session, id_producto: int) -> Optional[Producto]:
    return db.query(Producto).filter(Producto.id_producto == id_producto).first()


def get_productos(db: Session) -> List[Producto]:
    return db.query(Producto).all()


def get_productos_by_veterinaria(db: Session, id_veterinaria: int) -> List[Producto]:
    return db.query(Producto).filter(Producto.id_veterinaria == id_veterinaria).all()


def create_producto(db: Session, data: ProductoCreate) -> Producto:
    nuevo = Producto(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_producto(db: Session, producto: Producto, data: ProductoUpdate) -> Producto:
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return producto


def delete_producto(db: Session, producto: Producto) -> None:
    db.delete(producto)
    db.commit()


# ---------- Carrito ----------
def get_or_create_carrito_activo(db: Session, id_usuario: int) -> CarritoCompras:
    """
    Simplificación: un usuario tiene un solo 'carrito activo' a la vez,
    entendido como el carrito más reciente que aún no se ha convertido en pedido.
    """
    carrito = (
        db.query(CarritoCompras)
        .filter(CarritoCompras.id_usuario == id_usuario)
        .order_by(CarritoCompras.id_carrito.desc())
        .first()
    )
    # Si no existe carrito, o el último ya se usó en un pedido, creamos uno nuevo
    if carrito is None or db.query(Pedido).filter(Pedido.id_carrito == carrito.id_carrito).first():
        carrito = CarritoCompras(id_usuario=id_usuario)
        db.add(carrito)
        db.commit()
        db.refresh(carrito)
    return carrito


def get_carrito(db: Session, id_carrito: int) -> Optional[CarritoCompras]:
    return db.query(CarritoCompras).filter(CarritoCompras.id_carrito == id_carrito).first()


def agregar_producto_a_carrito(db: Session, carrito: CarritoCompras, producto: Producto, cantidad: int) -> DetalleCarrito:
    # Si el producto ya está en el carrito, aumentamos la cantidad
    detalle = (
        db.query(DetalleCarrito)
        .filter(DetalleCarrito.id_carrito == carrito.id_carrito, DetalleCarrito.id_producto == producto.id_producto)
        .first()
    )
    if detalle:
        detalle.cantidad += cantidad
    else:
        detalle = DetalleCarrito(
            id_carrito=carrito.id_carrito,
            id_producto=producto.id_producto,
            cantidad=cantidad,
            precio_unitario=producto.precio_venta,
        )
        db.add(detalle)
    db.commit()
    db.refresh(detalle)
    return detalle


def eliminar_detalle_carrito(db: Session, detalle: DetalleCarrito) -> None:
    db.delete(detalle)
    db.commit()


# ---------- Pedido ----------
def crear_pedido_desde_carrito(db: Session, carrito: CarritoCompras, data: PedidoCreate) -> Pedido:
    total = sum(detalle.cantidad * detalle.precio_unitario for detalle in carrito.detalles)

    # Descontar stock de cada producto
    for detalle in carrito.detalles:
        producto = db.query(Producto).filter(Producto.id_producto == detalle.id_producto).first()
        if producto:
            producto.stock = max(0, producto.stock - detalle.cantidad)

    nuevo_pedido = Pedido(
        id_carrito=carrito.id_carrito,
        id_usuario=carrito.id_usuario,
        direccion_entrega=data.direccion_entrega,
        metodo_pago=data.metodo_pago,
        total=total,
    )
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    return nuevo_pedido


def get_pedido(db: Session, id_pedido: int) -> Optional[Pedido]:
    return db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()


def get_pedidos_by_usuario(db: Session, id_usuario: int) -> List[Pedido]:
    return db.query(Pedido).filter(Pedido.id_usuario == id_usuario).all()


def update_pedido(db: Session, pedido: Pedido, data: PedidoUpdate) -> Pedido:
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(pedido, campo, valor)
    db.commit()
    db.refresh(pedido)
    return pedido