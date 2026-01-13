from sqlalchemy import (
    Column,
    String,
    Text,
    Enum,
    ForeignKey,
    TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.db_credentials import Base


class ImagenServicioComunidad(Base):
    __tablename__ = "imagenes_servicios_comunidad"

    id_imagen = Column(String(36), primary_key=True, index=True)
    id_servicio_comunidad = Column(
        String(36),
        ForeignKey(
            "servicios_comunidad.id_servicio_comunidad",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    imagen_url = Column(Text)
    descripcion = Column(String(255))
    estatus = Column(
        Enum("publica", "privada"),
        default="publica"
    )
    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )
    public_id = Column(Text)

    servicio_comunidad = relationship(
        "ServicioComunidad",
        back_populates="imagenes"
    )
