from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria"), nullable=False)

    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio_compra = Column(Numeric(10, 2), nullable=True)
    precio_venta = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    veterinaria = relationship("Veterinaria", backref="productos")


class CarritoCompras(Base):
    __tablename__ = "carrito_compras"

    id_carrito = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", backref="carritos")
    detalles = relationship("DetalleCarrito", back_populates="carrito", cascade="all, delete-orphan")


class DetalleCarrito(Base):
    __tablename__ = "detalle_carrito"

    id_detalle = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_carrito = Column(Integer, ForeignKey("carrito_compras.id_carrito"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)

    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Numeric(10, 2), nullable=False)

    carrito = relationship("CarritoCompras", back_populates="detalles")
    producto = relationship("Producto", backref="detalles_carrito")


class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_carrito = Column(Integer, ForeignKey("carrito_compras.id_carrito"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    direccion_entrega = Column(Text, nullable=False)
    estado = Column(String(30), nullable=False, default="pendiente")
    metodo_pago = Column(String(50), nullable=True)
    total = Column(Numeric(10, 2), nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    carrito = relationship("CarritoCompras", backref="pedidos")
    usuario = relationship("Usuario", backref="pedidos")