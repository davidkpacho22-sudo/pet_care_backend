from sqlalchemy import Column, Integer, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Mensaje(Base):
    __tablename__ = "mensajes"

    id_mensaje = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_remitente = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_destinatario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria"), nullable=True)
    id_cita = Column(Integer, ForeignKey("citas_veterinarias.id_cita"), nullable=True)

    contenido = Column(Text, nullable=False)
    leido = Column(Boolean, nullable=False, default=False)
    fecha_envio = Column(DateTime(timezone=True), server_default=func.now())

    remitente = relationship("Usuario", foreign_keys=[id_remitente], backref="mensajes_enviados")
    destinatario = relationship("Usuario", foreign_keys=[id_destinatario], backref="mensajes_recibidos")
    veterinaria = relationship("Veterinaria", backref="mensajes")
    cita = relationship("CitaVeterinaria", backref="mensajes")