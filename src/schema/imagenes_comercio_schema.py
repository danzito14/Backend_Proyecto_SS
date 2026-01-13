from pydantic import BaseModel
from typing import Optional, Literal


class ImagenComercioBase(BaseModel):
    imagen_url: Optional[str] = None
    descripcion: Optional[str] = None
    estatus: Optional[Literal["publica", "privada"]] = "publica"


class ImagenComercioCreate(ImagenComercioBase):
    id_comercio: str


class ImagenComercioUpdate(BaseModel):
    imagen_url: Optional[str] = None
    descripcion: Optional[str] = None
    estatus: Optional[Literal["publica", "privada"]] = None


class ImagenComercioResponse(ImagenComercioBase):
    id_imagen: str
    id_comercio: str

    class Config:
        from_attributes = True
