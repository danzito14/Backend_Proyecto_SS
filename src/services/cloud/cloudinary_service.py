import cloudinary
import cloudinary.uploader
import uuid
import re
from typing import List


def upload_images(files, folder: str):
    uploaded_images = []

    for file in files:
        public_id = f"{folder}/{uuid.uuid4()}"

        result = cloudinary.uploader.upload(
            file.file,
            public_id=public_id,
            overwrite=True,
            resource_type="image"
        )

        uploaded_images.append({
            "public_id": result["public_id"],
            "url": result["secure_url"]
        })

    return uploaded_images


def delete_image(public_id: str):
    cloudinary.uploader.destroy(
        public_id,
        resource_type="image"
    )



def extraer_public_id(url: str) -> str:
    """
    Extrae el public_id de una URL de Cloudinary

    Ejemplo:
    https://res.cloudinary.com/cloud/image/upload/v1234/folder/imagen.jpg
    -> folder/imagen
    """
    try:
        # Patrón: captura todo después de /upload/ hasta la extensión
        match = re.search(r'/upload/(?:v\d+/)?(.+)\.\w+$', url)

        if match:
            return match.group(1)

        return ""
    except Exception as e:
        print(f"❌ Error extrayendo public_id de {url}: {e}")
        return ""


def eliminar_imagen_cloudinary(imagen_url: str) -> bool:
    """
    Elimina una imagen de Cloudinary dado su URL

    Returns:
        True si se eliminó exitosamente, False si hubo error
    """
    if not imagen_url or "cloudinary.com" not in imagen_url:
        return False

    try:
        public_id = extraer_public_id(imagen_url)
        if public_id:
            resultado = cloudinary.uploader.destroy(public_id)
            print(f"✅ Imagen eliminada de Cloudinary: {public_id} - {resultado}")
            return resultado.get('result') == 'ok'
        return False
    except Exception as e:
        print(f"❌ Error eliminando imagen de Cloudinary {imagen_url}: {e}")
        return False


def eliminar_imagenes_cloudinary(imagenes_urls: List[str]) -> dict:
    """
    Elimina múltiples imágenes de Cloudinary

    Returns:
        {'exitosas': int, 'fallidas': int, 'total': int}
    """
    exitosas = 0
    fallidas = 0

    for url in imagenes_urls:
        if eliminar_imagen_cloudinary(url):
            exitosas += 1
        else:
            fallidas += 1

    resultado = {
        'exitosas': exitosas,
        'fallidas': fallidas,
        'total': len(imagenes_urls)
    }

    print(f"📊 Resumen eliminación Cloudinary: {exitosas}/{len(imagenes_urls)} exitosas")

    return resultado
