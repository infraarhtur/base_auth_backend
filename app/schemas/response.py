"""
Esquemas de respuesta estándar
"""

from typing import Optional, Any, List, Dict
from pydantic import Field

from .base import BaseSchema


class SuccessResponse(BaseSchema):
    """Esquema para respuestas de éxito"""
    
    success: bool = Field(True, description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de respuesta")
    data: Optional[Any] = Field(None, description="Datos de la respuesta")


class PaginatedResponse(BaseSchema):
    """Esquema para respuestas paginadas"""
    
    items: List[Any] = Field(..., description="Lista de elementos")
    total: int = Field(..., description="Total de elementos")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de página")
    pages: int = Field(..., description="Total de páginas")
    has_next: bool = Field(..., description="Tiene página siguiente")
    has_prev: bool = Field(..., description="Tiene página anterior")


class HealthCheckResponse(BaseSchema):
    """Esquema para respuesta de health check"""
    
    status: str = Field(..., description="Estado del servicio")
    version: str = Field(..., description="Versión de la aplicación")
    timestamp: str = Field(..., description="Timestamp de la verificación")
    database: str = Field(..., description="Estado de la base de datos")


class ErrorDetail(BaseSchema):
    """Esquema para detalles de error"""
    
    field: Optional[str] = Field(None, description="Campo que causó el error")
    message: str = Field(..., description="Mensaje de error")
    code: Optional[str] = Field(None, description="Código de error")


class ValidationErrorResponse(BaseSchema):
    """Esquema para errores de validación"""
    
    detail: List[ErrorDetail] = Field(..., description="Lista de errores de validación")
    error_type: str = Field("validation_error", description="Tipo de error")


class APIErrorResponse(BaseSchema):
    """Esquema para errores de API"""
    
    detail: str = Field(..., description="Mensaje de error")
    error_code: Optional[str] = Field(None, description="Código de error")
    error_type: str = Field("api_error", description="Tipo de error")
    timestamp: str = Field(..., description="Timestamp del error")


class ErrorResponse(BaseSchema):
    """Esquema para respuestas de error generales"""
    
    detail: str = Field(..., description="Mensaje de error")
    error_code: Optional[str] = Field(None, description="Código de error")
    timestamp: str = Field(..., description="Timestamp del error") 