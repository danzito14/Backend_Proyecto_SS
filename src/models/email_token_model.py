from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from datetime import datetime

from sqlalchemy.orm import relationship

from src.core.db_credentials import Base

class EmailToken(Base):
    __tablename__ = "email_token"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("usuario.id_usuario"), nullable=False)
    token = Column(String(100), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)

    usuario = relationship("Usuario", back_populates="tokens")