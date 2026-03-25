'''
Docstring for schemas.schema_reporte
'''
from datetime import datetime
from pydantic import BaseModel

class ReporteBase(BaseModel):
    '''Clase para modelar los campos de tabla Reportes del autolavado'''
    cajero_nombre_completo: str
    operativo_nombre_completo: str  # NUEVO CAMPO
    nombre_servicio: str
    descuento: int
    costo_servicio: float
    descripcion: str
    placas: str
    marca: str
    modelo: str
    color: str
    estado: bool
    fecha_registro: datetime
    fecha_actualizacion: datetime

# pylint: disable=too-few-public-methods, unnecessary-pass
class ReporteCreate(ReporteBase):
    '''Clase para crear un Reporte basado en la tabla Reportes'''
    pass

class ReporteUpdate(ReporteBase):
    '''Clase para actualizar un Reporte basado en la tabla Reportes'''
    pass

class Reporte(ReporteBase):
    '''Clase para realizar operaciones por ID en tabla Reportes'''
    Id: int
    
    class Config:
        '''Utilizar el orm para ejecutar las funcionalidades'''
        orm_mode = True