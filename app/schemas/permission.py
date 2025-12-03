"""
Esquemas para permisos
"""

from typing import List
import uuid
from pydantic import Field
from datetime import datetime

from .base import BaseSchema, BaseResponse


class PermissionRead(BaseSchema):
    """Esquema para leer un permiso"""
    
    id: uuid.UUID = Field(..., description="ID del registro")
    name: str = Field(..., description="Nombre del permiso")
    is_super_admin: bool = Field(default=False, description="Indica si es un permiso de super administrador")
    
    class Config:
        from_attributes = True


class PermissionList(BaseSchema):
    """Esquema para lista de permisos"""
    
    permissions: List[PermissionRead] = Field(..., description="Lista de permisos")
    total: int = Field(..., description="Total de permisos")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de página")
    pages: int = Field(..., description="Total de páginas")


class UserPermissions(BaseSchema):
    """Esquema para permisos de un usuario"""
    
    user_id: uuid.UUID = Field(..., description="ID del usuario")
    permissions: List[str] = Field(..., description="Lista de nombres de permisos")
    roles: List[str] = Field(..., description="Lista de nombres de roles") 