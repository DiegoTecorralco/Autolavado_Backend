from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import config.db, crud.crud_usuario_vehiculo_servicio,  schemas.schema_usuario_vehiculo_servicio, models.model_usuario_vehiculo_servicio
from typing import List


usuario_vehiculo_servicio = APIRouter()

models.model_usuario_vehiculo_servicio.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@usuario_vehiculo_servicio.get("/usuario_vehiculo_servicio/", response_model=List[schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio], tags=["Usuario Vehiculo Servicios"])
async def read_usuario_vehiculo_servicios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_usuario_vehiculo_servicio= crud.crud_usuario_vehiculo_servicio.get_usuario_vehiculo_servicio(db=db, skip=skip, limit=limit)
    return db_usuario_vehiculo_servicio

@usuario_vehiculo_servicio.post("/usuario_vehiculo_servicio/", response_model=schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio, tags=["Usuario Vehiculo Servicios"])
def create_rol(usuario_vehiculo_servicio: schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicioCreate, db: Session = Depends(get_db)):
    db_usuario_vehiculo_servicio = crud.crud_usuario_vehiculo_servicio.get_usuario_vehiculo_servicio_by_nombre(db, fecha=usuario_vehiculo_servicio.fecha, hora = usuario_vehiculo_servicio.hora)
    if db_usuario_vehiculo_servicio:
        raise HTTPException(status_code=400, detail="Usuario Vehiculo Servicio existente intenta nuevamente")
    return crud.crud_usuario_vehiculo_servicio.create_usuario_vehiculo_servicio(db=db, usuario_vehiculo_servicio=usuario_vehiculo_servicio)

@usuario_vehiculo_servicio.put("/usuario_vehiculo_servicio/{id}", response_model=schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio, tags=["Usuario Vehiculo Servicios"])
async def update_usuario_vehiculo_servicio(id: int, usuario_vehiculo_servicio: schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio, db: Session = Depends(get_db)):
    db_usuario_vehiculo_servicio = crud.crud_usuario_vehiculo_servicio.update_usuario_vehiculo_servicio(db=db, id=id, usuario_vehiculo_servicio=usuario_vehiculo_servicio)
    if db_usuario_vehiculo_servicio is None:
        raise HTTPException(status_code=404, detail="Usuario Vehiculo Servicio no existe, no actualizado")
    return db_usuario_vehiculo_servicio

@usuario_vehiculo_servicio.delete("/usuario_vehiculo_servicio/{id}", response_model=schemas.schema_usuario_vehiculo_servicio.UsuarioVehiculoServicio, tags=["Usuario Vehiculo Servicios"])
async def delete_usuario_vehiculo_servicio(id: int, db: Session = Depends(get_db)):
    db_usuario_vehiculo_servicio = crud.crud_usuario_vehiculo_servicio.delete_usuario_vehiculo_servicio(db=db, id=id)
    if db_usuario_vehiculo_servicio is None:
        raise HTTPException(status_code=404, detail="El Usuario Vehiculo Servicio no existe, no se pudo eliminar")
    return db_usuario_vehiculo_servicio