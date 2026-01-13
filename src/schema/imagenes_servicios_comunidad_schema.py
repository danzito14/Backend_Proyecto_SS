from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class ImagenServicioComunidadBase(BaseModel):
    imagen_url: Optional[str] = None
    descripcion: Optional[str] = None
    estatus: Optional[Literal["publica", "privada"]] = "publica"


class ImagenServicioComunidadCreate(ImagenServicioComunidadBase):
    id_servicio_comunidad: str


class ImagenServicioComunidadUpdate(BaseModel):
    imagen_url: Optional[str] = None
    descripcion: Optional[str] = None
    estatus: Optional[Literal["publica", "privada"]] = None


class ImagenServicioComunidadResponse(ImagenServicioComunidadBase):
    id_imagen: str
    id_servicio_comunidad: str
    created_at: datetime

    class Config:
        from_attributes = True
