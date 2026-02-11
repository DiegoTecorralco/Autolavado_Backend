'''
    Aqui estará el modelo de los roles
'''

from sqlalchemy import Column, Integer, String, Boolean, DataTime
# pylint: disable=import-error

from config.db import Base
# pylint: disable=too-few-public-methods

class Rol(Base):
    ''' En este apartado se define la clase con sus atriutos'''
    __tablename__ = "tbc_roles"

    Id = Column(Integer, primary_key=True, index=True)
    nombreRol = Column(String(20))
    estado = Column(Boolean)
    fecha_registro = Column(DataTime)
    fecha_actualizacion = Column(DataTime)
