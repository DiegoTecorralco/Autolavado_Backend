import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from config.logger import api_logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generar ID único
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        start_time = time.time()
        
        # Log de entrada
        api_logger.info(
            f"→ {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else "unknown"
            }
        )
        
        try:
            response = await call_next(request)
            duration = (time.time() - start_time) * 1000
            
            # Log de salida
            api_logger.info(
                f"← {response.status_code} {request.method} {request.url.path} ({duration:.2f}ms)",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "duration_ms": round(duration, 2)
                }
            )
            
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            api_logger.error(
                f"✗ Error en {request.method} {request.url.path}: {str(e)}",
                extra={"request_id": request_id},
                exc_info=True
            )
            raise