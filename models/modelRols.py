'''
    Aqui estará el modelo de los roles
'''

from sqlalchemy import Column, Integer, String, Boolean
from config.db import Base

class Rol(Base):
    ''' En este apartado se define la clase con sus atriutos'''
    _tablename_ = "tbc_roles"

    Id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(60))
    estatus = Column(Boolean)
    