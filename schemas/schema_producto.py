'''
Docstring for schemas.schema_producto
'''
from datetime import datetime
from pydantic import BaseModel

class ProductoBase(BaseModel):
    '''Clase para modelar los campos de tabla Productos'''
    nombre: str
    descripcion: str
    precio_compra: float
    precio_venta: float
    cantidad_stock: int
    unidad_medida: str
    categoria: str
    estado: bool
    fecha_registro: datetime
    fecha_actualizacion: datetime

# pylint: disable=too-few-public-methods, unnecessary-pass
class ProductoCreate(ProductoBase):
    '''Clase para crear un Producto basado en la tabla Productos'''
    pass

class ProductoUpdate(ProductoBase):
    '''Clase para actualizar un Producto basado en la tabla Productos'''
    pass

class Producto(ProductoBase):
    '''Clase para realizar operaciones por ID en tabla Productos'''
    Id: int
    
    class Config:
        '''Utilizar el orm para ejecutar las funcionalidades'''
        orm_mode = True