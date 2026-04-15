import sys
import os
# Añadir la ruta del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app
from config.logger import api_logger

client = TestClient(app)

# Datos de prueba
test_usuario = {
    "rol_Id": 1,
    "nombre": "Prueba",
    "primer_apellido": "Test",
    "segundo_apellido": "Logger",
    "direccion": "Calle Test 123",
    "correo_electronico": "test@autolavado.com",
    "numero_telefono": "1234567890",
    "contrasena": "test123",
    "estado": True,
    "fecha_registro": "2024-01-01T00:00:00",
    "fecha_actualizacion": "2024-01-01T00:00:00"
}

test_vehiculo = {
    "usuario_Id": 1,
    "placas": "TEST123",
    "marca": "Toyota",
    "modelo": "Corolla",
    "anio": 2020,
    "color": "Rojo",
    "tipo": "Sedan",
    "numero_serie": "ABC123456",
    "estado": True,
    "fecha_registro": "2024-01-01T00:00:00",
    "fecha_actualizacion": "2024-01-01T00:00:00"
}

def get_token():
    """Obtener token de autenticación"""
    api_logger.info("=== Obteniendo token de autenticación para pruebas ===")
    
    # Primero crear usuario si no existe
    response_create = client.post("/usuario/", json=test_usuario)
    api_logger.info(f"Crear usuario - Status: {response_create.status_code}")
    
    # Login
    response = client.post("/login/", data={
        "username": "test@autolavado.com",
        "password": "test123"
    })
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        api_logger.info("✓ Token obtenido exitosamente")
        return token
    else:
        api_logger.error(f"✗ Error obteniendo token: {response.text}")
        return None

def test_create_vehiculo():
    """Prueba: Crear un vehículo"""
    api_logger.info("\n=== INICIANDO PRUEBA: Crear vehículo ===")
    
    token = get_token()
    if not token:
        api_logger.error("No se pudo obtener token, abortando prueba")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/vehiculo/", json=test_vehiculo, headers=headers)
    
    api_logger.info(f"Status code: {response.status_code}")
    api_logger.info(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        api_logger.info("✓ Prueba de creación exitosa")
        return data["Id"]
    else:
        api_logger.error("✗ Prueba de creación falló")
        return None

def test_get_vehiculos():
    """Prueba: Listar vehículos"""
    api_logger.info("\n=== INICIANDO PRUEBA: Listar vehículos ===")
    
    token = get_token()
    if not token:
        api_logger.error("No se pudo obtener token, abortando prueba")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/vehiculo/", headers=headers)
    
    api_logger.info(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        api_logger.info(f"Vehículos encontrados: {len(response.json())}")
        api_logger.info("✓ Prueba de listado exitosa")
    else:
        api_logger.error("✗ Prueba de listado falló")

def test_vehiculo_duplicado():
    """Prueba: Intentar crear vehículo duplicado (debe fallar)"""
    api_logger.info("\n=== INICIANDO PRUEBA: Crear vehículo duplicado (debe fallar) ===")
    
    token = get_token()
    if not token:
        api_logger.error("No se pudo obtener token, abortando prueba")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Primer intento
    response1 = client.post("/vehiculo/", json=test_vehiculo, headers=headers)
    api_logger.info(f"Primer intento - Status: {response1.status_code}")
    
    # Segundo intento (duplicado)
    response2 = client.post("/vehiculo/", json=test_vehiculo, headers=headers)
    api_logger.info(f"Segundo intento (duplicado) - Status: {response2.status_code}")
    
    if response2.status_code == 400:
        api_logger.info("✓ Prueba de duplicado exitosa (error esperado)")
    else:
        api_logger.error("✗ Prueba de duplicado falló - debería dar error 400")

# Ejecutar todas las pruebas
if __name__ == "__main__":
    api_logger.info("\n" + "="*60)
    api_logger.info("INICIANDO BATERÍA DE PRUEBAS COMPLETA")
    api_logger.info("="*60)
    
    try:
        test_create_vehiculo()
        test_get_vehiculos()
        test_vehiculo_duplicado()
        
        api_logger.info("\n" + "="*60)
        api_logger.info("✓ TODAS LAS PRUEBAS FINALIZARON")
        api_logger.info("="*60)
    except Exception as e:
        api_logger.error(f"\n✗ ERROR EN PRUEBAS: {str(e)}", exc_info=True)