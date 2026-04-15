import logging
import json
from datetime import datetime
from typing import Optional
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# Crear directorio de logs si no existe
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

class JSONFormatter(logging.Formatter):
    """Formateador de logs en JSON para mejor análisis"""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        
        # Añadir excepción si existe
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Añadir atributos personalizados
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'endpoint'):
            log_entry['endpoint'] = record.endpoint
            
        return json.dumps(log_entry)

def setup_logger(name: str, log_file: str = None, level=logging.INFO):
    """Configura un logger con handlers para archivo y consola"""
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicación de handlers
    if logger.handlers:
        return logger
    
    # Formateadores
    json_formatter = JSONFormatter()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo (rotación por tamaño)
    if not log_file:
        log_file = f"{LOG_DIR}/{name}.log"
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)
    
    # Handler para errores separado
    error_handler = RotatingFileHandler(
        f"{LOG_DIR}/errors.log",
        maxBytes=10*1024*1024,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(json_formatter)
    logger.addHandler(error_handler)
    
    return logger

# Loggers específicos para tu proyecto
api_logger = setup_logger("api", f"{LOG_DIR}/api.log")
db_logger = setup_logger("database", f"{LOG_DIR}/database.log")
auth_logger = setup_logger("auth", f"{LOG_DIR}/auth.log")