'''
Docstring for schemas.schema_rol
'''
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    '''Clase para modelar los campos de tabla Usuarios'''
    nombre: str
    primer_apellido: str
    segundo_apellido: str
    direccion: str
    correo_electronico: str
    numero_telefono: str
    contrasena: str
    estatus: bool
    fecha_registro: datetime
    fecha_Actualizacion: datetime
# pylint: disable=too-few-public-methods, unnecessary-pass
class UserCreate(UserBase):
    '''Clase para crear un Rol basado en la tabla Rols'''
    pass
class UserUpdate(UserBase):
    '''Clase para actualizar un Rol basado en la tabla Rols'''
    pass

class User(UserBase):
    '''Clase para realizar operaciones por ID en tabla Rol'''
    Id: int
    class Config:
        '''Utilizar el orm para ejecutar las funcionalidades'''
        orm_mode =True

class UserLogin(BaseModel):
    '''Clase para realizar login por numero de telefono o correo'''
    numero_telefono: Optional[str] = None
    correo_electronico: Optional[str] = None
    contrasena: str