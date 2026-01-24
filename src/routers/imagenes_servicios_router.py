from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from src.core.db_credentials import get_db
from src.services.cloud.cloudinary_service import upload_images
from src.models.imagenes_servicios_model import ImagenServicio
from src.models.servicios_comercios_model import OpcionServicio

router = APIRouter(
    prefix="/imagenes-servicios",
    tags=["Imagenes Servicios"]
)


# ── Subir imágenes para una opción de servicio ──────────────────
@router.post("/{id_opcion_servicio}")
def upload_imagenes_opcion(
        id_opcion_servicio: str,
        files: List[UploadFile] = File(...),
        db: Session = Depends(get_db)
):
    """Sube imágenes asociadas a una opción de servicio específica"""

    # Verificar que la opción exista
    opcion = db.query(OpcionServicio).filter(
        OpcionServicio.id_opcion_servicio == id_opcion_servicio
    ).first()

    if not opcion:
        raise HTTPException(
            status_code=404,
            detail=f"Opción de servicio con ID {id_opcion_servicio} no encontrada"
        )

    try:
        # Subir a Cloudinary
        results = upload_images(files, folder=f"servicios/opciones/{id_opcion_servicio}")

        imagenes = []
        for img in results:
            imagen = ImagenServicio(
                id_imagen=str(uuid.uuid4()),
                id_opcion_servicio=id_opcion_servicio,
                public_id=img["public_id"],
                imagen_url=img["url"]
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
        print(f"❌ Error al subir imágenes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al subir imágenes: {str(e)}")


# ── Obtener imágenes de una opción ──────────────────────────────
@router.get("/opcion/{id_opcion_servicio}")
def obtener_imagenes_opcion(
        id_opcion_servicio: str,
        db: Session = Depends(get_db)
):
    """Obtiene todas las imágenes asociadas a una opción de servicio"""

    # Verificar que la opción exista
    opcion = db.query(OpcionServicio).filter(
        OpcionServicio.id_opcion_servicio == id_opcion_servicio
    ).first()

    if not opcion:
        raise HTTPException(
            status_code=404,
            detail=f"Opción de servicio con ID {id_opcion_servicio} no encontrada"
        )

    # Obtener imágenes
    imagenes = db.query(ImagenServicio).filter(
        ImagenServicio.id_opcion_servicio == id_opcion_servicio
    ).all()

    print(f"📸 Imágenes encontradas para opción {id_opcion_servicio}: {len(imagenes)}")

    return [
        {
            "id_imagen": img.id_imagen,
            "imagen_url": img.imagen_url
        } for img in imagenes
    ]


# ── Obtener una imagen específica ──────────────────────────────
@router.get("/imagen/{id_imagen}")
def obtener_imagen(
        id_imagen: str,
        db: Session = Depends(get_db)
):
    """Obtiene información de una imagen específica"""

    imagen = db.query(ImagenServicio).filter(
        ImagenServicio.id_imagen == id_imagen
    ).first()

    if not imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    return {
        "id_imagen": imagen.id_imagen,
        "id_opcion_servicio": imagen.id_opcion_servicio,
        "imagen_url": imagen.imagen_url,
        "public_id": imagen.public_id,
        "created_at": imagen.created_at
    }


# ── Eliminar una imagen específica ──────────────────────────────
@router.delete("/{id_imagen}")
def eliminar_imagen(
        id_imagen: str,
        db: Session = Depends(get_db)
):
    """Elimina una imagen específica de una opción de servicio"""

    imagen = db.query(ImagenServicio).filter(
        ImagenServicio.id_imagen == id_imagen
    ).first()

    if not imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    try:
        # Opcional: Eliminar de Cloudinary
        # from src.services.cloud.cloudinary_service import delete_image
        # delete_image(imagen.public_id)

        db.delete(imagen)
        db.commit()

        return {
            "status": "success",
            "message": "Imagen eliminada correctamente"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar imagen: {str(e)}")


# ── Obtener todas las imágenes de un servicio ───────────────────
@router.get("/servicio/{id_servicio}")
def obtener_imagenes_servicio(
        id_servicio: str,
        db: Session = Depends(get_db)
):
    """Obtiene todas las imágenes de todas las opciones de un servicio"""

    # Obtener todas las opciones del servicio
    opciones = db.query(OpcionServicio).filter(
        OpcionServicio.id_servicio == id_servicio
    ).all()

    if not opciones:
        return []

    # Obtener imágenes de todas las opciones
    ids_opciones = [opcion.id_opcion_servicio for opcion in opciones]
    imagenes = db.query(ImagenServicio).filter(
        ImagenServicio.id_opcion_servicio.in_(ids_opciones)
    ).all()

    print(f"📸 Total de imágenes para servicio {id_servicio}: {len(imagenes)}")

    return [
        {
            "id_imagen": img.id_imagen,
            "id_opcion_servicio": img.id_opcion_servicio,
            "imagen_url": img.imagen_url
        } for img in imagenes
    ]


# ── Eliminar todas las imágenes de una opción ──────────────────
@router.delete("/opcion/{id_opcion_servicio}/all")
def eliminar_todas_imagenes_opcion(
        id_opcion_servicio: str,
        db: Session = Depends(get_db)
):
    """Elimina todas las imágenes de una opción de servicio"""

    imagenes = db.query(ImagenServicio).filter(
        ImagenServicio.id_opcion_servicio == id_opcion_servicio
    ).all()

    if not imagenes:
        return {
            "status": "success",
            "message": "No hay imágenes para eliminar"
        }

    try:
        cantidad = len(imagenes)

        for imagen in imagenes:
            db.delete(imagen)

        db.commit()

        return {
            "status": "success",
            "message": f"{cantidad} imagen(es) eliminada(s) correctamente"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar imágenes: {str(e)}")