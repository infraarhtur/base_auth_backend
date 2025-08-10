"""
Esquemas para la entidad User
"""

from typing import Optional, List
from pydantic import Field, EmailStr

from .base import BaseSchema, BaseResponse


class UserCreate(BaseSchema):
    """Esquema para crear un usuario"""
    
    name: str = Field(..., min_length=1, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=5, description="Contraseña del usuario")
    company_name: str = Field(..., description="Nombre de la compañía")
    rol: str = Field(..., description="Rol del usuario en la compañía")


class UserUpdate(BaseSchema):
    """Esquema para actualizar un usuario"""
    
    name: Optional[str] = Field(None, min_length=1, description="Nombre del usuario")
    email: Optional[EmailStr] = Field(None, description="Email del usuario")
    is_active: Optional[bool] = Field(None, description="Estado activo del usuario")


class UserRead(BaseResponse):
    """Esquema para leer un usuario"""
    
    name: str = Field(..., description="Nombre del usuario")
    email: str = Field(..., description="Email del usuario")
    is_active: bool = Field(..., description="Estado activo del usuario")
    
    class Config:
        from_attributes = True


class UserWithRoles(BaseResponse):
    """Esquema para leer un usuario con sus roles en una compañía específica"""
    
    name: str = Field(..., description="Nombre del usuario")
    email: str = Field(..., description="Email del usuario")
    is_active: bool = Field(..., description="Estado activo del usuario")
    company_name: str = Field(..., description="Nombre de la compañía")
    roles: List[str] = Field(..., description="Lista de roles del usuario en la compañía")
    
    class Config:
        from_attributes = True


class UserList(BaseSchema):
    """Esquema para lista de usuarios"""
    
    users: List[UserRead] = Field(..., description="Lista de usuarios")
    total: int = Field(..., description="Total de usuarios")
    page: int = Field(..., description="Página actual")
    size: int = Field(..., description="Tamaño de página")
    pages: int = Field(..., description="Total de páginas")


class UserLogin(BaseSchema):
    """Esquema para login de usuario"""
    
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña del usuario")
    remember_me: Optional[bool] = Field(False, description="Recordar sesión")


class UserPasswordChange(BaseSchema):
    """Esquema para cambio de contraseña"""
    
    current_password: str = Field(..., description="Contraseña actual")
    new_password: str = Field(..., min_length=8, description="Nueva contraseña")
    confirm_password: str = Field(..., description="Confirmar nueva contraseña") 