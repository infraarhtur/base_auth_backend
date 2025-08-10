"""
Servicio de autenticación - Login, logout y gestión de tokens
"""

from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import AppUser
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission
from app.models.permission import Permission
from app.models.role import Role
from app.schemas.auth import Token, TokenData, LoginRequest
from app.services.security_service import SecurityService
from app.core.config import get_settings
from sqlalchemy.dialects import postgresql

# Obtener configuración
settings = get_settings()


class AuthService:
    """Servicio para operaciones de autenticación"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def authenticate_user(self, email: str, hashed_password: str, company_name: str) -> Optional[tuple[AppUser, str]]:
        """
        Autenticar usuario con email, hash de contraseña y nombre de empresa
        
        Args:
            email: Email del usuario
            hashed_password: Hash de la contraseña del usuario
            company_name: Nombre de la empresa
            
        Returns:
            Tupla (Usuario, company_id) si la autenticación es exitosa, None si no
        """
        user = self.db.query(AppUser).filter(AppUser.email == email).first()
        
        if not user:
            return None
        
        # Comparar directamente los hashes
        if user.hashed_password != hashed_password:
            return None
        
        if not user.is_active:
            return None
        
        # Verificar que el usuario pertenece a la empresa especificada
        from app.models.company import Company
        from app.models.company_user import CompanyUser
        
        company = self.db.query(Company).filter(Company.name == company_name).first()
        if not company:
            return None
        
        # Verificar que existe la relación usuario-empresa y está activa
        company_user = (
            self.db.query(CompanyUser)
            .filter(CompanyUser.user_id == user.id)
            .filter(CompanyUser.company_id == company.id)
            .filter(CompanyUser.is_active.is_(True))
            .first()
        )
        
        if not company_user:
            return None
        
        return user, str(company.id)
    
    def get_user_permissions(self, user_id: str, company_id: str) -> List[str]:
        """
        Obtener permisos de un usuario para una empresa específica
        
        Args:
            user_id: ID del usuario
            company_id: ID de la empresa
            
        Returns:
            Lista de nombres de permisos
        """
        # Obtener roles del usuario para la empresa específica
        user_roles = (
            self.db.query(UserRole)
            .join(Role, UserRole.role_id == Role.id)
            .filter(UserRole.user_id == user_id)
            .filter(Role.company_id == company_id)  # Filtrar por empresa
            .all()
        )
        
        # Obtener permisos de todos los roles del usuario
        permissions = set()
        for user_role in user_roles:
            role_permissions = (
                self.db.query(Permission)
                .join(RolePermission, Permission.id == RolePermission.permission_id)
                .filter(RolePermission.role_id == user_role.role_id)
                .all()
            )
            
            for permission in role_permissions:
                permissions.add(permission.name)
        
        return list(permissions)
    
    def create_tokens(self, user: AppUser, company_id: str) -> Token:
        """
        Crear tokens de acceso y refresco para un usuario
        
        Args:
            user: Usuario para el cual crear tokens
            company_id: ID de la empresa
            
        Returns:
            Token con access_token y refresh_token
        """
        # Obtener permisos del usuario
        permissions = self.get_user_permissions(str(user.id), company_id)
        
        # Obtener información de la empresa
        from app.models.company import Company
        company = self.db.query(Company).filter(Company.id == company_id).first()
        
        # Datos para el token
        token_data = {
            "user_id": str(user.id),
            "email": user.email,
            "name": user.name,
            "permissions": permissions,
            "company_id": company_id,
            "company_name": company.name if company else None
        }
        
        # Crear tokens
        access_token = SecurityService.create_access_token(token_data)
        refresh_token = SecurityService.create_refresh_token(token_data)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.security.access_token_expire_minutes * 60
        )
    
    def login(self, login_data: LoginRequest) -> Token:
        """
        Autenticar usuario y crear tokens
        
        Args:
            login_data: Datos de login (email, hashed_password, company_name)
            
        Returns:
            Token con access_token y refresh_token
            
        Raises:
            HTTPException: Si las credenciales son incorrectas
        """
        result = self.authenticate_user(login_data.email, login_data.hashed_password, login_data.company_name)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user, company_id = result
        return self.create_tokens(user, company_id)
    
    def refresh_token(self, refresh_token: str) -> Token:
        """
        Renovar token de acceso usando refresh token
        
        Args:
            refresh_token: Token de refresco
            
        Returns:
            Nuevo token con access_token y refresh_token
            
        Raises:
            HTTPException: Si el refresh token es inválido
        """
        try:
            # Verificar refresh token
            payload = SecurityService.verify_refresh_token(refresh_token)
            user_id = payload.get("user_id")
            company_id = payload.get("company_id")
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token de refresco inválido"
                )
            
            # Obtener usuario
            user = self.db.query(AppUser).filter(AppUser.id == user_id).first()
            if not user or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no encontrado o inactivo"
                )
            
            return self.create_tokens(user, company_id)
            
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de refresco inválido"
            )
    
    def get_current_user_from_token(self, token: str) -> Optional[AppUser]:
        """
        Obtener usuario actual desde token de acceso
        
        Args:
            token: Token de acceso
            
        Returns:
            Usuario si el token es válido, None si no
        """
        try:
            # Verificar token
            payload = SecurityService.verify_access_token(token)
            user_id = payload.get("user_id")
            
            if not user_id:
                return None
            
            # Obtener usuario
            user = self.db.query(AppUser).filter(AppUser.id == user_id).first()
            if not user or not user.is_active:
                return None
            
            return user
            
        except Exception:
            return None
    
    def logout(self, refresh_token: str) -> bool:
        """
        Cerrar sesión (invalidar refresh token)
        
        Args:
            refresh_token: Token de refresco a invalidar
            
        Returns:
            True si se cerró la sesión correctamente
        """
        # En una implementación real, aquí se invalidaría el refresh token
        # Por ahora, simplemente verificamos que el token es válido
        try:
            SecurityService.verify_refresh_token(refresh_token)
            return True
        except Exception:
            return False 