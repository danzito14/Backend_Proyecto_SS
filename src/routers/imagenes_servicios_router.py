from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from src.core.db_credentials import get_db
from src.services.cloud.cloudinary_service import upload_images
from src.models.imagenes_servicios_model import ImagenServicio

router = APIRouter(
    prefix="/imagenes-servicios",
    tags=["Imagenes Servicios"]
)

@router.post("/{id_servicio}")
def upload_imagenes_servicio(
    id_servicio: str,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        results = upload_images(files, folder=f"servicios/{id_servicio}")

        imagenes = []
        for img in results:
            imagen = ImagenServicio(
                id_imagen=str(uuid.uuid4()),
                id_opcion_servicio=id_servicio,
                public_id=img["public_id"],
                imagen_url=img["url"]
            )
            db.add(imagen)
            imagenes.append(imagen)

        db.commit()

        return {
            "status": "success",
            "message": "Imágenes del servicio subidas correctamente",
            "data": [
                {
                    "id_imagen": i.id_imagen,
                    "url": i.imagen_url
                } for i in imagenes
            ]
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
