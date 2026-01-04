from sqlalchemy import text

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os


# ✅ Cargar el archivo .env
load_dotenv()


####################################################################################################
# AQUI VAN LAS IMPORTACIONES DE LOS ENDPOINTS

# ES IMPORTANTE PRIMERO LEER EL .ENV
####################################################################################################
from src.routers.usuarios_router import router_usuario
from src.routers.nvl_usuario_router import router_nivel_usuario
from src.routers.comercios_router import router_comercio
from src.routers.servicios_comercio_router import router_servicio
from src.routers.opciones_servicio_router import router_opcion
from src.routers.brigadistas_asesor_router import router_brigadista, router_asesor, router_carrera
from src.routers.categorias_comercio_router import router_categoria
from src.routers.servicios_comunidad_model import router_servicio_comunidad
from src.core.db_credentials import SessionLocal

app = FastAPI(title="Proyecto del Servicio Social",
              description="Proyecto Comunitarios para el apoyo de la publicidad de los comercios de Ruiz Cortinez",
              version="0.0.1")
# Primero CORS
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:4200", "http://127.0.0.1:4200", '*'],  # ambos por seguridad
    allow_origins=['*'],  # ambos por seguridad
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_check():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ Conexión a la base de datos exitosa")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("❌ Error de conexión a la BD")
    finally:
        db.close()

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