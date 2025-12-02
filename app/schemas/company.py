"""
Esquemas para la entidad Company
"""

from typing import Optional, List
from datetime import datetime
from pydantic import Field

from .base import BaseSchema, BaseResponse


class CompanyCreate(BaseSchema):
    """Esquema para crear una empresa"""
    
    name: str = Field(..., min_length=1, description="Nombre de la empresa")


class CompanyUpdate(BaseSchema):
    """Esquema para actualizar una empresa"""
    
    name: Optional[str] = Field(None, min_length=1, description="Nombre de la empresa")


class CompanyRead(BaseResponse):
    """Esquema para leer una empresa"""
    
    name: str = Field(..., description="Nombre de la empresa")
    is_active: bool = Field(..., description="Estado activo de la empresa")
    
    class Config:
        from_attributes = True


class CompanyList(BaseSchema):
    """Esquema para lista de empresas"""
    
    companies: List[CompanyRead] = Field(..., description="Lista de empresas")
    total: int = Field(..., description="Total de empresas")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de página")
    pages: int = Field(..., description="Total de páginas")


class CompanyUserRead(BaseSchema):
    """Esquema para leer la relación usuario-empresa"""
    
    user_id: str = Field(..., description="ID del usuario")
    user_name: str = Field(..., description="Nombre del usuario")
    user_email: str = Field(..., description="Email del usuario")
    joined_at: datetime = Field(..., description="Fecha de ingreso a la empresa")
    is_active: bool = Field(..., description="Estado activo en la empresa")
    
    class Config:
        from_attributes = True


class CompanyWithUserCreate(BaseSchema):
    """Esquema para crear una empresa con un usuario"""
    
    company_name: str = Field(..., min_length=1, description="Nombre de la empresa")
    user_name: str = Field(..., min_length=1, description="Nombre del usuario")
    user_email: str = Field(..., description="Email del usuario")
    company_id: Optional[str] = Field(None, description="ID de la empresa que crea la empresa")


class CompanyWithUserResponse(BaseSchema):
    """Esquema para la respuesta de crear empresa con usuario"""
    
    company_id: str = Field(..., description="ID de la empresa creada")
    user_id: str = Field(..., description="ID del usuario creado")
    admin_role_id: str = Field(..., description="ID del rol admin creado")