from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from typing import List

from src.core.db_credentials import get_db
from src.models.comercios_model import Comercio as ComercioModel
from src.models.comercios_model import CategoriaComercio as CategoriaComercioModel
from src.schema.comercios_schema import ComercioCreate, ComercioUpdate, ComercioOut
from src.core.jwt_managger import  get_current_user  # Importar dependencia de seguridad

router_mcomercio = APIRouter(prefix="/miscomercios", tags=["MisComercios"])
# ── Obtener uno por usuario (privado) ──────────────────────────
@router_mcomercio.get("/miscomercios", response_model=List[ComercioOut])
def obtener_comercio(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """Endpoint privado - requiere autenticación"""
    comercio = db.query(ComercioModel).filter(
        ComercioModel.id_usuario == current_user
    ).all()
    if not comercio:
        raise HTTPException(status_code=404, detail="Comercio no encontrado")
    return comercio
