from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Veterinaria(Base):
    __tablename__ = "veterinarias"

    id_veterinaria = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    direccion = Column(Text, nullable=True)
    telefono = Column(String(20), nullable=True)
    latitud = Column(Numeric(10, 7), nullable=True)
    longitud = Column(Numeric(10, 7), nullable=True)
    calificacion_promedio = Column(Numeric(3, 2), nullable=True, default=0)

    profesionales = relationship("Profesional", back_populates="veterinaria")


class Profesional(Base):
    __tablename__ = "profesionales"

    id_profesional = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria"), nullable=False)

    nombre_completo = Column(String(100), nullable=False)
    especialidad = Column(String(100), nullable=True)
    numero_registro = Column(String(50), nullable=True)

    veterinaria = relationship("Veterinaria", back_populates="profesionales")


class CitaVeterinaria(Base):
    __tablename__ = "citas_veterinarias"

    id_cita = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota"), nullable=False)
    id_profesional = Column(Integer, ForeignKey("profesionales.id_profesional"), nullable=False)
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria"), nullable=False)

    fecha = Column(DateTime(timezone=True), nullable=False)
    estado = Column(String(30), nullable=False, default="pendiente")
    motivo = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    mascota = relationship("Mascota", backref="citas")
    profesional = relationship("Profesional", backref="citas")
    veterinaria = relationship("Veterinaria", backref="citas")