from fastapi import FastAPI, Depends, Request
from routes.routes_rol import rol
from routes.routes_usuario import usuario
from routes.routes_servicio import servicio
from routes.routes_vehiculo import vehiculo
from routes.routes_usuario_vehiculo_servicio import usuario_vehiculo_servicio
from routes.routes_producto import producto
from routes.routes_inventario import router as inventario_router    
from routes.routes_reporte import reporte
from config.security import get_current_user
from config.logger import api_logger, db_logger
from middleware.logging_middleware import LoggingMiddleware

app = FastAPI(
    title="Autolavado Proyecto Académico",
    description="API segura de almacenamiento de información para administrar autolavado",
    version="1.0.0"
)

# Añadir middleware de logging
app.add_middleware(LoggingMiddleware)

@app.on_event("startup")
async def startup_event():
    """Evento al iniciar la aplicación"""
    api_logger.info("=== API Autolavado iniciada ===")
    api_logger.info(f"Documentación disponible en /docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Evento al cerrar la aplicación"""
    api_logger.info("=== API Autolavado cerrada ===")

@app.get("/")
async def root(request: Request):
    api_logger.info("Endpoint root accedido", extra={"request_id": getattr(request.state, 'request_id', 'N/A')})
    return {
        "message": "Bienvenido a la API de Autolavado",
        "documentation": "/docs",
        "version": "1.0.0"
    }

# Tus routers existentes...
app.include_router(rol)
app.include_router(usuario)
app.include_router(vehiculo, dependencies=[Depends(get_current_user)])
app.include_router(servicio, dependencies=[Depends(get_current_user)])
app.include_router(usuario_vehiculo_servicio, dependencies=[Depends(get_current_user)])
app.include_router(producto, dependencies=[Depends(get_current_user)])
app.include_router(reporte, dependencies=[Depends(get_current_user)])
app.include_router(inventario_router, dependencies=[Depends(get_current_user)])