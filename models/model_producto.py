'''
Esta clase permite generar el modelo para los productos
'''
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
# pylint: disable=import-error
from config.db import Base

# pylint: disable=too-few-public-methods
class Producto(Base):
    '''Clase para especificar tabla de productos'''
    __tablename__ = "tbc_productos"
    Id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60))
    descripcion = Column(String(150))
    precio_compra = Column(Float)
    precio_venta = Column(Float)
    cantidad_stock = Column(Integer)
    unidad_medida = Column(String(20))
    categoria = Column(String(50))
    estado = Column(Boolean)
    fecha_registro = Column(DateTime)
    fecha_actualizacion = Column(DateTime)