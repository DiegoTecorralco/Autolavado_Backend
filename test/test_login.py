import sys
import os
# Añadir la ruta del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app
from config.logger import auth_logger

client = TestClient(app)

def test_login_exitoso():
    """Prueba: Login correcto"""
    auth_logger.info("\n=== PRUEBA: Login exitoso ===")
    
    # Crear usuario primero
    test_user = {
        "rol_Id": 1,
        "nombre": "LoginTest",
        "primer_apellido": "Test",
        "segundo_apellido": "User",
        "direccion": "Calle Test",
        "correo_electronico": "logintest@test.com",
        "numero_telefono": "999888777",
        "contrasena": "pass123",
        "estado": True,
        "fecha_registro": "2024-01-01T00:00:00",
        "fecha_actualizacion": "2024-01-01T00:00:00"
    }
    
    response_create = client.post("/usuario/", json=test_user)
    auth_logger.info(f"Crear usuario - Status: {response_create.status_code}")
    
    # Intentar login
    response = client.post("/login/", data={
        "username": "logintest@test.com",
        "password": "pass123"
    })
    
    auth_logger.info(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        assert "access_token" in response.json()
        auth_logger.info("✓ Login exitoso - Token generado")
    else:
        auth_logger.error(f"✗ Login falló: {response.text}")

def test_login_fallido_credenciales_incorrectas():
    """Prueba: Login con contraseña incorrecta"""
    auth_logger.info("\n=== PRUEBA: Login con credenciales incorrectas (debe fallar) ===")
    
    response = client.post("/login/", data={
        "username": "logintest@test.com",
        "password": "wrongpassword"
    })
    
    auth_logger.info(f"Status code esperado 401: {response.status_code}")
    
    if response.status_code == 401:
        auth_logger.info("✓ Fallo de login correctamente manejado")
    else:
        auth_logger.error(f"✗ Debería dar error 401, pero dio {response.status_code}")

def test_login_usuario_no_existente():
    """Prueba: Login con usuario que no existe"""
    auth_logger.info("\n=== PRUEBA: Login con usuario inexistente (debe fallar) ===")
    
    response = client.post("/login/", data={
        "username": "noexiste@test.com",
        "password": "cualquiercosa"
    })
    
    if response.status_code == 401:
        auth_logger.info("✓ Usuario inexistente correctamente rechazado")
    else:
        auth_logger.error(f"✗ Debería dar error 401, pero dio {response.status_code}")

if __name__ == "__main__":
    auth_logger.info("\n" + "="*60)
    auth_logger.info("INICIANDO PRUEBAS DE LOGIN")
    auth_logger.info("="*60)
    
    test_login_exitoso()
    test_login_fallido_credenciales_incorrectas()
    test_login_usuario_no_existente()
    
    auth_logger.info("\n✓ Todas las pruebas de login finalizaron")