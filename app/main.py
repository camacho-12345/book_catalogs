from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routers.libros import router as libros_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento de inicio: Conectar a MongoDB
    await connect_to_mongo()
    yield
    # Evento de apagado: Cerrar conexion
    await close_mongo_connection()


app = FastAPI(
    title=settings.APP_NAME,
    description="API REST desarrollada con FastAPI y MongoDB para la administracion y consulta de un catalogo de libros.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS para permitir integracion con frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(libros_router, prefix="/api/v1")


@app.get("/", tags=["Health Check"])
async def root():
    """Ruta raiz para verificar el estado de la API."""
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "docs": "/docs",
        "version": "1.0.0"
    }
