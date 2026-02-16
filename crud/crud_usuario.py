import models.model_usuario
import schemas.schema_usuario
from sqlalchemy.orm import Session
import models, schemas

def get_usuario(db: Session,skip: int = 0, limit: int = 100):
    return db.query(models.model_usuario.Usuario).offset(skip).limit(limit).all()

def get_usuario_by_nombre(db: Session, nombre: str):
    return db.query(models.model_usuario.Usuario).filter(models.model_usuario.Usuario.nombre == nombre).first()

def create_usuario(db:Session, usuario: schemas.schema_usuario.UsuarioCreate):
    db_usuario = models.model_usuario.Usuario(
        rol_Id = usuario.rol_Id,
        nombre = usuario.nombre,
        primer_apellido = usuario.primer_apellido,
        segundo_apellido = usuario.segundo_apellido,
        direccion = usuario.direccion,
        correo_electronico = usuario.correo_electronico,
        numero_telefono = usuario.numero_telefono,
        contrasena = usuario.contrasena,
        estado = usuario.estado,
        fecha_registro = usuario.fecha_registro,
        fecha_actualizacion = usuario.fecha_actualizacion
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db:Session, id: int, usuario: schemas.schema_usuario.UsuarioUpdate):
    
    db_usuario = db.query(models.model_usuario.Usuario).filter(models.model_usuario.Usuario.Id == id).first()
    if db_usuario:
        for var, value in vars(usuario).items():
            setattr(db_usuario, var, value) if value else None
        db.add(db_usuario)
        db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, id: int):
    db_usuario = db.query(models.model_usuario.Usuario).filter(models.model_usuario.Usuario.Id == id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario