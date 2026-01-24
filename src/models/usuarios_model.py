from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Enum, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from src.core.db_credentials import Base


class NivelUsuario(Base):
    __tablename__ = 'nvl_usuario'

    id_nvl_usuario = Column(Integer, primary_key=True, autoincrement=True)
    rol_usuario = Column(String(50), nullable=False)

    usuarios = relationship("Usuario", back_populates="nivel")


class Usuario(Base):
    __tablename__ = 'usuario'

    id_usuario = Column(String(36), primary_key=True)
    id_nvl_usuario = Column(Integer, ForeignKey('nvl_usuario.id_nvl_usuario'), nullable=False)

    google_id = Column(String(200), unique=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text)
    nombre_completo = Column(String(100))
    foto_perfil_url = Column(Text)

    provider = Column(Enum('local', 'google'), nullable=False, default='local')
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    ultimo_logeo = Column(TIMESTAMP, default=datetime.utcnow)
    estatus = Column(Boolean, default=0)

    nivel = relationship("NivelUsuario", back_populates="usuarios")
    # ✅ Agregar este relationship
    tokens = relationship("EmailToken", back_populates="usuario", cascade="all, delete-orphan")

    # Constraint única compuesta
    __table_args__ = (
        UniqueConstraint('email', 'estatus', name='uq_email_activo'),
    )