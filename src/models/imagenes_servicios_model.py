from sqlalchemy import (
    Column,
    String,
    Text,
    ForeignKey,
    TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.db_credentials import Base


class ImagenServicio(Base):
    __tablename__ = "imagenes_servicios"

    id_imagen = Column(String(36), primary_key=True, index=True)
    id_opcion_servicio = Column(
        String(36),
        ForeignKey(
            "opciones_servicio.id_opcion_servicio",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    imagen_url = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )
    public_id = Column(Text)

    opcion_servicio = relationship(
        "OpcionServicio",
        back_populates="imagenes"
    )
