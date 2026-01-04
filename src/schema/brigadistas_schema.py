from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# ─────────────────────────────────────────────
# Asesor
# ─────────────────────────────────────────────
class AsesorSSBase(BaseModel):
    nombre_asesor: str = Field(..., max_length=100)
    puesto: str = Field(..., max_length=100)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    estatus: bool = True


class AsesorSSCreate(AsesorSSBase):
    pass

class AsesorSSUpdate(BaseModel):
    nombre_asesor: Optional[str] = Field(None, max_length=100)
    puesto: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    estatus: Optional[bool] = None


class AsesorSSOut(AsesorSSBase):
    id_asesor: str

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────
# Carrera
# ─────────────────────────────────────────────
class CarreraBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    url_icon: Optional[str] = None
    color_hex: Optional[str] = Field(None, max_length=7)


class CarreraCreate(CarreraBase):
    pass


class CarreraUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    url_icon: Optional[str] = None
    color_hex: Optional[str] = Field(None, max_length=7)


class CarreraOut(CarreraBase):
    id_carrera: int

    class Config:
        from_attributes = True


# ─────────────────────────────────────────────
# Brigadista
# ─────────────────────────────────────────────
class BrigadistaBase(BaseModel):
    nombre_completo: str = Field(..., max_length=100)
    telefono: str = Field(..., max_length=15)
    fecha_nacimiento: date
    imagen_url: Optional[str] = None
    periodo: Optional[str] = Field(None, max_length=25)
    id_carrera: int


class BrigadistaCreate(BrigadistaBase):
    pass

class BrigadistaUpdate(BaseModel):
    nombre_completo: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=15)
    fecha_nacimiento: Optional[date] = None
    imagen_url: Optional[str] = None
    periodo: Optional[str] = Field(None, max_length=25)
    id_carrera: Optional[int] = None


class BrigadistaOut(BrigadistaBase):
    id_brigadista: str

    class Config:
        from_attributes = True
