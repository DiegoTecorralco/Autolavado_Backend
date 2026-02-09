'''
    Descripting for modelCliente
'''

from sqlalchemy import Column, Integer, String, Boolean, DataTime, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base
class serviciovehivulo(Base):
    ''' Docstring for serviciovehivulo'''
    _tablename_ = "tbb_cliente"
    Id = Column(Integer, primary_key=True, index=True)
    cajero_Id = Column(Integer, ForeignKey("tbc_user.Id"))
    lavador_Id = Column(Integer, ForeignKey("tbc_servicio.Id"))
    vehiculo_Id = Column(Integer, ForeignKey("tbc_vehiculo.Id"))
    fecha = column(DataTime)
    estatus = Column(Boolean)
    fecha_registro = Column(DataTime)
    fecha_modificacion = Column(DataTime)