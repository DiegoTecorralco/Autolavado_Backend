from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
import config.db, crud.crud_vehiculo,  schemas.schema_vehiculo, models.model_vehiculo
from typing import List
from config.logger import api_logger

vehiculo = APIRouter()

models.model_vehiculo.Base.metadata.create_all(bind=config.db.engine)

def get_db():
    db = config.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@vehiculo.get("/vehiculo/", response_model=List[schemas.schema_vehiculo.Vehiculo], tags=["Vehiculos"])
async def read_vehiculo(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    request_id = getattr(request.state, 'request_id', 'N/A')
    api_logger.info(f"Listando vehículos - skip: {skip}, limit: {limit}", extra={"request_id": request_id})
    
    db_vehiculo = crud.crud_vehiculo.get_vehiculo(db=db, skip=skip, limit=limit)
    api_logger.debug(f"Se encontraron {len(db_vehiculo)} vehículos", extra={"request_id": request_id})
    
    return db_vehiculo

@vehiculo.post("/vehiculo/", response_model=schemas.schema_vehiculo.Vehiculo, tags=["Vehiculos"])
def create_vehiculo(request: Request, vehiculo_data: schemas.schema_vehiculo.VehiculoCreate, db: Session = Depends(get_db)):
    request_id = getattr(request.state, 'request_id', 'N/A')
    api_logger.info(f"Intentando crear vehículo - Placas: {vehiculo_data.placas}", extra={"request_id": request_id})
    
    db_vehiculo = crud.crud_vehiculo.get_vehiculo_by_nombre(db, placas=vehiculo_data.placas)
    
    if db_vehiculo:
        api_logger.warning(f"Intento de crear vehículo duplicado - Placas: {vehiculo_data.placas}", extra={"request_id": request_id})
        raise HTTPException(status_code=400, detail="Vehiculo existente intenta nuevamente")
    
    try:
        result = crud.crud_vehiculo.create_vehiculo(db=db, vehiculo=vehiculo_data)
        api_logger.info(f"Vehículo creado exitosamente - ID: {result.Id}, Placas: {result.placas}", extra={"request_id": request_id})
        return result
    except Exception as e:
        api_logger.error(f"Error al crear vehículo: {str(e)}", extra={"request_id": request_id}, exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno al crear vehículo")

@vehiculo.put("/vehiculo/{id}", response_model=schemas.schema_vehiculo.Vehiculo, tags=["Vehiculos"])
async def update_vehiculo(request: Request, id: int, vehiculo_data: schemas.schema_vehiculo.VehiculoUpdate, db: Session = Depends(get_db)):
    request_id = getattr(request.state, 'request_id', 'N/A')
    api_logger.info(f"Intentando actualizar vehículo - ID: {id}", extra={"request_id": request_id})
    
    db_vehiculo = crud.crud_vehiculo.update_vehiculo(db=db, id=id, vehiculo=vehiculo_data)
    
    if db_vehiculo is None:
        api_logger.warning(f"Intento de actualizar vehículo inexistente - ID: {id}", extra={"request_id": request_id})
        raise HTTPException(status_code=404, detail="Vehiculos no existe, no actualizado")
    
    api_logger.info(f"Vehículo actualizado exitosamente - ID: {id}", extra={"request_id": request_id})
    return db_vehiculo

@vehiculo.delete("/vehiculo/{id}", response_model=schemas.schema_vehiculo.Vehiculo, tags=["Vehiculos"])
async def delete_vehiculo(request: Request, id: int, db: Session = Depends(get_db)):
    request_id = getattr(request.state, 'request_id', 'N/A')
    api_logger.info(f"Intentando eliminar vehículo - ID: {id}", extra={"request_id": request_id})
    
    db_vehiculo = crud.crud_vehiculo.delete_vehiculo(db=db, id=id)
    
    if db_vehiculo is None:
        api_logger.warning(f"Intento de eliminar vehículo inexistente - ID: {id}", extra={"request_id": request_id})
        raise HTTPException(status_code=404, detail="El vehiculo no existe, no se pudo eliminar")
    
    api_logger.info(f"Vehículo eliminado exitosamente - ID: {id}", extra={"request_id": request_id})
    return db_vehiculo