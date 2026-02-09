'''
    Descripting for servicio
'''

from sqlalchemy import Column, Integer, String, Boolean, DataTime, Enum, Date
from sqlalchemy.orm import relationship
from config.db import Base
class Servicio(Base):
    ''' Docstring for Servicio'''
    _tablename_ = "tbb_servicio"
    Id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60))
    description = Column(String(100))
    costo = Column(Integer)
    estatus = Column(Boolean)
    fecha_registro = Column(DataTime)
    fecha_modificacion = Column(DataTime)
