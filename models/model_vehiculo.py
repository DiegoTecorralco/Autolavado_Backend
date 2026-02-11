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
    usuario_Id = Column(Integer, ForeignKey("tbb_usuarios.Id"))
    Placa = Column(String(60))
    modelo = Column(String(60))
    matricula = Column(String(60))
    color = Column(String(60))
    tipo = Column(String(60))
    anio = Column(Integer)
    estado = Column(Boolean)
    fecha_registro = Column(DataTime)
    fecha_modificacion = Column(DataTime)