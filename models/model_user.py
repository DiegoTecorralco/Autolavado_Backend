'''
    Aquí estará el modelo de user
'''
from sqlalchemy import Column, Integer, String, Boolean, DataTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class User(Base):
    '''Docsting for User'''
    _tablename_ = "tbb_users"
    Id = Column(Integer, primary_key=True, index=True)
    rol_Id = Column(Integer, ForeignKey("tbc_roles.Id"))
    nombre = Column(String(60))
    primer_apellido = Column(String(60))
    segundo_apellido = Column(String(60))
    direccion = Column(String(200))
    correo_electronico = Column(String(100))
    numero_telefono = Column(String(20))
    contrasena = Column(String(40))
    estado = Column(Boolean)
    fecha_registro = Column(DataTime)
    fecha_modificacion = Column(DataTime)
