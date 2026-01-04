from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.db_credentials import get_db
from src.models.comercios_model import CategoriaComercio as CategoriaComercioModel
from src.schema.comercios_schema import (
    CategoriaComercioOut,
    CategoriaComercioCreate,
    CategoriaComercioUpdate
)

router_categoria = APIRouter(
    prefix="/categorias-comercio",
    tags=["Categorías Comercio"]
)


# 🔹 Obtener todas
@router_categoria.get("/", response_model=List[CategoriaComercioOut])
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(CategoriaComercioModel).all()


# 🔹 Obtener una por ID
@router_categoria.get("/{id_categoria}", response_model=CategoriaComercioOut)
def obtener_categoria(id_categoria: int, db: Session = Depends(get_db)):
    categoria = db.query(CategoriaComercioModel).filter(
        CategoriaComercioModel.id_categoria == id_categoria
    ).first()

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    return categoria


# 🔹 Crear
@router_categoria.post(
    "/",
    response_model=CategoriaComercioOut,
    status_code=status.HTTP_201_CREATED
)
def crear_categoria(
    categoria: CategoriaComercioCreate,
    db: Session = Depends(get_db)
):
    db_categoria = CategoriaComercioModel(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


# 🔹 Actualizar
@router_categoria.put("/{id_categoria}", response_model=CategoriaComercioOut)
def actualizar_categoria(
    id_categoria: int,
    categoria: CategoriaComercioUpdate,
    db: Session = Depends(get_db)
):
    db_categoria = db.query(CategoriaComercioModel).filter(
        CategoriaComercioModel.id_categoria == id_categoria
    ).first()

    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    for key, value in categoria.dict(exclude_unset=True).items():
        setattr(db_categoria, key, value)

    db.commit()
    db.refresh(db_categoria)
    return db_categoria


# 🔹 Eliminar
@router_categoria.delete("/{id_categoria}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(id_categoria: int, db: Session = Depends(get_db)):
    db_categoria = db.query(CategoriaComercioModel).filter(
        CategoriaComercioModel.id_categoria == id_categoria
    ).first()

    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db.delete(db_categoria)
    db.commit()
