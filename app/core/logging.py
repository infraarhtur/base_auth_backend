"""
Configuración de logging para la aplicación
"""

import logging
import sys
from typing import Optional
from app.core.config import get_settings

# Obtener configuración
settings = get_settings()


def setup_logging(log_level: Optional[str] = None) -> None:
    """
    Configurar logging para la aplicación
    
    Args:
        log_level: Nivel de logging (opcional, usa configuración por defecto si no se proporciona)
    """
    # Usar el nivel de configuración si no se proporciona uno
    if log_level is None:
        log_level = settings.log_level
    
    # Configurar formato básico
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log")
        ]
    )
    
    # Configurar loggers específicos
    loggers = [
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi",
        "sqlalchemy",
        "app"
    ]
    
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, log_level.upper()))
    
    # Log de inicio
    logging.info(f"Logging configurado con nivel: {log_level}")


def get_logger(name: str) -> logging.Logger:
    """
    Obtener un logger configurado
    
    Args:
        name: Nombre del logger
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)
