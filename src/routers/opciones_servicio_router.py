from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from src.core.db_credentials import get_db
from src.models.imagenes_servicios_model import ImagenServicio
from src.models.servicios_comercios_model import OpcionServicio as OpcionServicioModel
from src.models.servicios_comercios_model import ServicioComercio as ServicioComercioModel
from src.schema.servicios_comercio_schema import (
    OpcionServicioCreate,
    OpcionServicioUpdate,
    OpcionServicioOut
)
from src.services.cloud.cloudinary_service import eliminar_imagenes_cloudinary

router_opcion = APIRouter(prefix="/opciones-servicio", tags=["Opciones Servicio"])

# ── Obtener todas las opciones de un servicio ───────────
@router_opcion.get("/servicio/{id_servicio}", response_model=List[OpcionServicioOut])
def obtener_opciones_por_servicio(id_servicio: str, db: Session = Depends(get_db)):
    return db.query(OpcionServicioModel).filter(OpcionServicioModel.id_servicio == id_servicio).all()

# ── Obtener opción por ID ───────────────────────────────
@router_opcion.get("/{id_opcion_servicio}", response_model=OpcionServicioOut)
def obtener_opcion(id_opcion_servicio: str, db: Session = Depends(get_db)):
    opcion = db.query(OpcionServicioModel).filter(
        OpcionServicioModel.id_opcion_servicio == id_opcion_servicio
    ).first()
    if not opcion:
        raise HTTPException(status_code=404, detail="Opción de servicio no encontrada")
    return opcion

# ── Crear opción ───────────────────────────────────────
@router_opcion.post("/", response_model=OpcionServicioOut, status_code=status.HTTP_201_CREATED)
def crear_opcion(opcion: OpcionServicioCreate, db: Session = Depends(get_db)):
    # Verificar que el servicio exista
    servicio = db.query(ServicioComercioModel).filter(
        ServicioComercioModel.id_servicio == opcion.id_servicio
    ).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    # Verificar que no exista una opción con el mismo nombre en ese servicio
    opcion_existente = db.query(OpcionServicioModel).filter(
        OpcionServicioModel.id_servicio == opcion.id_servicio,
        OpcionServicioModel.nombre_opcion == opcion.nombre_opcion
    ).first()
    if opcion_existente:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe una opción con el nombre '{opcion.nombre_opcion}' para este servicio"
        )

    db_opcion = OpcionServicioModel(
        id_opcion_servicio=str(uuid.uuid4()),
        fecha_creacion=datetime.utcnow(),
        **opcion.dict()
    )
    db.add(db_opcion)
    db.commit()
    db.refresh(db_opcion)
    return db_opcion

# ── Actualizar opción ──────────────────────────────────
@router_opcion.put("/{id_opcion_servicio}", response_model=OpcionServicioOut)
def actualizar_opcion(id_opcion_servicio: str, opcion: OpcionServicioUpdate, db: Session = Depends(get_db)):
    db_opcion = db.query(OpcionServicioModel).filter(
        OpcionServicioModel.id_opcion_servicio == id_opcion_servicio
    ).first()
    if not db_opcion:
        raise HTTPException(status_code=404, detail="Opción de servicio no encontrada")

    # Validar duplicado si se está cambiando el nombre
    if opcion.nombre_opcion:
        opcion_duplicada = db.query(OpcionServicioModel).filter(
            OpcionServicioModel.id_servicio == db_opcion.id_servicio,
            OpcionServicioModel.nombre_opcion == opcion.nombre_opcion,
            OpcionServicioModel.id_opcion_servicio != id_opcion_servicio
        ).first()
        if opcion_duplicada:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe una opción con el nombre '{opcion.nombre_opcion}' para este servicio"
            )

    for key, value in opcion.dict(exclude_unset=True).items():
        setattr(db_opcion, key, value)

    db.commit()
    db.refresh(db_opcion)
    return db_opcion


# ── Eliminar opción ────────────────────────────────────
@router_opcion.delete("/{id_opcion_servicio}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_opcion(id_opcion_servicio: str, db: Session = Depends(get_db)):
    # 1. Verificar que existe
    db_opcion = db.query(OpcionServicioModel).filter(
        OpcionServicioModel.id_opcion_servicio == id_opcion_servicio
    ).first()

    if not db_opcion:
        raise HTTPException(status_code=404, detail="Opción de servicio no encontrada")

    # 2. RECOLECTAR URLs de imágenes ANTES de eliminar
    imagenes_a_eliminar = []

    imagenes = db.query(ImagenServicio).filter(
        ImagenServicio.id_opcion_servicio == id_opcion_servicio
    ).all()

    for imagen in imagenes:
        if imagen.imagen_url:
            imagenes_a_eliminar.append(imagen.imagen_url)

    # 3. ELIMINAR de Cloudinary
    if imagenes_a_eliminar:
        resultado = eliminar_imagenes_cloudinary(imagenes_a_eliminar)
        print(f"""
        ═══════════════════════════════════════
        OPCIÓN ELIMINADA: {db_opcion.nombre_opcion}
        ID: {id_opcion_servicio}
        Imágenes eliminadas: {resultado['exitosas']}/{resultado['total']}
        ═══════════════════════════════════════
        """)

    # 4. ELIMINAR de la base de datos (cascade elimina las imágenes)
    db.delete(db_opcion)
    db.commit()

    return None