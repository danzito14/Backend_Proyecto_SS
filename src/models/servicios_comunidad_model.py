from sqlalchemy import Column, String, Text, TIMESTAMP, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from src.core.db_credentials import Base

# ##############################################################################################################
# Modelos de Servicios de Comunidad
# ##############################################################################################################

class ServicioComunidad(Base):
    __tablename__ = 'servicios_comunidad'

    id_servicio_comunidad = Column(String(36), primary_key=True)
    titulo_servicio = Column(String(100), nullable=False)
    descripcion = Column(Text)
    direccion = Column(String(255))
    email = Column(String(100))
    telefono = Column(String(15))
    imagen_url = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    estatus = Column(Boolean, default=True)

    # Relación
    imagenes = relationship("ImagenServicioComunidad", back_populates="servicio_comunidad",
                            cascade="all, delete-orphan")

"""
class ImagenServicioComunidad(Base):
    __tablename__ = 'imagenes_servicios_comunidad'

    id_imagen = Column(String(36), primary_key=True)
    id_servicio_comunidad = Column(String(36),
                                   ForeignKey('servicios_comunidad.id_servicio_comunidad', ondelete='CASCADE'),
                                   nullable=False)
    imagen_url = Column(Text)
    descripcion = Column(String(255))
    estatus = Column(Enum('publica', 'privada'), default='publica')
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relación
    servicio_comunidad = relationship("ServicioComunidad", back_populates="imagenes")
"""