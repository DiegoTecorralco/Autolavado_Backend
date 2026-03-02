from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Vehiculo(Base):
    __tablename__ = "tbb_vehiculos"
    
    Id = Column(Integer, primary_key=True, index=True)
    usuario_Id = Column(Integer, ForeignKey("tbb_usuarios.Id"))
    placas = Column(String(10))  # Cambiado de 'placa' a 'placas' para coincidir con schema
    marca = Column(String(60))
    modelo = Column(String(10))
    anio = Column(Integer)
    color = Column(String(60))
    tipo = Column(String(50))
    numero_serie = Column(String(60))  # Cambiado de 'serie' a 'numero_serie'
    estado = Column(Boolean)  # Cambiado de 'estatus' a 'estado'
    fecha_registro = Column(DateTime)
    fecha_actualizacion = Column(DateTime)

    usuarios = relationship("Usuario", back_populates="vehiculos")
    usuarios_vehiculos_servicios_V = relationship("UsuarioVehiculoServicio", back_populates="vehiculos")