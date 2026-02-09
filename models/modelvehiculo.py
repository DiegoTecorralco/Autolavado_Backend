'''
    Descripting for modelVehiculo
'''

from sqlalchemy import Column, Integer, String, Boolean, DataTime, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base
class Vehiculo(Base):
    ''' Docstring for Vehiculo'''
    _tablename_ = "tbb_vehiculo"
    Id = Column(Integer, primary_key=True, index=True)
    Id = Column(Integer, ForeignKey("tbc_roles.Id"))
    matricula = Column(String(60))
    modelo = Column(String(60))
    color = Column(String(60))
    telefono_owner = Column(String(15))
    estatus = Column(Boolean)
    fecha_registro = Column(DataTime)
    fecha_modificacion = Column(DataTime)