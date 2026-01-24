from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import false
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import uuid

from src.core.db_credentials import get_db
from src.core.jwt_managger import get_current_user
from src.core.segurity import hash_password
from src.models.email_token_model import EmailToken
from src.models.usuarios_model import Usuario as UsuarioModel
from src.schema.usuarios_schema import (
    UsuarioOut,
    UsuarioCreate,
    UsuarioUpdate
)
from src.services.email.enviar_correo_activacion_cuenta import enviar_link_activacion

router_usuario = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


# -------------------------------------------------------------------------------------------------
# ✅ NUEVO: Obtener usuario actual (autenticado)
# -------------------------------------------------------------------------------------------------
@router_usuario.get("/me", response_model=UsuarioOut)
def obtener_usuario_actual(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene la información del usuario actualmente autenticado
    """
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id_usuario == current_user
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return usuario


# -------------------------------------------------------------------------------------------------
# Listar usuarios
# -------------------------------------------------------------------------------------------------
@router_usuario.get("/", response_model=List[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(UsuarioModel).all()


# -------------------------------------------------------------------------------------------------
# Obtener usuario por ID
# -------------------------------------------------------------------------------------------------
@router_usuario.get("/{id_usuario}", response_model=UsuarioOut)
def obtener_usuario(id_usuario: str, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id_usuario == id_usuario
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return usuario


# -------------------------------------------------------------------------------------------------
# Crear usuario (HASH 🔐)
# -------------------------------------------------------------------------------------------------
@router_usuario.post("/", status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):

    usuario_existente = db.query(UsuarioModel).filter(
        UsuarioModel.email == usuario.email
    ).first()

    # ─────────────────────────────
    # Caso 1: Usuario activo
    # ─────────────────────────────
    if usuario_existente and usuario_existente.estatus is True:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado y activado"
        )

    # ─────────────────────────────
    # Caso 2: Usuario inactivo reciente
    # ─────────────────────────────
    if usuario_existente and usuario_existente.estatus is False:
        if usuario_existente.fecha_creacion > datetime.utcnow() - timedelta(hours=24):
            raise HTTPException(
                status_code=400,
                detail="Ya existe un registro pendiente de activación. Revisa tu correo."
            )
        else:
            # Inactivo viejo → se elimina
            db.delete(usuario_existente)
            db.commit()

    # ─────────────────────────────
    # Crear nuevo usuario
    # ─────────────────────────────
    nuevo_usuario = UsuarioModel(
        id_usuario=str(uuid.uuid4()),
        id_nvl_usuario=usuario.id_nvl_usuario,
        email=usuario.email,
        nombre_completo=usuario.nombre_completo,
        foto_perfil_url=usuario.foto_perfil_url,
        password_hash=hash_password(usuario.password),
        provider="local",
        estatus=False,
        fecha_creacion=datetime.utcnow()
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    # ─────────────────────────────
    # Token de activación
    # ─────────────────────────────
    token = str(uuid.uuid4())

    email_token = EmailToken(
        id=str(uuid.uuid4()),
        user_id=nuevo_usuario.id_usuario,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=30),
        used=False
    )

    db.add(email_token)
    db.commit()

    enviar_link_activacion(
        nuevo_usuario.email,
        nuevo_usuario.nombre_completo,
        token
    )

    return {"message": "Usuario creado. Revisa tu correo para activar la cuenta."}


# -------------------------------------------------------------------------------------------------
# Reenviar correo de activación
# -------------------------------------------------------------------------------------------------
@router_usuario.post("/reenviar-activacion", status_code=status.HTTP_200_OK)
def reenviar_correo_activacion(email: str, db: Session = Depends(get_db)):
    # Buscar el usuario MÁS RECIENTE no activado con ese email
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.email == email,
        UsuarioModel.estatus.is_(False)
    ).order_by(UsuarioModel.fecha_creacion.desc()).first()

    if not usuario:
        # Verificar si existe uno activo
        usuario_activo = db.query(UsuarioModel).filter(
            UsuarioModel.email == email,
            UsuarioModel.estatus.is_(True)
        ).first()

        if usuario_activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cuenta ya está activada"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay solicitudes de registro pendientes para este email"
            )

    # Invalidar tokens anteriores del usuario
    db.query(EmailToken).filter(
        EmailToken.user_id == usuario.id_usuario,
        EmailToken.used.is_(False)
    ).update({"used": 1})

    # Crear nuevo token
    token = str(uuid.uuid4())

    email_token = EmailToken(
        id=str(uuid.uuid4()),
        user_id=usuario.id_usuario,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=30),
        used=0
    )

    db.add(email_token)
    db.commit()

    # Enviar correo
    enviar_link_activacion(
        usuario.email,
        usuario.nombre_completo,
        token
    )

    return {"message": "Correo de activación reenviado exitosamente"}


# -------------------------------------------------------------------------------------------------
# Actualizar usuario
# -------------------------------------------------------------------------------------------------
@router_usuario.put("/{id_usuario}", response_model=UsuarioOut)
def actualizar_usuario(
        usuario: UsuarioUpdate,
        db: Session = Depends(get_db), current_user: str = Depends(get_current_user)
):
    db_usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id_usuario == current_user
    ).first()

    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado aa"
        )

    datos = usuario.dict(exclude_unset=True)
    if "password" in datos:
        datos["password_hash"] = hash_password(datos.pop("password"))

    for key, value in datos.items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)

    return db_usuario


# -------------------------------------------------------------------------------------------------
# Eliminar usuario
# -------------------------------------------------------------------------------------------------
@router_usuario.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: str, db: Session = Depends(get_db)):
    db_usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id_usuario == id_usuario
    ).first()

    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    # Eliminar tokens asociados
    db.query(EmailToken).filter(EmailToken.user_id == id_usuario).delete()

    db.delete(db_usuario)
    db.commit()