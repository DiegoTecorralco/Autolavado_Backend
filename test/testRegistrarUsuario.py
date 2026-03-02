import pytest
import sys
import os

# Añadir el directorio padre al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import Session
from config.db import SessionLocal
from models.model_rol import Rol
from models.model_usuario import Usuario  # Importar modelo de usuario

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """
    Fixture que se ejecuta automáticamente antes de todas las pruebas
    """
    db = SessionLocal()
    
    try:
        # Verificar si ya existe el rol con ID 1
        rol_existente = db.query(Rol).filter(Rol.Id == 1).first()
        
        if not rol_existente:
            print("🔄 Insertando rol con ID 1...")
            rol_admin = Rol(
                Id=1,
                nombre_rol="Administrador",
                estado=True,
                fecha_registro="2026-02-24T20:05:05.948Z",
                fecha_actualizacion="2026-02-24T20:05:05.948Z"
            )
            db.add(rol_admin)
            
            # Crear otros roles necesarios
            roles = [
                Rol(nombre_rol="Cajero", estado=True, 
                    fecha_registro="2026-02-24T20:05:05.948Z", 
                    fecha_actualizacion="2026-02-24T20:05:05.948Z"),
                Rol(nombre_rol="Operativo", estado=True, 
                    fecha_registro="2026-02-24T20:05:05.948Z", 
                    fecha_actualizacion="2026-02-24T20:05:05.948Z"),
                Rol(nombre_rol="Cliente", estado=True, 
                    fecha_registro="2026-02-24T20:05:05.948Z", 
                    fecha_actualizacion="2026-02-24T20:05:05.948Z")
            ]
            
            for rol in roles:
                db.add(rol)
            
            db.commit()
            print("✅ Roles insertados correctamente")
        else:
            print(f"✅ El rol con ID 1 ya existe: {rol_existente.nombre_rol}")
        
        # Verificar y limpiar usuario de prueba si existe
        usuario_existente = db.query(Usuario).filter(
            Usuario.correo_electronico == "teco@gmail.com"
        ).first()
        
        if usuario_existente:
            print(f"⚠️ Eliminando usuario existente: {usuario_existente.correo_electronico}")
            db.delete(usuario_existente)
            db.commit()
            print("✅ Usuario eliminado para prueba limpia")
            
        total_roles = db.query(Rol).count()
        print(f"📊 Total de roles en BD: {total_roles}")
            
    except Exception as e:
        print(f"❌ Error en setup: {e}")
        db.rollback()
    finally:
        db.close()
    
    yield

def test_crear_usuario_exitoso():
    # Usar un correo único con timestamp para evitar duplicados
    import time
    email_unico = f"teco_{int(time.time())}@gmail.com"
    
    payload = {
        "rol_Id": 1,
        "nombre": "Diego",
        "primer_apellido": "Tecorralco",
        "segundo_apellido": "Martinez",
        "direccion": "la chingada",
        "correo_electronico": email_unico,  # Email único
        "numero_telefono": "1234567890",
        "contrasena": "123456",
        "estado": True,
        "fecha_registro": "2026-02-24T20:05:05.948Z",
        "fecha_actualizacion": "2026-02-24T20:05:05.948Z"
    }

    print(f"🔄 Intentando crear usuario con email: {email_unico}")
    
    response = client.post("/usuario", json=payload)

    print(f"📨 Status code: {response.status_code}")
    if response.status_code != 200 and response.status_code != 201:
        print(f"❌ Error response: {response.text}")
    
    assert response.status_code == 201 or response.status_code == 200
    
    data = response.json()
    assert data["correo_electronico"] == email_unico
    assert data["nombre"] == "Diego"
    assert "contrasena" not in data
    
    print(f"✅ Usuario creado exitosamente: {data['correo_electronico']}")

def test_crear_usuario_con_email_existente():
    """Prueba que debe fallar si el email ya existe"""
    # Primero crear un usuario
    payload = {
        "rol_Id": 1,
        "nombre": "Aby",
        "primer_apellido": "Morales",
        "segundo_apellido": "gonzales",
        "direccion": "por mi casa",
        "correo_electronico": "aby@gmail.com",
        "numero_telefono": "776852145",
        "contrasena": "123456",
        "estado": True,
        "fecha_registro": "2026-02-24T20:05:05.948Z",
        "fecha_actualizacion": "2026-02-24T20:05:05.948Z"
    }
    
    # Crear primer usuario
    response1 = client.post("/usuario", json=payload)
    assert response1.status_code in [200, 201]
    
    # Intentar crear otro con el mismo email
    response2 = client.post("/usuario", json=payload)

    # Debería fallar con 400 (Bad Request) por email duplicado
    assert response2.status_code == 400
    print("✅ Validación de email duplicado correcta")

def test_crear_usuario_datos_invalidos():
    payload_invalido = {"rol_Id": "no-es-un-numero", "nombre": "Error"}
    
    response = client.post("/usuario", json=payload_invalido)
    assert response.status_code == 422

# Función para insertar roles manualmente
def insertar_roles_manualmente():
    """Función para insertar roles manualmente si es necesario"""
    print("=== INSERTANDO DATOS DE PRUEBA MANUALMENTE ===")
    db = SessionLocal()
    try:
        # Verificar si ya existe el rol con ID 1
        rol = db.query(Rol).filter(Rol.Id == 1).first()
        
        if not rol:
            print("🔄 Insertando rol con ID 1...")
            nuevo_rol = Rol(
                Id=1,
                nombre_rol="Administrador",
                estado=True,
                fecha_registro="2026-02-24T20:05:05.948Z",
                fecha_actualizacion="2026-02-24T20:05:05.948Z"
            )
            db.add(nuevo_rol)
            db.commit()
            print("✅ Rol administrador insertado correctamente")
        else:
            print(f"✅ El rol administrador ya existe (ID: {rol.Id}, Nombre: {rol.nombre_rol})")
            
        # Mostrar todos los roles
        todos_roles = db.query(Rol).all()
        print("\n📋 Roles en la base de datos:")
        for r in todos_roles:
            print(f"   - ID: {r.Id}, Nombre: {r.nombre_rol}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    insertar_roles_manualmente()
    print("\n=== EJECUTANDO PRUEBAS ===")
    pytest.main([__file__, "-v", "--tb=short"])