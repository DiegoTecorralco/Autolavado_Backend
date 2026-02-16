from fastapi import FastAPI
from routes.routes_rol import rol
from routes.routes_usuario import usuario
from routes.routes_servicio import servicio
from routes.routes_vehiculo import vehiculo
from routes.routes_usuario_vehiculo_servicio import usuario_vehiculo_servicio
app = FastAPI(
    title="Autolavado Proyecto Académico",
    description="API segura de almacenamiento de informacion ara administrar autolavado"
)

app.include_router(rol)
app.include_router(usuario)
app.include_router(vehiculo)
app.include_router(servicio)
app.include_router(usuario_vehiculo_servicio)

