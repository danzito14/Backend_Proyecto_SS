from fastapi import (
    APIRouter, UploadFile, File,
    Depends, HTTPException, status
)
from sqlalchemy.orm import Session
import uuid

from src.core.db_credentials import get_db
from src.models.imagenes_servicios_comunidad_model import ImagenServicioComunidad
from src.services.cloud.cloudinary_service import upload_images, delete_image
from src.schema.imagenes_servicios_comunidad_schema import ImagenServicioComunidadResponse

router = APIRouter(
    prefix="/imagenes-servicios-comunidad",
    tags=["Imagenes Servicios Comunidad"]
)


@router.post(
    "/{id_servicio_comunidad}",
    response_model=ImagenServicioComunidadResponse,
    status_code=status.HTTP_201_CREATED
)
def upload_imagen_servicio_comunidad(
    id_servicio_comunidad: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    result = upload_images(
        file,
        folder=f"servicios_comunidad/{id_servicio_comunidad}"
    )

    imagen = ImagenServicioComunidad(
        id_imagen=str(uuid.uuid4()),
        id_servicio_comunidad=id_servicio_comunidad,
        imagen_url=result["url"],
        public_id=result["public_id"]
    )

    db.add(imagen)
    db.commit()
    db.refresh(imagen)

    return imagen


@router.delete("/{id_imagen}", status_code=204)
def delete_imagen_servicio_comunidad(
    id_imagen: str,
    db: Session = Depends(get_db)
):
    imagen = db.query(ImagenServicioComunidad).get(id_imagen)
    if not imagen:
        raise HTTPException(404)

    delete_image(imagen.public_id)
    db.delete(imagen)
    db.commit()
