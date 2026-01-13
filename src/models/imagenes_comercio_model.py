from sqlalchemy import (
    Column,
    String,
    Text,
    Enum,
    ForeignKey
)
from sqlalchemy.orm import relationship

from src.core.db_credentials import Base


class ImagenComercio(Base):
    __tablename__ = "imagenes_comercio"

    id_imagen = Column(String(36), primary_key=True, index=True)
    id_comercio = Column(
        String(36),
        ForeignKey("comercios.id_comercio", ondelete="CASCADE"),
        nullable=False
    )
    imagen_url = Column(Text)
    descripcion = Column(String(255))
    estatus = Column(
        Enum("publica", "privada"),
        default="publica"
    )
    public_id = Column(Text)

    comercio = relationship(
        "Comercio",
        back_populates="imagenes"
    )
