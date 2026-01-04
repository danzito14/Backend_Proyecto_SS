from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

# ##############################################################################################################
# Schema: Nivel de Usuario
# ##############################################################################################################

class NivelUsuario(BaseModel):
    id_nvl_usuario: Optional[int] = None
    rol_usuario: str = Field(..., max_length=50)

    class Config:
        from_attributes = True


# ##############################################################################################################
# Schema: Usuario
# ##############################################################################################################
# usuarios_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    email: EmailStr
    nombre_completo: Optional[str] = None
    foto_perfil_url: Optional[str] = None
    id_nvl_usuario: int

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    foto_perfil_url: Optional[str] = None
    id_nvl_usuario: Optional[int] = None
    password: Optional[str] = None

class UsuarioOut(UsuarioBase):
    id_usuario: str
    fecha_creacion: datetime
    ultimo_logeo: datetime

    class Config:
        from_attributes = True
