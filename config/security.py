import os
from dotenv import load_dotenv
from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException, status
#from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError,jwt

load_dotenv()

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="rol")
api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un JSON Web Token (JWT) firmado."""
    to_encode = data.copy()
    # 2. Calcular tiempo de expiración
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)) # 30 es el valor por defecto
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    # 3. Añadir el 'claim' de expiración (exp) al payload
    to_encode.update({"exp": expire})
    # 4. Codificar y firmar el token
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

'''def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username # O busca al usuario en la DB y retorna el objeto usuario
    except JWTError:
        raise credentials_exception'''

def get_current_user(token: str = Depends(api_key_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        payload = jwt.decode(
            token, 
            os.getenv("SECRET_KEY"), 
            algorithms=[os.getenv("ALGORITHM", "HS256")]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username 
    except (JWTError, IndexError, AttributeError):
        raise credentials_exception