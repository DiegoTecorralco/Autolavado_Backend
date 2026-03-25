'''
Esta clase permite generar el modelo para los reportes del autolavado
'''
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
# pylint: disable=import-error
from config.db import Base

# pylint: disable=too-few-public-methods
class Reporte(Base):
    '''Clase para especificar tabla de reportes del autolavado'''
    __tablename__ = "tbc_reportes"
    
    Id = Column(Integer, primary_key=True, index=True)
    
    # Campos del reporte
    cajero_nombre_completo = Column(String(180))  # nombre + primer_apellido + segundo_apellido
    operativo_nombre_completo = Column(String(180))  # NUEVO CAMPO: nombre del operativo que realiza el servicio
    nombre_servicio = Column(String(60))
    descuento = Column(Integer)
    costo_servicio = Column(Float)
    descripcion = Column(String(150))
    placas = Column(String(10))
    marca = Column(String(60))
    modelo = Column(String(10))
    color = Column(String(60))
    
    # Campos de auditoría
    estado = Column(Boolean, default=True)
    fecha_registro = Column(DateTime)
    fecha_actualizacion = Column(DateTime)