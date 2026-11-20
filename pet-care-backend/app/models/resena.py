from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Resena(Base):
    __tablename__ = "resenas"
    __table_args__ = (
        CheckConstraint("calificacion >= 1 AND calificacion <= 5", name="chk_calificacion_rango"),
    )

    id_resena = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria"), nullable=False)
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido"), nullable=True)

    calificacion = Column(Integer, nullable=False)  # 1 a 5
    comentario = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", backref="resenas")
    veterinaria = relationship("Veterinaria", backref="resenas")
    pedido = relationship("Pedido", backref="resenas")