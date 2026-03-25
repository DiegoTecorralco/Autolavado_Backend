from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.model_inventario import ProductoInventario, MovimientoInventario
from schemas.schema_inventario import ProductoCreate, ProductoUpdate, MovimientoInventarioCreate
from datetime import datetime
from typing import List, Optional

# ============ PRODUCTOS ============
def get_producto(db: Session, producto_id: int):
    return db.query(ProductoInventario).filter(ProductoInventario.Id == producto_id).first()

def get_producto_by_codigo(db: Session, codigo: str):
    # Como no hay campo codigo, usamos Id como código o buscas por nombre
    return db.query(ProductoInventario).filter(ProductoInventario.Id == int(codigo)).first() if codigo.isdigit() else None

def get_productos(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    categoria: Optional[str] = None,
    estado: Optional[bool] = None,
    stock_bajo: bool = False
):
    query = db.query(ProductoInventario)
    
    if categoria:
        query = query.filter(ProductoInventario.categoria == categoria)
    
    if estado is not None:
        query = query.filter(ProductoInventario.estado == estado)
    
    if stock_bajo:
        # Usar cantidad_stock que es el campo existente
        query = query.filter(ProductoInventario.cantidad_stock <= 5)  # stock_minimo por defecto 5
    
    return query.offset(skip).limit(limit).all()

def create_producto(db: Session, producto: ProductoCreate):
    # Verificar si ya existe por nombre (campo existente)
    existing = db.query(ProductoInventario).filter(
        ProductoInventario.nombre == producto.nombre
    ).first()
    if existing:
        return None
    
    db_producto = ProductoInventario(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        categoria=producto.categoria,
        unidad_medida=producto.unidad_medida,
        precio_compra=producto.precio_compra,
        precio_venta=producto.precio_venta,
        cantidad_stock=producto.cantidad_stock,  # campo existente
        estado=producto.estado,
        fecha_registro=datetime.now(),
        fecha_actualizacion=datetime.now()
    )
    
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(db: Session, producto_id: int, producto: ProductoUpdate):
    db_producto = get_producto(db, producto_id)
    if not db_producto:
        return None
    
    update_data = producto.model_dump(exclude_unset=True)
    
    # Mapear campos: si viene stock_actual, usar cantidad_stock
    if 'stock_actual' in update_data:
        update_data['cantidad_stock'] = update_data.pop('stock_actual')
    
    for field, value in update_data.items():
        if hasattr(db_producto, field):
            setattr(db_producto, field, value)
    
    db_producto.fecha_actualizacion = datetime.now()
    db.commit()
    db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: int):
    db_producto = get_producto(db, producto_id)
    if not db_producto:
        return None
    
    db_producto.estado = False
    db_producto.fecha_actualizacion = datetime.now()
    db.commit()
    db.refresh(db_producto)
    return db_producto

def get_movimientos(
    db: Session, 
    producto_id: Optional[int] = None,
    skip: int = 0, 
    limit: int = 100
):
    query = db.query(MovimientoInventario)
    
    if producto_id:
        query = query.filter(MovimientoInventario.producto_Id == producto_id)
    
    return query.order_by(MovimientoInventario.fecha_movimiento.desc()).offset(skip).limit(limit).all()

def create_movimiento(
    db: Session, 
    movimiento: MovimientoInventarioCreate
):
    producto = get_producto(db, movimiento.producto_Id)
    if not producto:
        return None
    
    stock_anterior = producto.cantidad_stock  # usar campo existente
    cantidad = movimiento.cantidad
    
    if movimiento.tipo_movimiento.upper() == "ENTRADA":
        stock_nuevo = stock_anterior + cantidad
    elif movimiento.tipo_movimiento.upper() == "SALIDA":
        if stock_anterior < cantidad:
            return None
        stock_nuevo = stock_anterior - cantidad
    elif movimiento.tipo_movimiento.upper() == "AJUSTE":
        stock_nuevo = cantidad
    else:
        return None
    
    db_movimiento = MovimientoInventario(
        producto_Id=movimiento.producto_Id,
        tipo_movimiento=movimiento.tipo_movimiento.upper(),
        cantidad=cantidad,
        stock_anterior=stock_anterior,
        stock_nuevo=stock_nuevo,
        motivo=movimiento.motivo,
        usuario_Id=movimiento.usuario_Id,
        observaciones=movimiento.observaciones,
        fecha_movimiento=datetime.now(),
        fecha_registro=datetime.now()
    )
    
    # Actualizar usando el campo existente cantidad_stock
    producto.cantidad_stock = stock_nuevo
    producto.fecha_actualizacion = datetime.now()
    
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    return db_movimiento

def get_productos_stock_bajo(db: Session):
    productos = db.query(ProductoInventario).filter(
        ProductoInventario.estado == True,
        ProductoInventario.cantidad_stock <= 5  # stock mínimo por defecto
    ).all()
    return productos

def get_resumen_inventario(db: Session):
    total_productos = db.query(ProductoInventario).filter(ProductoInventario.estado == True).count()
    stock_bajo = db.query(ProductoInventario).filter(
        ProductoInventario.estado == True,
        ProductoInventario.cantidad_stock <= 5
    ).count()
    
    valor_inventario = db.query(ProductoInventario).filter(ProductoInventario.estado == True).all()
    valor_total = sum(p.cantidad_stock * p.precio_compra for p in valor_inventario)
    
    return {
        "total_productos": total_productos,
        "productos_stock_bajo": stock_bajo,
        "valor_total_inventario": valor_total
    }