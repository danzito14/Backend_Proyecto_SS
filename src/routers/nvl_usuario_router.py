from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import traceback

from src.core.db_credentials import get_db
from src.schema.usuarios_schema import NivelUsuario
from src.models.usuarios_model import NivelUsuario as NivelUsuarioModel

# ##############################################################################################################
# Router de Niveles de Usuario
# ##############################################################################################################

router_nivel_usuario = APIRouter(
    prefix="/niveles-usuario",
    tags=["Niveles Usuario"]
)


# ===========================
# GET ALL
# ===========================
@router_nivel_usuario.get("/", response_model=List[NivelUsuario])
def obtener_niveles_usuario(db: Session = Depends(get_db)):
    try:
        return db.query(NivelUsuarioModel).all()

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ===========================
# GET BY ID
# ===========================
@router_nivel_usuario.get("/{id_nvl_usuario}", response_model=NivelUsuario)
def obtener_nivel_usuario(id_nvl_usuario: int, db: Session = Depends(get_db)):
    try:
        nivel = (
            db.query(NivelUsuarioModel)
            .filter(NivelUsuarioModel.id_nvl_usuario == id_nvl_usuario)
            .first()
        )

        if not nivel:
            raise HTTPException(
                status_code=404,
                detail="Nivel de usuario no encontrado"
            )

        return nivel

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ===========================
# POST
# ===========================
@router_nivel_usuario.post(
    "/",
    response_model=NivelUsuario,
    status_code=status.HTTP_201_CREATED
)
def crear_nivel_usuario(nivel: NivelUsuario, db: Session = Depends(get_db)):
    try:
        existe = (
            db.query(NivelUsuarioModel)
            .filter(NivelUsuarioModel.rol_usuario == nivel.rol_usuario)
            .first()
        )

        if existe:
            raise HTTPException(
                status_code=400,
                detail="El rol de usuario ya existe"
            )

        db_nivel = NivelUsuarioModel(**nivel.dict())
        db.add(db_nivel)
        db.commit()
        db.refresh(db_nivel)
        return db_nivel

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))




# ===========================
# PUT
# ===========================
@router_nivel_usuario.put("/{id_nvl_usuario}", response_model=NivelUsuario)
def actualizar_nivel_usuario(
    id_nvl_usuario: int,
    nivel: NivelUsuario,
    db: Session = Depends(get_db)
):
    try:
        db_nivel = (
            db.query(NivelUsuarioModel)
            .filter(NivelUsuarioModel.id_nvl_usuario == id_nvl_usuario)
            .first()
        )

        if not db_nivel:
            raise HTTPException(
                status_code=404,
                detail="Nivel de usuario no encontrado"
            )

        # Validar duplicado SOLO si se quiere cambiar el rol
        if nivel.rol_usuario:
            existe = (
                db.query(NivelUsuarioModel)
                .filter(
                    NivelUsuarioModel.rol_usuario == nivel.rol_usuario,
                    NivelUsuarioModel.id_nvl_usuario != id_nvl_usuario
                )
                .first()
            )
            if existe:
                raise HTTPException(
                    status_code=400,
                    detail="El rol de usuario ya existe"
                )

        for key, value in nivel.dict(exclude_unset=True).items():
            setattr(db_nivel, key, value)

        db.commit()
        db.refresh(db_nivel)
        return db_nivel

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ===========================
# DELETE
# ===========================
@router_nivel_usuario.delete(
    "/{id_nvl_usuario}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_nivel_usuario(id_nvl_usuario: int, db: Session = Depends(get_db)):
    try:
        db_nivel = (
            db.query(NivelUsuarioModel)
            .filter(NivelUsuarioModel.id_nvl_usuario == id_nvl_usuario)
            .first()
        )

        if not db_nivel:
            raise HTTPException(
                status_code=404,
                detail="Nivel de usuario no encontrado"
            )

        db.delete(db_nivel)
        db.commit()
        return None

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
