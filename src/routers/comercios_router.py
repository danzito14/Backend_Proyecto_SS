from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from typing import List

from src.core.db_credentials import get_db
from src.models.comercios_model import Comercio as ComercioModel
from src.models.comercios_model import CategoriaComercio as CategoriaComercioModel
from src.schema.comercios_schema import ComercioCreate, ComercioUpdate, ComercioOut

router_comercio = APIRouter(prefix="/comercios", tags=["Comercios"])

# ── Obtener todos ─────────────────────────────────────────
@router_comercio.get("/", response_model=List[ComercioOut])
def obtener_comercios(db: Session = Depends(get_db)):
    return db.query(ComercioModel).all()

# ── Obtener uno por ID ────────────────────────────────────
@router_comercio.get("/{id_comercio}", response_model=ComercioOut)
def obtener_comercio(id_comercio: str, db: Session = Depends(get_db)):
    comercio = db.query(ComercioModel).filter(ComercioModel.id_comercio == id_comercio).first()
    if not comercio:
        raise HTTPException(status_code=404, detail="Comercio no encontrado")
    return comercio

# ── Crear ─────────────────────────────────────────────────
@router_comercio.post("/", response_model=ComercioOut, status_code=status.HTTP_201_CREATED)
def crear_comercio(comercio: ComercioCreate, db: Session = Depends(get_db)):
    # Validar categoría
    categoria = db.query(CategoriaComercioModel).filter(
        CategoriaComercioModel.id_categoria == comercio.id_categoria
    ).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Validar nombre único por usuario
    existente = db.query(ComercioModel).filter(
        ComercioModel.id_usuario == comercio.id_usuario,
        ComercioModel.nombre_comercio == comercio.nombre_comercio
    ).first()
    if existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un comercio con este nombre para el usuario"
        )

    # Crear comercio
    db_comercio = ComercioModel(
        id_comercio=str(uuid.uuid4()),
        created_at=datetime.utcnow(),
        **comercio.dict()
    )
    db.add(db_comercio)
    db.commit()
    db.refresh(db_comercio)
    return db_comercio

# ── Actualizar ───────────────────────────────────────────
@router_comercio.put("/{id_comercio}", response_model=ComercioOut)
def actualizar_comercio(id_comercio: str, comercio: ComercioUpdate, db: Session = Depends(get_db)):
    db_comercio = db.query(ComercioModel).filter(ComercioModel.id_comercio == id_comercio).first()
    if not db_comercio:
        raise HTTPException(status_code=404, detail="Comercio no encontrado")

    # Validar que no repita nombre con otro comercio del mismo usuario
    if comercio.nombre_comercio:
        existente = db.query(ComercioModel).filter(
            ComercioModel.id_usuario == db_comercio.id_usuario,
            ComercioModel.nombre_comercio == comercio.nombre_comercio,
            ComercioModel.id_comercio != id_comercio
        ).first()
        if existente:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un comercio con este nombre para el usuario"
            )

    for key, value in comercio.dict(exclude_unset=True).items():
        setattr(db_comercio, key, value)

    db.commit()
    db.refresh(db_comercio)
    return db_comercio

# ── Eliminar ─────────────────────────────────────────────
@router_comercio.delete("/{id_comercio}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_comercio(id_comercio: str, db: Session = Depends(get_db)):
    db_comercio = db.query(ComercioModel).filter(ComercioModel.id_comercio == id_comercio).first()
    if not db_comercio:
        raise HTTPException(status_code=404, detail="Comercio no encontrado")

    db.delete(db_comercio)
    db.commit()
