from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Recordatorio(Base):
    __tablename__ = "recordatorios"

    id_recordatorio = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota"), nullable=False)

    tipo = Column(String(50), nullable=False)  # ej: "medicamento", "vacuna", "cita", "otro"
    descripcion = Column(Text, nullable=True)
    fecha_programada = Column(Date, nullable=False)
    frecuencia = Column(String(50), nullable=True)  # ej: "unica", "diaria", "semanal", "mensual"
    notificado = Column(Boolean, nullable=False, default=False)

    mascota = relationship("Mascota", backref="recordatorios")


class Medicamento(Base):
    __tablename__ = "medicamentos"

    id_medicamento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota"), nullable=False)
    id_recordatorio = Column(Integer, ForeignKey("recordatorios.id_recordatorio"), nullable=True)

    nombre = Column(String(150), nullable=False)
    dosis = Column(String(100), nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    observaciones = Column(Text, nullable=True)

    mascota = relationship("Mascota", backref="medicamentos")
    recordatorio = relationship("Recordatorio", backref="medicamentos")


class Vacuna(Base):
    __tablename__ = "vacunas"

    id_vacuna = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota"), nullable=False)
    id_recordatorio = Column(Integer, ForeignKey("recordatorios.id_recordatorio"), nullable=True)

    nombre = Column(String(150), nullable=False)
    fecha_aplicacion = Column(Date, nullable=True)
    fecha_proxima_dosis = Column(Date, nullable=True)
    observaciones = Column(Text, nullable=True)

    mascota = relationship("Mascota", backref="vacunas")
    recordatorio = relationship("Recordatorio", backref="vacunas")