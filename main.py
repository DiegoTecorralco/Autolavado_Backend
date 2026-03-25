from fastapi import FastAPI, Depends
from routes.routes_rol import rol
from routes.routes_usuario import usuario
from routes.routes_servicio import servicio
from routes.routes_vehiculo import vehiculo
from routes.routes_usuario_vehiculo_servicio import usuario_vehiculo_servicio
from routes.routes_producto import producto  # <-- NUEVA IMPORTACIÓN
from routes.routes_inventario import router as inventario_router    
from routes.routes_reporte import reporte

from config.security import get_current_user

app = FastAPI(
    title="Autolavado Proyecto Académico",
    description="API segura de almacenamiento de información para administrar autolavado",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de Autolavado",
        "documentation": "/docs",
        "version": "1.0.0"
    }

app.include_router(rol)
app.include_router(usuario)
app.include_router(vehiculo, dependencies=[Depends(get_current_user)])
app.include_router(servicio, dependencies=[Depends(get_current_user)])
app.include_router(usuario_vehiculo_servicio, dependencies=[Depends(get_current_user)])
app.include_router(producto, dependencies=[Depends(get_current_user)])  # <-- NUEVA RUTA
app.include_router(reporte, dependencies=[Depends(get_current_user)])
app.include_router(inventario_router, dependencies=[Depends(get_current_user)])