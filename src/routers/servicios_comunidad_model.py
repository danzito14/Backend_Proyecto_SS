from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime
from src.core.db_credentials import get_db

from src.models.servicios_comunidad_model import ServicioComunidad as ServicioComunidadModel
from src.schema.servicios_comunidad_schema import ServicioComunidad
# ##############################################################################################################
# Router de Servicios de Comunidad
# ##############################################################################################################

router_servicio_comunidad = APIRouter(prefix="/servicios-comunidad", tags=["Servicios Comunidad"])


@router_servicio_comunidad.get("/", response_model=List[ServicioComunidad])
def obtener_servicios_comunidad(activos: bool = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(ServicioComunidadModel)
    if activos is not None:
        query = query.filter(ServicioComunidadModel.estatus == activos)
    return query.offset(skip).limit(limit).all()


@router_servicio_comunidad.get("/{id_servicio_comunidad}", response_model=ServicioComunidad)
def obtener_servicio_comunidad(id_servicio_comunidad: str, db: Session = Depends(get_db)):
    servicio = db.query(ServicioComunidadModel).filter(
        ServicioComunidadModel.id_servicio_comunidad == id_servicio_comunidad).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio de comunidad no encontrado")
    return servicio


@router_servicio_comunidad.post("/", response_model=ServicioComunidad, status_code=status.HTTP_201_CREATED)
def crear_servicio_comunidad(servicio: ServicioComunidad, db: Session = Depends(get_db)):
    servicio_dict = servicio.dict()
    servicio_dict['id_servicio_comunidad'] = str(uuid.uuid4())
    servicio_dict['created_at'] = datetime.utcnow()

    db_servicio = ServicioComunidadModel(**servicio_dict)
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio


@router_servicio_comunidad.put("/{id_servicio_comunidad}", response_model=ServicioComunidad)
def actualizar_servicio_comunidad(id_servicio_comunidad: str, servicio: ServicioComunidad,
                                  db: Session = Depends(get_db)):
    db_servicio = db.query(ServicioComunidadModel).filter(
        ServicioComunidadModel.id_servicio_comunidad == id_servicio_comunidad).first()
    if not db_servicio:
        raise HTTPException(status_code=404, detail="Servicio de comunidad no encontrado")

    for key, value in servicio.dict(exclude_unset=True).items():
        if key not in ['id_servicio_comunidad', 'created_at']:
            setattr(db_servicio, key, value)

    db.commit()
    db.refresh(db_servicio)
    return db_servicio


@router_servicio_comunidad.delete("/{id_servicio_comunidad}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_servicio_comunidad(id_servicio_comunidad: str, db: Session = Depends(get_db)):
    db_servicio = db.query(ServicioComunidadModel).filter(
        ServicioComunidadModel.id_servicio_comunidad == id_servicio_comunidad).first()
    if not db_servicio:
        raise HTTPException(status_code=404, detail="Servicio de comunidad no encontrado")

    db.delete(db_servicio)
    db.commit()
    return None


