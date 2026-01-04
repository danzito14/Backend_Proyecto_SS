from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

# ##############################################################################################################
# Modelos de Comercios
# ##############################################################################################################


# ##############################################################################################################
# Schemas de Categorías de Comercio
# ##############################################################################################################

class CategoriaComercioBase(BaseModel):
    nombre_categoria: str = Field(..., max_length=50)
    color_hex: Optional[str] = Field(None, max_length=7)


class CategoriaComercioCreate(CategoriaComercioBase):
    pass


class CategoriaComercioUpdate(BaseModel):
    nombre_categoria: Optional[str] = Field(None, max_length=50)
    color_hex: Optional[str] = Field(None, max_length=7)


class CategoriaComercioOut(CategoriaComercioBase):
    id_categoria: int

    class Config:
        from_attributes = True

# ##############################################################################################################
# -------- Base --------

class ComercioBase(BaseModel):
    id_categoria: int
    nombre_comercio: str = Field(..., max_length=100)
    descripcion_comercio: str
    telefono: Optional[int] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    imagen_url: str
    id_usuario: str  # ID del usuario dueño del comercio

class ComercioCreate(ComercioBase):
    pass

class ComercioUpdate(BaseModel):
    id_categoria: Optional[int] = None
    nombre_comercio: Optional[str] = None
    descripcion_comercio: Optional[str] = None
    telefono: Optional[int] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    imagen_url: Optional[str] = None

class ComercioOut(ComercioBase):
    id_comercio: str
    created_at: datetime

    class Config:
        from_attributes = True