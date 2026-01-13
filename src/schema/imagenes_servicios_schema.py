from pydantic import BaseModel
from datetime import datetime


class ImagenServicioBase(BaseModel):
    imagen_url: str


class ImagenServicioCreate(ImagenServicioBase):
    id_opcion_servicio: str


class ImagenServicioResponse(ImagenServicioBase):
    id_imagen: str
    id_opcion_servicio: str
    created_at: datetime

    class Config:
        from_attributes = True
