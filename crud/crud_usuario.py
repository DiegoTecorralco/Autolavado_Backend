import models.model_usuario
import schemas.schema_usuario
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
import models, schemas
from config.logger import db_logger, auth_logger

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_usuario(db: Session,skip: int = 0, limit: int = 100):
    db_logger.debug(f"Obteniendo usuarios - skip: {skip}, limit: {limit}")
    return db.query(models.model_usuario.Usuario).offset(skip).limit(limit).all()

def get_usuario_by_nombre(db: Session, nombre: str):
    db_logger.debug(f"Buscando usuario por nombre: {nombre}")
    return db.query(models.model_usuario.Usuario).filter(models.model_usuario.Usuario.nombre == nombre).first()

def get_usuario_by_correo(db: Session, correo: str):
    db_logger.debug(f"Buscando usuario por correo: {correo}")
    return db.query(models.model_usuario.Usuario).filter(models.model_usuario.Usuario.correo_electronico == correo).first()

def create_usuario(db:Session, usuario: schemas.schema_usuario.UsuarioCreate):
    db_logger.info(f"Intentando crear usuario - Nombre: {usuario.nombre}, Email: {usuario.correo_electronico}")
    
    try:
        password_plana = str(usuario.contrasena).strip()
        hashed_password = pwd_context.hash(password_plana)
        
        db_usuario = models.model_usuario.Usuario(
            rol_Id = usuario.rol_Id,
            nombre = usuario.nombre,
            primer_apellido = usuario.primer_apellido,
            segundo_apellido = usuario.segundo_apellido,
            direccion = usuario.direccion,
            correo_electronico = usuario.correo_electronico,
            numero_telefono = usuario.numero_telefono,
            contrasena = hashed_password,
            estado = usuario.estado,
            fecha_registro = usuario.fecha_registro,
            fecha_actualizacion = usuario.fecha_actualizacion
        )
        
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        
        db_logger.info(f"Usuario creado exitosamente - ID: {db_usuario.Id}, Nombre: {usuario.nombre}")
        return db_usuario
        
    except Exception as e:
        db_logger.error(f"Error al crear usuario {usuario.nombre}: {str(e)}", exc_info=True)
        raise

def update_usuario(db:Session, id: int, usuario: schemas.schema_usuario.UsuarioUpdate):
    db_logger.info(f"Intentando actualizar usuario - ID: {id}")
    
    db_usuario = db.query(models.model_usuario.Usuario).filter(models.model_usuario.Usuario.Id == id).first()
    
    if db_usuario:
        for var, value in vars(usuario).items():
            setattr(db_usuario, var, value) if value else None
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        db_logger.info(f"Usuario actualizado exitosamente - ID: {id}")
    else:
        db_logger.warning(f"Intento de actualizar usuario inexistente - ID: {id}")
    
    return db_usuario

def delete_usuario(db: Session, id: int):
    db_logger.info(f"Intentando eliminar usuario - ID: {id}")
    
    db_usuario = db.query(models.model_usuario.Usuario).filter(models.model_usuario.Usuario.Id == id).first()
    
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
        db_logger.info(f"Usuario eliminado exitosamente - ID: {id}")
    else:
        db_logger.warning(f"Intento de eliminar usuario inexistente - ID: {id}")
    
    return db_usuario

def authenticate_user(db: Session, email_o_tel: str, contrasena: str):
    auth_logger.info(f"Intento de autenticación para: {email_o_tel}")
    
    usuario = db.query(models.model_usuario.Usuario).filter(
        (models.model_usuario.Usuario.correo_electronico == email_o_tel) |
        (models.model_usuario.Usuario.numero_telefono == email_o_tel)
    ).first()
    
    if not usuario:
        auth_logger.warning(f"Autenticación fallida - Usuario no encontrado: {email_o_tel}")
        return None
    
    try:
        if not pwd_context.verify(contrasena, usuario.contrasena):
            auth_logger.warning(f"Autenticación fallida - Contraseña incorrecta para: {email_o_tel}")
            return None
    except UnknownHashError:
        auth_logger.error(f"Hash inválido en BD para usuario: {email_o_tel}", exc_info=True)
        return None
    
    auth_logger.info(f"Autenticación exitosa - Usuario ID: {usuario.Id}, Email: {usuario.correo_electronico}")
    return usuario