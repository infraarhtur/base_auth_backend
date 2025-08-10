"""
Esquemas para autenticación y JWT
"""

from datetime import datetime
from typing import Optional, List
from pydantic import Field

from .base import BaseSchema


class LoginRequest(BaseSchema):
    """Esquema para solicitud de login"""
    
    email: str = Field(..., description="Email del usuario")
    hashed_password: str = Field(..., description="Hash de la contraseña del usuario")
    company_name: str = Field(..., description="Nombre de la empresa")
    remember_me: Optional[bool] = Field(False, description="Recordar sesión")


class Token(BaseSchema):
    """Esquema para token JWT"""
    
    access_token: str = Field(..., description="Token de acceso")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Tiempo de expiración en segundos")
    refresh_token: Optional[str] = Field(None, description="Token de refresco")


class TokenData(BaseSchema):
    """Esquema para datos del token"""
    
    user_id: str = Field(..., description="ID del usuario")
    email: str = Field(..., description="Email del usuario")
    name: str = Field(..., description="Nombre del usuario")
    permissions: List[str] = Field(default=[], description="Lista de permisos")
    company_id: Optional[str] = Field(None, description="ID de la empresa actual")
    company_name: Optional[str] = Field(None, description="Nombre de la empresa actual")
    exp: Optional[datetime] = Field(None, description="Fecha de expiración")


class RefreshRequest(BaseSchema):
    """Esquema para solicitud de refresco de token"""
    
    refresh_token: str = Field(..., description="Token de refresco")


class LogoutRequest(BaseSchema):
    """Esquema para solicitud de logout"""
    
    refresh_token: Optional[str] = Field(None, description="Token de refresco a invalidar")


class PasswordResetRequest(BaseSchema):
    """Esquema para solicitud de reset de contraseña"""
    
    email: str = Field(..., description="Email del usuario")


class PasswordResetConfirm(BaseSchema):
    """Esquema para confirmar reset de contraseña"""
    
    token: str = Field(..., description="Token de reset")
    new_password: str = Field(..., min_length=8, description="Nueva contraseña")


class EmailVerificationRequest(BaseSchema):
    """Esquema para solicitud de verificación de email"""
    
    email: str = Field(..., description="Email del usuario")


class EmailVerificationConfirm(BaseSchema):
    """Esquema para confirmar verificación de email"""
    
    token: str = Field(..., description="Token de verificación") 