from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from src.core.db_credentials import Base

# ─────────────────────────────────────────────
# Asesores de Servicio Social
# ─────────────────────────────────────────────
class AsesorSS(Base):
    __tablename__ = 'asesor_ss'
    __table_args__ = (
        UniqueConstraint('nombre_asesor', name='uq_asesor_nombre'),
    )

    id_asesor = Column(String(36), primary_key=True)
    nombre_asesor = Column(String(100), nullable=False)
    puesto = Column(String(100), nullable=False)
    descripcion = Column(Text)
    imagen_url = Column(Text)
    estatus = Column(Boolean, default=True)


# ─────────────────────────────────────────────
# Carreras
# ─────────────────────────────────────────────
class Carrera(Base):
    __tablename__ = 'carrera'
    __table_args__ = (
        UniqueConstraint('nombre', name='uq_carrera_nombre'),
    )

    id_carrera = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    url_icon = Column(Text)
    color_hex = Column(String(7))

    brigadistas = relationship(
        "Brigadista",
        back_populates="carrera",
        cascade="all, delete"
    )


# ─────────────────────────────────────────────
# Brigadistas
# ─────────────────────────────────────────────
class Brigadista(Base):
    __tablename__ = 'brigadista'
    __table_args__ = (
        UniqueConstraint('telefono', name='uq_brigadista_telefono'),
    )

    id_brigadista = Column(String(36), primary_key=True)
    nombre_completo = Column(String(100), nullable=False)
    telefono = Column(String(15), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    imagen_url = Column(Text)
    periodo = Column(String(25))
    id_carrera = Column(Integer, ForeignKey('carrera.id_carrera'), nullable=False)

    carrera = relationship("Carrera", back_populates="brigadistas")
