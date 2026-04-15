import models.model_vehiculo
import schemas.schema_vehiculo
from sqlalchemy.orm import Session
import models, schemas
from config.logger import db_logger

def get_vehiculo(db: Session, skip: int = 0, limit: int = 100):
    db_logger.debug(f"Obteniendo vehículos - skip: {skip}, limit: {limit}")
    return db.query(models.model_vehiculo.Vehiculo).offset(skip).limit(limit).all()

def get_vehiculo_by_nombre(db: Session, placas: str):
    db_logger.debug(f"Buscando vehículo por placas: {placas}")
    # CORREGIDO: models.model_vehiculo en lugar de models.model_vehiculos
    return db.query(models.model_vehiculo.Vehiculo).filter(models.model_vehiculo.Vehiculo.placas == placas).first()

def create_vehiculo(db: Session, vehiculo: schemas.schema_vehiculo.VehiculoCreate):
    db_logger.info(f"Intentando crear vehículo - Placas: {vehiculo.placas}")
    
    try:
        db_vehiculo = models.model_vehiculo.Vehiculo(
            usuario_Id = vehiculo.usuario_Id,
            placas = vehiculo.placas,
            marca = vehiculo.marca,
            modelo = vehiculo.modelo,
            anio = vehiculo.anio,
            color = vehiculo.color,
            tipo = vehiculo.tipo,
            numero_serie = vehiculo.numero_serie,
            estado = vehiculo.estado,
            fecha_registro = vehiculo.fecha_registro,
            fecha_actualizacion = vehiculo.fecha_actualizacion
        )
        db.add(db_vehiculo)
        db.commit()
        db.refresh(db_vehiculo)
        
        db_logger.info(f"Vehículo creado exitosamente - ID: {db_vehiculo.Id}, Placas: {vehiculo.placas}")
        return db_vehiculo
        
    except Exception as e:
        db_logger.error(f"Error al crear vehículo {vehiculo.placas}: {str(e)}", exc_info=True)
        raise

def update_vehiculo(db: Session, id: int, vehiculo: schemas.schema_vehiculo.VehiculoUpdate):
    db_logger.info(f"Intentando actualizar vehículo - ID: {id}")
    
    # CORREGIDO: models.model_vehiculo en lugar de models.model_vehiculos
    db_vehiculo = db.query(models.model_vehiculo.Vehiculo).filter(models.model_vehiculo.Vehiculo.Id == id).first()
    
    if db_vehiculo:
        for var, value in vars(vehiculo).items():
            setattr(db_vehiculo, var, value) if value else None
        db.add(db_vehiculo)
        db.commit()
        db.refresh(db_vehiculo)
        db_logger.info(f"Vehículo actualizado exitosamente - ID: {id}")
    else:
        db_logger.warning(f"Intento de actualizar vehículo inexistente - ID: {id}")
    
    return db_vehiculo

def delete_vehiculo(db: Session, id: int):
    db_logger.info(f"Intentando eliminar vehículo - ID: {id}")
    
    # CORREGIDO: models.model_vehiculo en lugar de models.model_vehiculos
    db_vehiculo = db.query(models.model_vehiculo.Vehiculo).filter(models.model_vehiculo.Vehiculo.Id == id).first()
    
    if db_vehiculo:
        db.delete(db_vehiculo)
        db.commit()
        db_logger.info(f"Vehículo eliminado exitosamente - ID: {id}")
    else:
        db_logger.warning(f"Intento de eliminar vehículo inexistente - ID: {id}")
    
    return db_vehiculo