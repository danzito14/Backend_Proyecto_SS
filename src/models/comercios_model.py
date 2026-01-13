from sqlalchemy import Column, Integer, String, Text, Numeric, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.core.db_credentials import Base

# ##############################################################################################################
# Categorías de Comercio
# ##############################################################################################################

class CategoriaComercio(Base):
    __tablename__ = 'categorias_comercio'

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre_categoria = Column(String(50), nullable=False)
    color_hex = Column(String(7))

    comercios = relationship("Comercio", back_populates="categoria")


# ##############################################################################################################
# Comercios
# ##############################################################################################################
# ── Comercio ───────────────────────────────────────────────
class Comercio(Base):
    __tablename__ = 'comercios'

    id_comercio = Column(String(36), primary_key=True)
    id_categoria = Column(Integer, ForeignKey('categorias_comercio.id_categoria'), nullable=False)
    nombre_comercio = Column(String(100), nullable=False)
    descripcion_comercio = Column(Text, nullable=False)
    telefono = Column(Numeric(10))
    email = Column(String(100))
    direccion = Column(String(255))
    imagen_url = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    id_usuario = Column(String(36), nullable=False)

    # Relaciones
    categoria = relationship("CategoriaComercio", back_populates="comercios")
    imagenes = relationship("ImagenComercio", back_populates="comercio", cascade="all, delete-orphan")
    servicios = relationship("ServicioComercio", back_populates="comercio", cascade="all, delete-orphan")

"""
class ImagenComercio(Base):
    __tablename__ = 'imagenes_comercio'

    id_imagen = Column(String(36), primary_key=True)
    id_comercio = Column(String(36), ForeignKey('comercios.id_comercio', ondelete='CASCADE'), nullable=False)
    imagen_url = Column(Text)
    descripcion = Column(String(255))
    estatus = Column(Enum('publica', 'privada'))

    # Relación inversa
    comercio = relationship("Comercio", back_populates="imagenes")"""