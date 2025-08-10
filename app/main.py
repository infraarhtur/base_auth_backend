"""
Punto de entrada principal de FastAPI
"""

from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn

from app.core.config import get_settings
from app.db.session import engine
# from app.db.init_db import init_db_first_time  # Comentado temporalmente
from app.api import register_routes
from app.schemas.response import ErrorResponse, SuccessResponse, HealthCheckResponse

# Obtener configuración
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Eventos de inicio y cierre de la aplicación
    """
    # Evento de inicio
    print("🚀 Iniciando aplicación base_auth_backend...")
    
    # Inicializar base de datos si es necesario
    # try:
    #     init_db_first_time()
    #     print("✅ Base de datos inicializada correctamente")
    # except Exception as e:
    #     print(f"⚠️ Error al inicializar base de datos: {e}")
    print("✅ Aplicación iniciada correctamente")
    
    yield
    
    # Evento de cierre
    print("🛑 Cerrando aplicación base_auth_backend...")


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.title,
    version=settings.version,
    description="Backend de autenticación multitenant con FastAPI y SQLAlchemy",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manejo de excepciones globales
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Manejar excepciones HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail,
            error_code=f"HTTP_{exc.status_code}",
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejar errores de validación"""
    # Obtener detalles de los errores de validación
    error_details = []
    for error in exc.errors():
        field = error.get("loc", [])[-1] if error.get("loc") else "unknown"
        message = error.get("msg", "Error de validación")
        error_details.append(f"{field}: {message}")
    
    error_message = "Error de validación en los datos de entrada"
    if error_details:
        error_message += f" - {'; '.join(error_details)}"
    
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            detail=error_message,
            error_code="VALIDATION_ERROR",
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Manejar excepciones generales"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail="Error interno del servidor",
            error_code="INTERNAL_ERROR",
            timestamp=datetime.utcnow().isoformat()
        ).dict()
    )


# Registrar rutas de la API
register_routes(app)


# Rutas básicas de la aplicación
@app.get("/", response_model=SuccessResponse)
async def root():
    """Ruta raíz de la aplicación"""
    return SuccessResponse(
        message="Bienvenido a base_auth_backend",
        data={
            "title": settings.title,
            "version": settings.version,
            "docs": "/docs"
        }
    )


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Verificar el estado de salud de la aplicación"""
    # Verificar conexión a base de datos
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()
        db_status = "OK"
    except Exception as e:
        print(f"Database health check error: {e}")
        db_status = "ERROR"
    
    return HealthCheckResponse(
        status="OK" if db_status == "OK" else "ERROR",
        version=settings.version,
        timestamp=datetime.utcnow().isoformat(),
        database=db_status
    )


@app.get("/info")
async def info():
    """Información de la aplicación"""
    return {
        "title": settings.title,
        "version": settings.version,
        "description": "Backend de autenticación multitenant",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json"
    }


# Función para ejecutar la aplicación
def run_app():
    """Ejecutar la aplicación con uvicorn"""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8002,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    run_app()
