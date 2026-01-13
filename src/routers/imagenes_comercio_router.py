from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from src.core.db_credentials import get_db
from src.services.cloud.cloudinary_service import upload_images
from src.models.imagenes_comercio_model import ImagenComercio

router = APIRouter(
    prefix="/imagenes-comercios",
    tags=["Imagenes Comercios"]
)

@router.post("/{id_comercio}")
def upload_imagenes_comercio(
    id_comercio: str,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        results = upload_images(files, folder=f"comercios/{id_comercio}")

        imagenes = []
        for img in results:
            imagen = ImagenComercio(
                id_imagen=str(uuid.uuid4()),
                id_comercio=id_comercio,
                imagen_url=img["url"],      # ✅ CORREGIDO
                public_id=img["public_id"]
            )
            db.add(imagen)
            imagenes.append(imagen)

        db.commit()

        return {
            "status": "success",
            "message": "Imágenes del comercio subidas correctamente",
            "data": [
                {
                    "id_imagen": i.id_imagen,
                    "imagen_url": i.imagen_url
                } for i in imagenes
            ]
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
