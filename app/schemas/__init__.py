"""
Esquemas Pydantic v2 para la aplicación base_auth_backend
"""

from .base import BaseSchema, BaseResponse, ErrorResponse
from .company import CompanyCreate, CompanyRead, CompanyUpdate, CompanyList
from .user import UserCreate, UserRead, UserUpdate, UserList, UserLogin
from .auth import Token, TokenData, LoginRequest, RefreshRequest
from .role import RoleCreate, RoleRead, RoleUpdate, RoleList
from .permission import PermissionRead, PermissionList
from .response import SuccessResponse, PaginatedResponse

__all__ = [
    "BaseSchema",
    "BaseResponse", 
    "ErrorResponse",
    "CompanyCreate",
    "CompanyRead",
    "CompanyUpdate",
    "CompanyList",
    "UserCreate",
    "UserRead", 
    "UserUpdate",
    "UserList",
    "UserLogin",
    "Token",
    "TokenData",
    "LoginRequest",
    "RefreshRequest",
    "RoleCreate",
    "RoleRead",
    "RoleUpdate", 
    "RoleList",
    "PermissionRead",
    "PermissionList",
    "SuccessResponse",
    "PaginatedResponse"
]
