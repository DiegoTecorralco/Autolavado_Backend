'''
    Descripting for servicios
'''

from sqlalchemy import Column, Integer, String, Boolean, DataTime, Enum, Date
from sqlalchemy.orm import relationship
from config.db import Base

class Servicio(Base):
    ''' Docstring for Servicios'''
    _tablename_ = "tbb_servicios"
    Id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60))
    description = Column(String(100))
    costo = Column(Integer)
    estado = Column(Boolean)
    duracion_minutos = Column(Integer)
    fecha_registro = Column(DataTime)
    fecha_modificacion = Column(DataTime)
