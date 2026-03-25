from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base

class ProductoInventario(Base):
    '''Vista/relación para productos de inventario - NO CREA TABLA, solo referencia'''
    __tablename__ = "tbc_productos"
    __table_args__ = {'extend_existing': True, 'autoload_with': None}  # No autoload
    
    # Usar los campos EXISTENTES de la tabla productos
    Id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(60))  # campo existente
    descripcion = Column(String(150))  # campo existente
    precio_compra = Column(Float)  # campo existente
    precio_venta = Column(Float)  # campo existente
    cantidad_stock = Column(Integer)  # ← este es stock_actual en inventario
    unidad_medida = Column(String(20))  # campo existente
    categoria = Column(String(50))  # campo existente
    estado = Column(Boolean)  # campo existente
    fecha_registro = Column(DateTime)  # campo existente
    fecha_actualizacion = Column(DateTime)  # campo existente
    
    # Propiedades computadas para compatibilidad con inventario
    @property
    def stock_actual(self):
        return self.cantidad_stock
    
    @stock_actual.setter
    def stock_actual(self, value):
        self.cantidad_stock = value
    
    @property
    def stock_minimo(self):
        return getattr(self, '_stock_minimo', 5)
    
    @stock_minimo.setter
    def stock_minimo(self, value):
        self._stock_minimo = value
    
    @property
    def stock_maximo(self):
        return getattr(self, '_stock_maximo', 100)
    
    @stock_maximo.setter
    def stock_maximo(self, value):
        self._stock_maximo = value
    
    @property
    def codigo(self):
        return getattr(self, '_codigo', str(self.Id))
    
    @codigo.setter
    def codigo(self, value):
        self._codigo = value
    
    movimientos = relationship("MovimientoInventario", back_populates="producto")

class MovimientoInventario(Base):
    '''Clase para registrar movimientos de inventario'''
    __tablename__ = "tbd_movimientos_inventario"
    
    Id = Column(Integer, primary_key=True, index=True)
    producto_Id = Column(Integer, ForeignKey("tbc_productos.Id"))
    tipo_movimiento = Column(String(20), nullable=False)
    cantidad = Column(Integer, nullable=False)
    stock_anterior = Column(Integer, nullable=False)
    stock_nuevo = Column(Integer, nullable=False)
    motivo = Column(String(200), nullable=True)
    usuario_Id = Column(Integer, ForeignKey("tbb_usuarios.Id"))
    fecha_movimiento = Column(DateTime, default=datetime.now)
    observaciones = Column(Text, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.now)
    
    producto = relationship("ProductoInventario", back_populates="movimientos") 