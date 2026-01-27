from sqlalchemy import text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# ✅ Cargar el archivo .env
load_dotenv()

####################################################################################################
# IMPORTACIONES DE LOS ENDPOINTS
####################################################################################################
from src.routers.usuarios_router import router_usuario
from src.routers.nvl_usuario_router import router_nivel_usuario
from src.routers.comercios_router import router_comercio
from src.routers.servicios_comercio_router import router_servicio
from src.routers.opciones_servicio_router import router_opcion
from src.routers.brigadistas_asesor_router import router_brigadista, router_asesor, router_carrera
from src.routers.categorias_comercio_router import router_categoria
from src.routers.servicios_comunidad_model import router_servicio_comunidad
from src.routers.imagenes_general_router import router as router_imagen_general
from src.routers.imagenes_servicios_router import router as router_imagen_servicio
from src.routers.imagenes_comercio_router import router as router_imagen_comercio
from src.routers.imagenes_servicios_comunidad_router import router as router_imagen_servicio_comunidad
from src.core.db_credentials import SessionLocal
from src.routers.login_router import router_login
from src.routers.mis_comercios import router_mcomercio
from src.routers.activar_cuenta_router import router_activar

app = FastAPI(
    title="Proyecto del Servicio Social",
    description="Proyecto Comunitarios para el apoyo de la publicidad de los comercios de Ruiz Cortinez",
    version="0.0.1"
)

# ✅ CONFIGURACIÓN CORS CORREGIDA
# Obtén los orígenes permitidos desde variables de entorno
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "https://proyectoss-production.up.railway.app,http://localhost:4200,http://localhost:4000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # ✅ Lista específica de orígenes
    allow_credentials=True,  # ✅ Permite cookies/auth headers
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],  # Métodos específicos
    allow_headers=["*"],  # Permite todos los headers
    expose_headers=["*"],  # Expone headers en respuesta
    max_age=3600,  # Caché de preflight requests
)


# ✅ Middleware para logging (opcional pero útil)
@app.middleware("http")
async def log_requests(request, call_next):
    import logging
    logger = logging.getLogger("uvicorn")

    origin = request.headers.get("origin", "No origin")
    logger.info(f"📥 {request.method} {request.url.path} - Origin: {origin}")

    response = await call_next(request)

    logger.info(f"📤 Status: {response.status_code}")
    return response


@app.on_event("startup")
def startup_db_check():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ Conexión a la base de datos exitosa")
        print(f"🌍 Orígenes permitidos: {ALLOWED_ORIGINS}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("❌ Error de conexión a la BD")
    finally:
        db.close()


# ✅ Endpoint de health check
@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "API funcionando correctamente",
        "version": "0.0.1"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Incluir routers
app.include_router(router_usuario)
app.include_router(router_nivel_usuario)
app.include_router(router_comercio)
app.include_router(router_servicio)
app.include_router(router_opcion)
app.include_router(router_brigadista)
app.include_router(router_asesor)
app.include_router(router_carrera)
app.include_router(router_categoria)
app.include_router(router_servicio_comunidad)
app.include_router(router_imagen_servicio_comunidad)
app.include_router(router_imagen_servicio)
app.include_router(router_imagen_general)
app.include_router(router_imagen_comercio)
app.include_router(router_login)
app.include_router(router_activar)
app.include_router(router_mcomercio)