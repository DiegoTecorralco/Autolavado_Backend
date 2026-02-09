'''
    DEscripting for modelCliente
'''

from sqlalchemy import Column, Integer, String, Boolean, DataTime, Enum, Date
from sqlalchemy.orm import relationship
from config.db import Base
class Cliente(Base):
    ''' Docstring for Cliente'''
    _tablename_ = "tbb_cliente"
    Id = Column(Integer, primary_key=True, index=True)
    Id = Column(Integer, ForeignKey("tbc_roles.Id"))
    nombre = Column(String(60))
    papellido = Column(String(60))
    sapellido = Column(String(60))
    usuario = Column(String(60))
    telefono = Column(String(15))
    estatus = Column(Boolean)
    fecha_registro = Column(DataTime)
    fecha_modificacion = Column(DataTime)