from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import uuid

from src.core.db_credentials import get_db
from src.core.segurity import hash_password
from src.models.email_token_model import EmailToken
from src.models.usuarios_model import Usuario as UsuarioModel
from src.schema.usuarios_schema import (
    UsuarioOut,
    UsuarioCreate,
    UsuarioUpdate
)
from src.services.email.enviar_correo_activacion_cuenta import enviar_link_activacion

# -------------------------------------------------------------------------------------------------
# Router Usuarios
# -------------------------------------------------------------------------------------------------

router_usuario = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

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

    if db.query(UsuarioModel).filter(
        UsuarioModel.email == usuario.email
    ).first():
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )

    nuevo_usuario = UsuarioModel(
        id_usuario=str(uuid.uuid4()),
        id_nvl_usuario=usuario.id_nvl_usuario,
        email=usuario.email,
        nombre_completo=usuario.nombre_completo,
        foto_perfil_url=usuario.foto_perfil_url,
        password_hash=hash_password(usuario.password),
        provider="local",
        estatus=0,
        fecha_creacion=datetime.utcnow()
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    token = str(uuid.uuid4())

    email_token = EmailToken(
        id=str(uuid.uuid4()),
        user_id=nuevo_usuario.id_usuario,
        token=token,
        expires_at=datetime.utcnow() + timedelta(minutes=30),
        used=0
    )

    db.add(email_token)
    db.commit()

    enviar_link_activacion(
        nuevo_usuario.email,
        nuevo_usuario.nombre_completo,
        token
    )

    return {"message": "Usuario creado. Revisa tu correo para activar la cuenta."}

# -----------------------------
# ACTIVAR CUENTA
# -----------------------------
@router_usuario.get("/activar")
def activar_cuenta(token: str, db: Session = Depends(get_db)):

    registro = db.query(EmailToken).filter(
        EmailToken.token == token,
        EmailToken.used == 0
    ).first()

    if not registro:
        raise HTTPException(status_code=400, detail="Token inválido")

    if registro.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expirado")

    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id_usuario == registro.user_id
    ).first()

    usuario.estatus = 1
    registro.used = 1

    db.commit()

    return {"message": "Cuenta activada correctamente"}



# -------------------------------------------------------------------------------------------------
# Actualizar usuario
# -------------------------------------------------------------------------------------------------
@router_usuario.put("/{id_usuario}", response_model=UsuarioOut)
def actualizar_usuario(
    id_usuario: str,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db)
):

    db_usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id_usuario == id_usuario
    ).first()

    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
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

    db.delete(db_usuario)
    db.commit()
