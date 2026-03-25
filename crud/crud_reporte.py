'''
Docstring for crud.crud_reporte
'''
from sqlalchemy.orm import Session
from models.model_reporte import Reporte as ReporteModel
from schemas.schema_reporte import ReporteCreate, ReporteUpdate

def get_reporte(db: Session, skip: int = 0, limit: int = 100):
    '''Obtiene todos los reportes'''
    return db.query(ReporteModel).offset(skip).limit(limit).all()

def get_reporte_by_id(db: Session, id: int):
    '''Obtiene un reporte por su ID'''
    return db.query(ReporteModel).filter(ReporteModel.Id == id).first()

def get_reporte_by_placas(db: Session, placas: str):
    '''Obtiene reportes por placas del vehículo'''
    return db.query(ReporteModel).filter(ReporteModel.placas == placas).all()

def get_reporte_by_servicio(db: Session, nombre_servicio: str):
    '''Obtiene reportes por nombre del servicio'''
    return db.query(ReporteModel).filter(ReporteModel.nombre_servicio == nombre_servicio).all()

def get_reporte_by_cajero(db: Session, cajero_nombre: str):
    '''Obtiene reportes por nombre del cajero'''
    return db.query(ReporteModel).filter(ReporteModel.cajero_nombre_completo == cajero_nombre).all()

def get_reporte_by_operativo(db: Session, operativo_nombre: str):
    '''Obtiene reportes por nombre del operativo'''
    return db.query(ReporteModel).filter(ReporteModel.operativo_nombre_completo == operativo_nombre).all()

def create_reporte(db: Session, reporte: ReporteCreate):
    '''Crea un nuevo reporte'''
    db_reporte = ReporteModel(
        cajero_nombre_completo=reporte.cajero_nombre_completo,
        operativo_nombre_completo=reporte.operativo_nombre_completo,  # NUEVO CAMPO
        nombre_servicio=reporte.nombre_servicio,
        descuento=reporte.descuento,
        costo_servicio=reporte.costo_servicio,
        descripcion=reporte.descripcion,
        placas=reporte.placas,
        marca=reporte.marca,
        modelo=reporte.modelo,
        color=reporte.color,
        estado=reporte.estado,
        fecha_registro=reporte.fecha_registro,
        fecha_actualizacion=reporte.fecha_actualizacion
    )
    db.add(db_reporte)
    db.commit()
    db.refresh(db_reporte)
    return db_reporte

def update_reporte(db: Session, id: int, reporte: ReporteUpdate):
    '''Actualiza un reporte existente'''
    db_reporte = db.query(ReporteModel).filter(ReporteModel.Id == id).first()
    if db_reporte:
        for key, value in reporte.dict().items():
            setattr(db_reporte, key, value)
        db.commit()
        db.refresh(db_reporte)
    return db_reporte

def delete_reporte(db: Session, id: int):
    '''Elimina un reporte'''
    db_reporte = db.query(ReporteModel).filter(ReporteModel.Id == id).first()
    if db_reporte:
        db.delete(db_reporte)
        db.commit()
    return db_reporte