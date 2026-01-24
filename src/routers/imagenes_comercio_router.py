from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from src.core.db_credentials import get_db
from src.services.cloud.cloudinary_service import upload_images
from src.models.imagenes_comercio_model import ImagenComercio
from src.models.comercios_model import Comercio as ComercioModel
from src.core.jwt_managger import get_current_user  # Importar seguridad

router = APIRouter(
    prefix="/imagenes-comercios",
    tags=["Imagenes Comercios"]
)


@router.post("/{id_comercio}")
def upload_imagenes_comercio(
        id_comercio: str,
        files: List[UploadFile] = File(...),
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)  # 🔒 Protegido
):
    """
    Sube imágenes para un comercio específico.
    Solo el dueño del comercio puede subir imágenes.
    """
    # Verificar que el comercio existe
    comercio = db.query(ComercioModel).filter(
        ComercioModel.id_comercio == id_comercio
    ).first()

    if not comercio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comercio no encontrado"
        )

    # Verificar que el usuario autenticado sea el dueño del comercio
    if comercio.id_usuario != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para subir imágenes a este comercio"
        )

    # Validar archivos
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

    for file in files:
        # Validar tipo
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de archivo no permitido: {file.content_type}. "
                       f"Usa: {', '.join(ALLOWED_TYPES)}"
            )

        # Validar tamaño (lectura parcial para no cargar todo en memoria)
        file.file.seek(0, 2)  # Ir al final del archivo
        file_size = file.file.tell()  # Obtener posición = tamaño
        file.file.seek(0)  # Volver al inicio

        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El archivo {file.filename} excede el tamaño máximo de 5MB"
            )

    try:
        # Subir imágenes a Cloudinary
        results = upload_images(files, folder=f"comercios/{id_comercio}")

        # Guardar referencias en la base de datos
        imagenes = []
        for img in results:
            imagen = ImagenComercio(
                id_imagen=str(uuid.uuid4()),
                id_comercio=id_comercio,
                imagen_url=img["url"],
                public_id=img["public_id"]
            )
            db.add(imagen)
            imagenes.append(imagen)

        db.commit()

        return {
            "status": "success",
            "message": f"{len(imagenes)} imagen(es) subida(s) correctamente",
            "data": [
                {
                    "id_imagen": i.id_imagen,
                    "imagen_url": i.imagen_url
                } for i in imagenes
            ]
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir imágenes: {str(e)}"
        )


@router.delete("/{id_imagen}")
def eliminar_imagen_comercio(
        id_imagen: str,
        db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)  # 🔒 Protegido
):
    """
    Elimina una imagen de comercio.
    Solo el dueño del comercio puede eliminar sus imágenes.
    """
    # Buscar la imagen
    imagen = db.query(ImagenComercio).filter(
        ImagenComercio.id_imagen == id_imagen
    ).first()

    if not imagen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagen no encontrada"
        )

    # Verificar que el comercio pertenezca al usuario
    comercio = db.query(ComercioModel).filter(
        ComercioModel.id_comercio == imagen.id_comercio
    ).first()

    if not comercio or comercio.id_usuario != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta imagen"
        )

    try:
        # Eliminar de Cloudinary (opcional, implementar si es necesario)
        # cloudinary.uploader.destroy(imagen.public_id)

        # Eliminar de la base de datos
        db.delete(imagen)
        db.commit()

        return {
            "status": "success",
            "message": "Imagen eliminada correctamente"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar imagen: {str(e)}"
        )