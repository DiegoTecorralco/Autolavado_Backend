from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import config.db
import crud.crud_reporte
import schemas.schema_reporte
import models.model_reporte
from typing import List
from config.security import get_current_user

reporte = APIRouter()

models.model_reporte.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@reporte.get("/reporte/", response_model=List[schemas.schema_reporte.Reporte], tags=["Reportes"])
async def read_reportes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    '''Obtiene todos los reportes'''
    db_reporte = crud.crud_reporte.get_reporte(db=db, skip=skip, limit=limit)
    return db_reporte

@reporte.get("/reporte/{id}", response_model=schemas.schema_reporte.Reporte, tags=["Reportes"])
async def read_reporte(
    id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    '''Obtiene un reporte por su ID'''
    db_reporte = crud.crud_reporte.get_reporte_by_id(db=db, id=id)
    if db_reporte is None:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return db_reporte

@reporte.get("/reporte/placas/{placas}", response_model=List[schemas.schema_reporte.Reporte], tags=["Reportes"])
async def read_reportes_by_placas(
    placas: str, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    '''Obtiene reportes por placas del vehículo'''
    db_reportes = crud.crud_reporte.get_reporte_by_placas(db=db, placas=placas)
    return db_reportes

@reporte.get("/reporte/servicio/{nombre_servicio}", response_model=List[schemas.schema_reporte.Reporte], tags=["Reportes"])
async def read_reportes_by_servicio(
    nombre_servicio: str, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    '''Obtiene reportes por nombre del servicio'''
    db_reportes = crud.crud_reporte.get_reporte_by_servicio(db=db, nombre_servicio=nombre_servicio)
    return db_reportes

@reporte.get("/reporte/cajero/{cajero_nombre}", response_model=List[schemas.schema_reporte.Reporte], tags=["Reportes"])
async def read_reportes_by_cajero(
    cajero_nombre: str, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    '''Obtiene reportes por nombre del cajero'''
    db_reportes = crud.crud_reporte.get_reporte_by_cajero(db=db, cajero_nombre=cajero_nombre)
    return db_reportes

@reporte.get("/reporte/operativo/{operativo_nombre}", response_model=List[schemas.schema_reporte.Reporte], tags=["Reportes"])
async def read_reportes_by_operativo(
    operativo_nombre: str, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    '''Obtiene reportes por nombre del operativo'''
    db_reportes = crud.crud_reporte.get_reporte_by_operativo(db=db, operativo_nombre=operativo_nombre)
    return db_reportes

@reporte.post("/reporte/", response_model=schemas.schema_reporte.Reporte, tags=["Reportes"])
def create_reporte(
    reporte: schemas.schema_reporte.ReporteCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    '''Crea un nuevo reporte'''
    return crud.crud_reporte.create_reporte(db=db, reporte=reporte)

@reporte.put("/reporte/{id}", response_model=schemas.schema_reporte.Reporte, tags=["Reportes"])
async def update_reporte(
    id: int, 
    reporte: schemas.schema_reporte.ReporteUpdate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    '''Actualiza un reporte existente'''
    db_reporte = crud.crud_reporte.update_reporte(db=db, id=id, reporte=reporte)
    if db_reporte is None:
        raise HTTPException(status_code=404, detail="Reporte no existe, no actualizado")
    return db_reporte

@reporte.delete("/reporte/{id}", response_model=schemas.schema_reporte.Reporte, tags=["Reportes"])
async def delete_reporte(
    id: int, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    '''Elimina un reporte'''
    db_reporte = crud.crud_reporte.delete_reporte(db=db, id=id)
    if db_reporte is None:
        raise HTTPException(status_code=404, detail="El Reporte no existe, no se pudo eliminar")
    return db_reporte