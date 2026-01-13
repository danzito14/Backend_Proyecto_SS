from sqlalchemy import Column, String, Text, TIMESTAMP, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.core.db_credentials import Base


# ##############################################################################################################
# Modelos de Servicios de Comercio
# ##############################################################################################################

class ServicioComercio(Base):
    __tablename__ = 'servicios_comercio'

    id_servicio = Column(String(36), primary_key=True)
    id_comercio = Column(String(36), ForeignKey('comercios.id_comercio', ondelete='CASCADE'), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)

    # Relaciones
    comercio = relationship("Comercio", back_populates="servicios")
    opciones = relationship("OpcionServicio", back_populates="servicio", cascade="all, delete-orphan")


class OpcionServicio(Base):
    __tablename__ = 'opciones_servicio'

    id_opcion_servicio = Column(String(36), primary_key=True)
    id_servicio = Column(String(36), ForeignKey('servicios_comercio.id_servicio', ondelete='CASCADE'), nullable=False)
    nombre_opcion = Column(String(100), nullable=False)
    descripcion = Column(Text)
    precio = Column(DECIMAL(10, 2), nullable=False)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)

    # Relaciones
    servicio = relationship("ServicioComercio", back_populates="opciones")
    imagenes = relationship("ImagenServicio", back_populates="opcion_servicio", cascade="all, delete-orphan")


"""class ImagenServicio(Base):
    __tablename__ = 'imagenes_servicios'

    id_imagen = Column(String(36), primary_key=True)
    id_opcion_servicio = Column(String(36), ForeignKey('opciones_servicio.id_opcion_servicio', ondelete='CASCADE'),
                                nullable=False)
    imagen_url = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relación
    opcion_servicio = relationship("OpcionServicio", back_populates="imagenes")
"""

