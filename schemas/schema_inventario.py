from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

# ============ PRODUCTOS (usando campos existentes) ============
class ProductoBase(BaseModel):
    '''Base para productos usando campos existentes de tbc_productos'''
    # Mapear campos existentes
    nombre: str = Field(..., max_length=60)
    descripcion: Optional[str] = Field(None, max_length=150)
    categoria: str = Field(..., max_length=50)
    unidad_medida: str = Field(..., max_length=20)
    precio_compra: float = Field(..., gt=0)
    precio_venta: float = Field(..., gt=0)
    cantidad_stock: int = Field(0, ge=0)  # ← este es stock_actual
    estado: bool = True
    
    # Campos adicionales que inventario necesita (opcionales)
    codigo: Optional[str] = Field(None, max_length=50)  # se puede generar automático
    stock_minimo: int = Field(5, ge=0)  # valor por defecto
    stock_maximo: int = Field(100, ge=0)  # valor por defecto   
    
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    
    @field_validator('precio_venta')
    @classmethod
    def precio_venta_mayor_compra(cls, v, info):
        if 'precio_compra' in info.data and v <= info.data['precio_compra']:
            raise ValueError('El precio de venta debe ser mayor al precio de compra')
        return v

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    unidad_medida: Optional[str] = None
    precio_compra: Optional[float] = None
    precio_venta: Optional[float] = None
    cantidad_stock: Optional[int] = None
    codigo: Optional[str] = None
    stock_minimo: Optional[int] = None
    stock_maximo: Optional[int] = None
    estado: Optional[bool] = None

class Producto(ProductoBase):
    Id: int
    model_config = ConfigDict(from_attributes=True)

# ============ MOVIMIENTOS DE INVENTARIO ============
class MovimientoInventarioBase(BaseModel):
    producto_Id: int
    tipo_movimiento: str  # ENTRADA, SALIDA, AJUSTE
    cantidad: int = Field(..., gt=0)
    motivo: Optional[str] = None
    usuario_Id: int
    observaciones: Optional[str] = None

class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass

class MovimientoInventario(MovimientoInventarioBase):
    Id: int
    stock_anterior: int
    stock_nuevo: int
    fecha_movimiento: datetime
    fecha_registro: datetime
    model_config = ConfigDict(from_attributes=True)

# ============ REPORTES Y FILTROS ============
class ProductoStockBajo(BaseModel):
    Id: int
    nombre: str
    cantidad_stock: int
    stock_minimo: int
    diferencia: int

class ReporteMovimiento(BaseModel):
    producto_Id: int
    producto_nombre: str
    tipo_movimiento: str
    cantidad: int
    fecha_movimiento: datetime
    usuario_nombre: str
    motivo: Optional[str]