from pydantic import BaseModel, Field
from datetime import datetime
# ##############################################################################################################
# Modelos Generales
# ##############################################################################################################

class ImagenGeneral(BaseModel):
    id_imagen: str = Field(..., max_length=36)
    imagen_url: str
    created_at: datetime

    class Config:
        from_attributes = True