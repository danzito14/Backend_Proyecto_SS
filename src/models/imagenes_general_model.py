from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.sql import func

from src.core.db_credentials import Base


class ImagenGeneral(Base):
    __tablename__ = "imagenes_general"

    id_imagen = Column(String(36), primary_key=True, index=True)
    imagen_url = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )
    public_id = Column(Text)
