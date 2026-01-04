from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime
# ##############################################################################################################
# Modelos de Servicios de Comunidad
# ##############################################################################################################

class ServicioComunidad(BaseModel):
    id_servicio_comunidad: str = Field(..., max_length=36)
    titulo_servicio: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    direccion: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=15)
    imagen_url: Optional[str] = None
    created_at: datetime
    estatus: bool = True

    class Config:
        from_attributes = True


class ImagenServicioComunidad(BaseModel):
    id_imagen: str = Field(..., max_length=36)
    id_servicio_comunidad: str = Field(..., max_length=36)
    imagen_url: Optional[str] = None
    descripcion: Optional[str] = Field(None, max_length=255)
    estatus: Literal['publica', 'privada'] = 'publica'
    created_at: datetime

    class Config:
        from_attributes = True


