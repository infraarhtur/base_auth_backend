"""
Configuración del proyecto base_auth_backend
Basado en las mejores prácticas de FastAPI para settings y environment variables
"""

from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Configuración de la base de datos PostgreSQL"""
    
    url: str = Field(
        default="postgresql://user:password@localhost/base_auth_db",
        alias="DATABASE_URL",
        description="URL de conexión a PostgreSQL"
    )
    echo: bool = Field(
        default=False,
        alias="DATABASE_ECHO",
        description="Mostrar queries SQL en logs"
    )
    pool_size: int = Field(
        default=10,
        alias="DATABASE_POOL_SIZE",
        description="Tamaño del pool de conexiones"
    )
    max_overflow: int = Field(
        default=20,
        alias="DATABASE_MAX_OVERFLOW",
        description="Máximo overflow del pool"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


class SecuritySettings(BaseSettings):
    """Configuración de seguridad y JWT"""
    
    secret_key: str = Field(
        default="your-secret-key-here",
        description="Clave secreta para JWT"
    )
    algorithm: str = Field(
        default="HS256",
        description="Algoritmo para JWT"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Tiempo de expiración del access token en minutos"
    )
    refresh_token_expire_days: int = Field(
        default=7,
        description="Tiempo de expiración del refresh token en días"
    )


class AppSettings(BaseSettings):
    """Configuración principal de la aplicación"""
    
    # Configuración básica de la app
    title: str = Field(
        default="Base Auth Backend",
        description="Título de la aplicación"
    )
    version: str = Field(
        default="0.1.0",
        description="Versión de la aplicación"
    )
    debug: bool = Field(
        default=False,
        description="Modo debug"
    )
    
    # Configuración de logging
    log_level: str = Field(
        default="INFO",
        description="Nivel de logging"
    )
    
    # Configuraciones específicas
    database: DatabaseSettings = Field(
        default_factory=DatabaseSettings,
        description="Configuración de base de datos"
    )
    security: SecuritySettings = Field(
        default_factory=SecuritySettings,
        description="Configuración de seguridad"
    )
    
    # Configuración de Pydantic Settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache
def get_settings() -> AppSettings:
    """
    Obtiene la configuración de la aplicación.
    Usa lru_cache para evitar leer el archivo .env múltiples veces.
    """
    return AppSettings()


# Instancia global de configuración
settings = get_settings()
