"""
Esquemas base con configuración común para todos los esquemas
"""

from datetime import datetime
from typing import Optional, Any, Dict
import uuid
from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    """Esquema base con configuración común"""
    
    model_config = ConfigDict(
        from_attributes=True,  # Permite acceso a atributos del modelo
        str_strip_whitespace=True,  # Elimina espacios en blanco
        validate_assignment=True,  # Valida al asignar valores
        extra="forbid",  # No permite campos extra
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class BaseResponse(BaseSchema):
    """Respuesta base con campos comunes"""
    
    id: uuid.UUID = Field(..., description="ID del registro")
    created_at: Optional[datetime] = Field(..., description="Fecha de creación")


class ErrorResponse(BaseSchema):
    """Esquema para respuestas de error"""
    
    detail: str = Field(..., description="Mensaje de error")
    error_code: Optional[str] = Field(None, description="Código de error")
    field: Optional[str] = Field(None, description="Campo que causó el error")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp del error")


class PaginationParams(BaseSchema):
    """Parámetros de paginación"""
    
    page: int = Field(default=1, ge=1, description="Número de página")
    size: int = Field(default=10, ge=1, le=100, description="Tamaño de página")
    skip: Optional[int] = Field(None, description="Registros a saltar")
    limit: Optional[int] = Field(None, description="Límite de registros")


class SortParams(BaseSchema):
    """Parámetros de ordenamiento"""
    
    sort_by: Optional[str] = Field(None, description="Campo por el cual ordenar")
    sort_order: Optional[str] = Field(default="asc", pattern="^(asc|desc)$", description="Orden de clasificación")


class FilterParams(BaseSchema):
    """Parámetros de filtrado"""
    
    search: Optional[str] = Field(None, description="Término de búsqueda")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo") 