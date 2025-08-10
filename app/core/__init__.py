"""
Core module para la aplicación base_auth_backend
"""

from .config import get_settings, settings, AppSettings, DatabaseSettings, SecuritySettings
from .logging import setup_logging, get_logger
from .security import (
    verify_password,
    get_password_hash,
    validate_password_strength,
    sanitize_input,
    validate_email
)

__all__ = [
    # Configuración
    "get_settings",
    "settings",
    "AppSettings",
    "DatabaseSettings", 
    "SecuritySettings",
    
    # Logging
    "setup_logging",
    "get_logger",
    
    # Seguridad
    "verify_password",
    "get_password_hash",
    "validate_password_strength",
    "sanitize_input",
    "validate_email"
]
