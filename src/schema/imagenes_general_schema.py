from pydantic import BaseModel
from datetime import datetime


class ImagenGeneralBase(BaseModel):
    imagen_url: str


class ImagenGeneralCreate(ImagenGeneralBase):
    pass


class ImagenGeneralResponse(ImagenGeneralBase):
    id_imagen: str
    created_at: datetime

    class Config:
        from_attributes = True
