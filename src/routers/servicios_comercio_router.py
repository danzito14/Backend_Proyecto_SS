from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from src.core.db_credentials import get_db
from src.models.servicios_comercios_model import ServicioComercio as ServicioComercioModel, OpcionServicio as OpcionServicioModel
from src.models.comercios_model import Comercio as ComercioModel
from src.schema.servicios_comercio_schema import (
    ServicioComercioCreate,
    ServicioComercioUpdate,
    ServicioComercioOut
)
from src.services.cloud.cloudinary_service import eliminar_imagenes_cloudinary
from src.models.imagenes_servicios_model import ImagenServicio

router_servicio = APIRouter(prefix="/servicios-comercio", tags=["Servicios Comercio"])

# ── Obtener todos los servicios de un comercio ───────────
@router_servicio.get("/comercio/{id_comercio}", response_model=List[ServicioComercioOut])
def obtener_servicios_por_comercio(id_comercio: str, db: Session = Depends(get_db)):
    return db.query(ServicioComercioModel).filter(ServicioComercioModel.id_comercio == id_comercio).all()

# ── Obtener un servicio por ID ───────────────────────────
@router_servicio.get("/{id_servicio}", response_model=ServicioComercioOut)
def obtener_servicio(id_servicio: str, db: Session = Depends(get_db)):
    servicio = db.query(ServicioComercioModel).filter(ServicioComercioModel.id_servicio == id_servicio).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio

# ── Crear servicio ───────────────────────────────────────
@router_servicio.post("/nuevo_servicio", response_model=ServicioComercioOut, status_code=status.HTTP_201_CREATED)
def crear_servicio(servicio: ServicioComercioCreate, db: Session = Depends(get_db)):
    # Validar que el comercio exista
    comercio = db.query(ComercioModel).filter(ComercioModel.id_comercio == servicio.id_comercio).first()
    if not comercio:
        raise HTTPException(status_code=404, detail="Comercio no encontrado")

    db_servicio = ServicioComercioModel(
        id_servicio=str(uuid.uuid4()),
        fecha_creacion=datetime.utcnow(),
        **servicio.dict()
    )
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio

# ── Actualizar servicio ──────────────────────────────────
@router_servicio.put("/{id_servicio}", response_model=ServicioComercioOut)
def actualizar_servicio(id_servicio: str, servicio: ServicioComercioUpdate, db: Session = Depends(get_db)):
    db_servicio = db.query(ServicioComercioModel).filter(ServicioComercioModel.id_servicio == id_servicio).first()
    if not db_servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    for key, value in servicio.dict(exclude_unset=True).items():
        setattr(db_servicio, key, value)

    db.commit()
    db.refresh(db_servicio)
    return db_servicio


# ── Eliminar servicio ────────────────────────────────────
@router_servicio.delete("/{id_servicio}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_servicio(id_servicio: str, db: Session = Depends(get_db)):
    # 1. Verificar que existe
    db_servicio = db.query(ServicioComercioModel).filter(
        ServicioComercioModel.id_servicio == id_servicio
    ).first()

    if not db_servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    # 2. RECOLECTAR todas las URLs de imágenes ANTES de eliminar
    imagenes_a_eliminar = []

    # Obtener todas las opciones del servicio
    opciones = db.query(OpcionServicioModel).filter(
        OpcionServicioModel.id_servicio == id_servicio
    ).all()

    # Por cada opción, obtener sus imágenes
    for opcion in opciones:
        imagenes_opcion = db.query(ImagenServicio).filter(
            ImagenServicio.id_opcion_servicio == opcion.id_opcion_servicio
        ).all()

        for imagen in imagenes_opcion:
            if imagen.imagen_url:
                imagenes_a_eliminar.append(imagen.imagen_url)

    # 3. ELIMINAR de Cloudinary
    if imagenes_a_eliminar:
        resultado = eliminar_imagenes_cloudinary(imagenes_a_eliminar)
        print(f"""
        ═══════════════════════════════════════
        SERVICIO ELIMINADO: {db_servicio.nombre}
        ID: {id_servicio}
        Opciones eliminadas: {len(opciones)}
        Imágenes eliminadas: {resultado['exitosas']}/{resultado['total']}
        ═══════════════════════════════════════
        """)

    # 4. ELIMINAR de la base de datos (cascade elimina opciones e imágenes)
    db.delete(db_servicio)
    db.commit()

    return None
