"""
Modelo base con campos comunes para todos los modelos
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Configuración de metadatos para PostgreSQL
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

# Base declarativa con metadatos personalizados
Base = declarative_base(metadata=metadata)


class BaseModel(Base):
    """
    Modelo base abstracto con campos comunes.
    Todos los modelos heredan de esta clase.
    """
    
    __abstract__ = True
    
    # Campos comunes
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self) -> str:
        """Representación string del modelo"""
        return f"<{self.__class__.__name__}(id={self.id})>" 