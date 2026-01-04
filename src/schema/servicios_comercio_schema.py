from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

# ── Servicio ─────────────────────────────────────────────
class ServicioComercioBase(BaseModel):
    id_comercio: str = Field(..., max_length=36)
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = None

class ServicioComercioCreate(ServicioComercioBase):
    pass

class ServicioComercioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None

class ServicioComercioOut(ServicioComercioBase):
    id_servicio: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True

# ── Opción de Servicio ───────────────────────────────────
class OpcionServicioBase(BaseModel):
    id_servicio: str
    nombre_opcion: str
    descripcion: Optional[str] = None
    precio: Decimal

class OpcionServicioCreate(OpcionServicioBase):
    pass

class OpcionServicioUpdate(BaseModel):
    nombre_opcion: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = None

class OpcionServicioOut(OpcionServicioBase):
    id_opcion_servicio: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True

# ── Imagen de Opción ─────────────────────────────────────
class ImagenServicioBase(BaseModel):
    id_opcion_servicio: str
    imagen_url: str

class ImagenServicioCreate(ImagenServicioBase):
    pass

class ImagenServicioOut(ImagenServicioBase):
    id_imagen: str
    created_at: datetime

    class Config:
        from_attributes = True
