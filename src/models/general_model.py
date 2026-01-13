from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from src.core.db_credentials import Base
# ##############################################################################################################
# Modelos Generales
# ##############################################################################################################
"""
class ImagenGeneral(Base):
    __tablename__ = 'imagenes_general'

    id_imagen = Column(String(36), primary_key=True)
    imagen_url = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
"""