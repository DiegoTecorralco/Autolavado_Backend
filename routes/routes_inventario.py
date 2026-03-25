from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from config.db import SessionLocal
from config.security import get_current_user
import crud.crud_inventario
import schemas.schema_inventario

router = APIRouter(prefix="/inventario", tags=["Inventario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============ PRODUCTOS ============
@router.get("/productos/", response_model=List[schemas.schema_inventario.Producto])
async def read_productos(
    skip: int = 0,
    limit: int = 100,
    categoria: Optional[str] = None,
    estado: Optional[bool] = None,
    stock_bajo: bool = False,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    productos = crud.crud_inventario.get_productos(
        db, skip=skip, limit=limit,
        categoria=categoria, estado=estado, stock_bajo=stock_bajo
    )
    return productos

@router.get("/productos/{producto_id}", response_model=schemas.schema_inventario.Producto)
async def read_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    producto = crud.crud_inventario.get_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/productos/", response_model=schemas.schema_inventario.Producto)
async def create_producto(
    producto: schemas.schema_inventario.ProductoCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    # Verificar si ya existe el código
    existing = crud.crud_inventario.get_producto_by_codigo(db, producto.codigo)
    if existing:
        raise HTTPException(status_code=400, detail="El código del producto ya existe")
    
    db_producto = crud.crud_inventario.create_producto(db, producto)
    if not db_producto:
        raise HTTPException(status_code=400, detail="Error al crear el producto")
    
    return db_producto

@router.put("/productos/{producto_id}", response_model=schemas.schema_inventario.Producto)
async def update_producto(
    producto_id: int,
    producto: schemas.schema_inventario.ProductoUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_producto = crud.crud_inventario.update_producto(db, producto_id, producto)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.delete("/productos/{producto_id}", response_model=schemas.schema_inventario.Producto)
async def delete_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_producto = crud.crud_inventario.delete_producto(db, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# ============ MOVIMIENTOS ============
@router.get("/movimientos/", response_model=List[schemas.schema_inventario.MovimientoInventario])
async def read_movimientos(
    producto_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    movimientos = crud.crud_inventario.get_movimientos(
        db, producto_id=producto_id, skip=skip, limit=limit
    )
    return movimientos

@router.post("/movimientos/", response_model=schemas.schema_inventario.MovimientoInventario)
async def create_movimiento(
    movimiento: schemas.schema_inventario.MovimientoInventarioCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_movimiento = crud.crud_inventario.create_movimiento(db, movimiento)
    if not db_movimiento:
        raise HTTPException(
            status_code=400, 
            detail="Error al crear movimiento. Verifique stock disponible o tipo de movimiento"
        )
    return db_movimiento

# ============ REPORTES ============
@router.get("/reportes/stock-bajo/", response_model=List[schemas.schema_inventario.Producto])
async def get_stock_bajo(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    productos = crud.crud_inventario.get_productos_stock_bajo(db)
    return productos

@router.get("/reportes/resumen/")
async def get_resumen(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    resumen = crud.crud_inventario.get_resumen_inventario(db)
    return resumen