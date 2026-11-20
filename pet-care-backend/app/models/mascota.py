from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.database import Base


class Mascota(Base):
    __tablename__ = "mascotas"

    id_mascota = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    nombre = Column(String(100), nullable=False)
    especie = Column(String(50), nullable=False)
    raza = Column(String(50), nullable=True)
    peso = Column(Numeric(6, 2), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    chip = Column(String(50), nullable=True, unique=True)

    alergias = Column(Text, nullable=True)
    condiciones_medicas = Column(Text, nullable=True)

    # Relación inversa hacia el dueño
    dueno = relationship("Usuario", backref="mascotas")