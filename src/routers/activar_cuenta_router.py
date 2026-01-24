from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from starlette.responses import RedirectResponse

from src.core.db_credentials import get_db
from src.models.email_token_model import EmailToken
from src.models.usuarios_model import Usuario as UsuarioModel

router_activar = APIRouter(
    prefix="/activar",
    tags=["activar"]
)


# -------------------------------------------------------------------------------------------------
# ACTIVAR CUENTA
# -------------------------------------------------------------------------------------------------
@router_activar.get("/activar")
def activar_cuenta(token: str, db: Session = Depends(get_db)):
    registro = db.query(EmailToken).filter(
        EmailToken.token == token
    ).first()

    if not registro:
        raise HTTPException(status_code=400, detail="Token inválido o ya usado")

    if registro.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expirado")

    print(registro.user_id)
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id_usuario == registro.user_id
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="algo")

    # Verificar si ya existe una cuenta activa con este email
    # (por si activó otra cuenta mientras tanto)
    cuenta_activa_existente = db.query(UsuarioModel).filter(
        UsuarioModel.email == usuario.email,
        UsuarioModel.estatus.is_(True),
        UsuarioModel.id_usuario != usuario.id_usuario
    ).first()

    if cuenta_activa_existente:
        # Eliminar este intento de registro y sus tokens
        db.query(EmailToken).filter(EmailToken.user_id == usuario.id_usuario).delete()
        db.delete(usuario)
        db.commit()
        raise HTTPException(
            status_code=400,
            detail="Ya existe una cuenta activa con este email"
        )

    # Activar la cuenta
    usuario.estatus = True
    usuario.ultimo_logeo = datetime.utcnow()
    registro.used = True

    # Eliminar otros intentos de registro inactivos con el mismo email
    db.query(UsuarioModel).filter(
        UsuarioModel.email == usuario.email,
        UsuarioModel.estatus.is_(False),  # ✅ Cambio aquí
        UsuarioModel.id_usuario != usuario.id_usuario
    ).delete()

    db.commit()

    return RedirectResponse(url="http://localhost:4200/")

