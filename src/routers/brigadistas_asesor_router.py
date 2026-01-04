from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from src.core.db_credentials import get_db
from src.models.brigadistas_model import (
    AsesorSS as AsesorSSModel,
    Brigadista as BrigadistaModel,
    Carrera as CarreraModel
)
from src.schema.brigadistas_schema import (
    AsesorSSCreate, AsesorSSOut, AsesorSSUpdate,
    CarreraCreate, CarreraOut, CarreraUpdate,
    BrigadistaCreate, BrigadistaOut, BrigadistaUpdate
)

# ═════════════════════════════════════════════
# ASESOR
# ═════════════════════════════════════════════
router_asesor = APIRouter(prefix="/asesores", tags=["Asesores SS"])

@router_asesor.get("/", response_model=List[AsesorSSOut])
def obtener_asesores(db: Session = Depends(get_db)):
    return db.query(AsesorSSModel).all()

@router_asesor.post("/", response_model=AsesorSSOut, status_code=201)
def crear_asesor(asesor: AsesorSSCreate, db: Session = Depends(get_db)):
    if db.query(AsesorSSModel).filter(
        AsesorSSModel.nombre_asesor == asesor.nombre_asesor
    ).first():
        raise HTTPException(400, "El asesor ya existe")

    db_asesor = AsesorSSModel(
        id_asesor=str(uuid.uuid4()),
        **asesor.dict()
    )
    db.add(db_asesor)
    db.commit()
    db.refresh(db_asesor)
    return db_asesor

@router_asesor.put("/{id_asesor}", response_model=AsesorSSOut)
def actualizar_asesor(
    id_asesor: str,
    asesor: AsesorSSUpdate,
    db: Session = Depends(get_db)
):
    db_asesor = db.query(AsesorSSModel).get(id_asesor)
    if not db_asesor:
        raise HTTPException(404, "Asesor no encontrado")

    data = asesor.dict(exclude_unset=True)

    if "nombre_asesor" in data:
        if db.query(AsesorSSModel).filter(
            AsesorSSModel.nombre_asesor == data["nombre_asesor"],
            AsesorSSModel.id_asesor != id_asesor
        ).first():
            raise HTTPException(400, "Ya existe otro asesor con ese nombre")

    for key, value in data.items():
        setattr(db_asesor, key, value)

    db.commit()
    db.refresh(db_asesor)
    return db_asesor

@router_asesor.delete("/{id_asesor}", status_code=204)
def eliminar_asesor(id_asesor: str, db: Session = Depends(get_db)):
    asesor = db.query(AsesorSSModel).get(id_asesor)
    if not asesor:
        raise HTTPException(404, "Asesor no encontrado")

    db.delete(asesor)
    db.commit()


# ═════════════════════════════════════════════
# CARRERAS
# ═════════════════════════════════════════════
router_carrera = APIRouter(prefix="/carreras", tags=["Carreras"])

@router_carrera.get("/", response_model=List[CarreraOut])
def obtener_carreras(db: Session = Depends(get_db)):
    return db.query(CarreraModel).all()

@router_carrera.post("/", response_model=CarreraOut, status_code=201)
def crear_carrera(carrera: CarreraCreate, db: Session = Depends(get_db)):
    if db.query(CarreraModel).filter(
        CarreraModel.nombre == carrera.nombre
    ).first():
        raise HTTPException(400, "La carrera ya existe")

    db_carrera = CarreraModel(**carrera.dict())
    db.add(db_carrera)
    db.commit()
    db.refresh(db_carrera)
    return db_carrera

@router_carrera.put("/{id_carrera}", response_model=CarreraOut)
def actualizar_carrera(
    id_carrera: int,
    carrera: CarreraUpdate,
    db: Session = Depends(get_db)
):
    db_carrera = db.query(CarreraModel).get(id_carrera)
    if not db_carrera:
        raise HTTPException(404, "Carrera no encontrada")

    data = carrera.dict(exclude_unset=True)

    if "nombre" in data:
        if db.query(CarreraModel).filter(
            CarreraModel.nombre == data["nombre"],
            CarreraModel.id_carrera != id_carrera
        ).first():
            raise HTTPException(400, "Ya existe otra carrera con ese nombre")

    for key, value in data.items():
        setattr(db_carrera, key, value)

    db.commit()
    db.refresh(db_carrera)
    return db_carrera

@router_carrera.delete("/{id_carrera}", status_code=204)
def eliminar_carrera(id_carrera: int, db: Session = Depends(get_db)):
    carrera = db.query(CarreraModel).get(id_carrera)
    if not carrera:
        raise HTTPException(404, "Carrera no encontrada")

    db.delete(carrera)
    db.commit()


# ═════════════════════════════════════════════
# BRIGADISTAS
# ═════════════════════════════════════════════
router_brigadista = APIRouter(prefix="/brigadistas", tags=["Brigadistas"])

@router_brigadista.get("/", response_model=List[BrigadistaOut])
def obtener_brigadistas(db: Session = Depends(get_db)):
    return db.query(BrigadistaModel).all()

@router_brigadista.post("/", response_model=BrigadistaOut, status_code=201)
def crear_brigadista(brigadista: BrigadistaCreate, db: Session = Depends(get_db)):
    if not db.query(CarreraModel).get(brigadista.id_carrera):
        raise HTTPException(404, "Carrera no encontrada")

    if db.query(BrigadistaModel).filter(
        BrigadistaModel.telefono == brigadista.telefono
    ).first():
        raise HTTPException(400, "El teléfono ya está registrado")

    if db.query(BrigadistaModel).filter(
        BrigadistaModel.nombre_completo == brigadista.nombre_completo
    ).first():
        raise HTTPException(400, "El brigadista ya está registrado")

    db_brigadista = BrigadistaModel(
        id_brigadista=str(uuid.uuid4()),
        **brigadista.dict()
    )
    db.add(db_brigadista)
    db.commit()
    db.refresh(db_brigadista)
    return db_brigadista

@router_brigadista.put("/{id_brigadista}", response_model=BrigadistaOut)
def actualizar_brigadista(
    id_brigadista: str,
    brigadista: BrigadistaUpdate,
    db: Session = Depends(get_db)
):
    db_brigadista = db.query(BrigadistaModel).get(id_brigadista)
    if not db_brigadista:
        raise HTTPException(404, "Brigadista no encontrado")

    data = brigadista.dict(exclude_unset=True)

    if "id_carrera" in data:
        if not db.query(CarreraModel).get(data["id_carrera"]):
            raise HTTPException(404, "Carrera no encontrada")

    if "telefono" in data:
        if db.query(BrigadistaModel).filter(
            BrigadistaModel.telefono == data["telefono"],
            BrigadistaModel.id_brigadista != id_brigadista
        ).first():
            raise HTTPException(400, "El teléfono ya está registrado")

    if "nombre_completo" in data:
        if db.query(BrigadistaModel).filter(
                BrigadistaModel.nombre_completo == data["nombre_completo"],
                BrigadistaModel.id_brigadista != id_brigadista
        ).first():
            raise HTTPException(400, "El brigadista ya está registrado")

    for key, value in data.items():
        setattr(db_brigadista, key, value)

    db.commit()
    db.refresh(db_brigadista)
    return db_brigadista

@router_brigadista.delete("/{id_brigadista}", status_code=204)
def eliminar_brigadista(id_brigadista: str, db: Session = Depends(get_db)):
    brigadista = db.query(BrigadistaModel).get(id_brigadista)
    if not brigadista:
        raise HTTPException(404, "Brigadista no encontrado")

    db.delete(brigadista)
    db.commit()
