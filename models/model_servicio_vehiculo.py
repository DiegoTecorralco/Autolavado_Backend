'''
    Descripting for modelCliente
'''

from sqlalchemy import Column, Integer, String, Boolean, DataTime, Time, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Solicitud():
    Programada = " Programada"
    Proceso = "Proceso"
    Realizada = "Realizada"
    Cancelada = "Cancelada"

# pylint_ disable=too-few-public-methods
class VehiculoServicio(Base):
    ''' Docstring for serviciovehivulo'''
    _tablename_ = "tbb_cliente"
    Id = Column(Integer, primary_key=True, index=True)
    vehiculo_Id = Column(Integer, ForeignKey("tbb_vehiculo.Id"))
    cajero_Id = Column(Integer, ForeignKey("tbb_usuarios.Id"))
    operativo_Id = Column(Integer, ForeignKey("tbb_usuarios.Id"))
    lavador_Id = Column(Integer, ForeignKey("tbc_servicio.Id"))
    fecha = column(DataTime)
    hora = Column(Time)
    estatus = Column(Enum(Solicitud))
    estado = Column(Boolean)
    fecha_registro = Column(DataTime)
    fecha_modificacion = Column(DataTime)