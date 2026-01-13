# src/routes/auth_router.py
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.db_credentials import get_db
from src.schema.login_schema import LoginRequest, TokenResponse
from src.models.usuarios_model import Usuario
from src.core.jwt_managger import create_access_token
from src.core.segurity import verify_password  # donde pusiste bcrypt

router_login = APIRouter(prefix="/auth", tags=["Auth"])

@router_login.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(
        Usuario.email == data.email
    ).first()

    # 1️⃣ Usuario no existe
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # 2️⃣ Cuenta NO verificada
    if usuario.estatus is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta no ha sido verificada"
        )

    # 3️⃣ Password incorrecto
    if not verify_password(data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # 4️⃣ Login OK → generar token
    token = create_access_token(
        id_usuario=str(usuario.id_usuario),
        nvl_usuario=str(usuario.id_nvl_usuario)
    )

    usuario.ultimo_logeo = datetime.utcnow()
    db.commit()

    return {
        "access_token": token,
        "token_type": "bearer"
    }