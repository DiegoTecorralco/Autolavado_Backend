'''
Docstring for crud.crud_producto
'''
from sqlalchemy.orm import Session
from models.model_producto import Producto
from schemas.schema_producto import ProductoCreate, ProductoUpdate

def get_producto(db: Session, skip: int = 0, limit: int = 100):
    '''Obtiene todos los productos'''
    return db.query(Producto).offset(skip).limit(limit).all()

def get_producto_by_nombre(db: Session, nombre: str):
    '''Obtiene un producto por su nombre'''
    return db.query(Producto).filter(Producto.nombre == nombre).first()

def get_producto_by_id(db: Session, producto_id: int):
    '''Obtiene un producto por su ID'''
    return db.query(Producto).filter(Producto.Id == producto_id).first()

def create_producto(db: Session, producto: ProductoCreate):
    '''Crea un nuevo producto'''
    db_producto = Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio_compra=producto.precio_compra,
        precio_venta=producto.precio_venta,
        cantidad_stock=producto.cantidad_stock,
        unidad_medida=producto.unidad_medida,
        categoria=producto.categoria,
        estado=producto.estado,
        fecha_registro=producto.fecha_registro,
        fecha_actualizacion=producto.fecha_actualizacion
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, id: int, producto: ProductoUpdate):
    '''Actualiza un producto existente'''
    db_producto = db.query(Producto).filter(Producto.Id == id).first()
    if db_producto:
        for key, value in producto.dict().items():
            setattr(db_producto, key, value)
        db.commit()
        db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, id: int):
    '''Elimina un producto (borrado lógico cambiando estado a False)'''
    db_producto = db.query(Producto).filter(Producto.Id == id).first()
    if db_producto:
        db_producto.estado = False
        db.commit()
        db.refresh(db_producto)
    return db_producto