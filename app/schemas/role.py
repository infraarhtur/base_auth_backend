"""
Esquemas para roles y permisos
"""

from typing import Optional, List
import uuid
from pydantic import Field
from .permission import PermissionRead

from .base import BaseSchema
import json


class RoleBaseResponse(BaseSchema):
    """Respuesta base para Role sin created_at"""
    
    id: uuid.UUID = Field(..., description="ID del registro")


class RoleCreate(BaseSchema):
    """Esquema para crear un rol"""
    
    name: str = Field(..., min_length=1, description="Nombre del rol")
    company_id: Optional[uuid.UUID] = Field(None, description="ID de la empresa (None para roles globales)")
    permissions: Optional[List[uuid.UUID]] = Field(None, description="Lista de IDs de permisos")


class RoleUpdate(BaseSchema):
    """Esquema para actualizar un rol"""
    
    name: Optional[str] = Field(None, min_length=1, description="Nombre del rol")
    permissions: Optional[List[uuid.UUID]] = Field(None, description="Lista de IDs de permisos")


class RoleRead(RoleBaseResponse):
    """Esquema para leer un rol"""
    
    name: str = Field(..., description="Nombre del rol")
    company_id: Optional[uuid.UUID] = Field(None, description="ID de la empresa")
    permissions: List["PermissionRead"] = Field(default=[], description="Permisos del rol")

    

    
    class Config:
        from_attributes = True


class RoleList(BaseSchema):
    """Esquema para lista de roles"""
    
    roles: List[RoleRead] = Field(..., description="Lista de roles")
    total: int = Field(..., description="Total de roles")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de página")
    pages: int = Field(..., description="Total de páginas")


class UserRoleCreate(BaseSchema):
    """Esquema para asignar rol a usuario"""
    
    user_id: uuid.UUID = Field(..., description="ID del usuario")
    role_id: uuid.UUID = Field(..., description="ID del rol")


class UserRoleRead(BaseSchema):
    """Esquema para leer asignación de rol a usuario"""
    
    user_id: uuid.UUID = Field(..., description="ID del usuario")
    role_id: uuid.UUID = Field(..., description="ID del rol")
    role: RoleRead = Field(..., description="Información del rol")
    
    class Config:
        from_attributes = True 