from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.core.db_credentials import get_db
from src.services.cloud.cloudinary_service import upload_images

router = APIRouter(
    prefix="/imagenes-general",
    tags=["Imagenes General"]
)

@router.post("/")
def upload_imagen_general(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        result = upload_images(files, folder="general")
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
