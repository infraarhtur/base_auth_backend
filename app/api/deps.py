"""
Dependencias comunes para la API
"""

from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import AppUser
from app.models.permission import Permission
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.company_service import CompanyService
from app.services.role_service import RoleService

# Configurar seguridad HTTP Bearer
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> AppUser:
    """
    Obtener usuario actual desde token JWT
    
    Args:
        credentials: Credenciales del token
        db: Sesión de base de datos
        
    Returns:
        Usuario actual
        
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    auth_service = AuthService(db)
    user = auth_service.get_current_user_from_token(credentials.credentials)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_active_user(
    current_user: AppUser = Depends(get_current_user)
) -> AppUser:
    """
    Obtener usuario actual activo
    
    Args:
        current_user: Usuario actual
        
    Returns:
        Usuario activo
        
    Raises:
        HTTPException: Si el usuario está inactivo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    return current_user


def get_user_permissions(
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[str]:
    """
    Obtener permisos del usuario actual
    
    Args:
        current_user: Usuario actual
        db: Sesión de base de datos
        
    Returns:
        Lista de nombres de permisos del usuario
    """
    # Obtener roles del usuario
    user_roles = (
        db.query(UserRole)
        .filter(UserRole.user_id == current_user.id)
        .all()
    )
    
    # Obtener permisos de todos los roles del usuario
    permissions = set()
    for user_role in user_roles:
        role_permissions = (
            db.query(Permission)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .filter(RolePermission.role_id == user_role.role_id)
            .all()
        )
        
        for permission in role_permissions:
            permissions.add(permission.name)
    
    return list(permissions)


def require_permission(permission_name: str):
    """
    Decorador para requerir un permiso específico
    
    Args:
        permission_name: Nombre del permiso requerido
        
    Returns:
        Función de dependencia
    """
    def permission_dependency(
        permissions: List[str] = Depends(get_user_permissions)
    ) -> bool:
        if permission_name not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso requerido: {permission_name}"
            )
        return True
    
    return permission_dependency


# Dependencias de servicios
def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    try:
        return AuthService(db)
    except Exception as e:
        db.rollback()
        raise e


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


def get_company_service(db: Session = Depends(get_db)) -> CompanyService:
    return CompanyService(db)


def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(db)


# Dependencias de permisos específicos
require_user_read = require_permission("user:read")
require_user_create = require_permission("user:create")
require_user_update = require_permission("user:update")
require_user_delete = require_permission("user:delete")

require_company_read = require_permission("company:read")
require_company_create = require_permission("company:create")
require_company_update = require_permission("company:update")
require_company_delete = require_permission("company:delete")

require_role_read = require_permission("role:read")
require_role_create = require_permission("role:create")
require_role_update = require_permission("role:update")
require_role_delete = require_permission("role:delete")

require_permission_read = require_permission("permission:read")
require_permission_assign = require_permission("permission:assign")
