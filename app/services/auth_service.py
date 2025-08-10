"""
Servicio de autenticación - Login, logout y gestión de tokens
"""

from datetime import datetime, timedelta, timezone
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
from app.models.invalidated_token import InvalidatedToken

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
            # Crear instancia de SecurityService con la sesión de BD
            security_service = SecurityService(self.db)
            
            # Verificar refresh token (incluye verificación de blacklist)
            payload = security_service.verify_refresh_token(refresh_token)
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
            # Crear instancia de SecurityService con la sesión de BD
            security_service = SecurityService(self.db)
            
            # Verificar token (incluye verificación de blacklist)
            payload = security_service.verify_access_token(token)
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
    
    def logout(self, refresh_token: str, access_token: str = None) -> bool:
        """
        Cerrar sesión invalidando tokens (access y refresh)
        
        Args:
            refresh_token: Token de refresco a invalidar
            access_token: Token de acceso a invalidar (opcional)
            
        Returns:
            True si se cerró la sesión correctamente
        """
        try:
            # Crear instancia de SecurityService con la sesión de BD
            security_service = SecurityService(self.db)
            
            # Verificar que el refresh token es válido (incluye verificación de blacklist)
            payload = security_service.verify_refresh_token(refresh_token)
            if not payload:
                return False
            
            user_id = payload.get("user_id")
            company_id = payload.get("company_id")
            
            if not user_id or not company_id:
                return False
            
            # Invalidar el refresh token
            refresh_token_hash = security_service.hash_token(refresh_token)
            
            # Calcular expiración del refresh token
            refresh_expires_at = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
            
            # Agregar refresh token a la blacklist
            blacklisted_refresh = InvalidatedToken(
                token_hash=refresh_token_hash,
                user_id=user_id,
                company_id=company_id,
                expires_at=refresh_expires_at,
                token_type="refresh"
            )
            
            self.db.add(blacklisted_refresh)
            
            # Si se proporciona un access token, invalidarlo también
            if access_token:
                try:
                    # Verificar que el access token es válido
                    access_payload = security_service.verify_access_token(access_token)
                    if access_payload:
                        # Generar hash del access token
                        access_token_hash = security_service.hash_token(access_token)
                        
                        # Calcular expiración del access token
                        access_expires_at = datetime.fromtimestamp(access_payload.get("exp"), tz=timezone.utc)
                        
                        # Agregar access token a la blacklist
                        blacklisted_access = InvalidatedToken(
                            token_hash=access_token_hash,
                            user_id=user_id,
                            company_id=company_id,
                            expires_at=access_expires_at,
                            token_type="access"
                        )
                        
                        self.db.add(blacklisted_access)
                        print(f"✅ Access token invalidado durante logout")
                except Exception as e:
                    print(f"⚠️ No se pudo invalidar access token: {e}")
            
            self.db.commit()
            
            return True
            
        except Exception as e:
            # Rollback en caso de error
            self.db.rollback()
            print(f"Error durante logout: {e}")
            return False
    
    def invalidate_access_token(self, access_token: str) -> bool:
        """
        Invalidar un token de acceso específico
        
        Args:
            access_token: Token de acceso a invalidar
            
        Returns:
            True si se invalidó correctamente
        """
        try:
            # Verificar que el access token es válido
            security_service = SecurityService(self.db)
            payload = security_service.verify_access_token(access_token)
            
            if not payload:
                return False
            
            user_id = payload.get("user_id")
            company_id = payload.get("company_id")
            
            if not user_id or not company_id:
                return False
            
            # Generar hash del token
            token_hash = security_service.hash_token(access_token)
            
            # Calcular expiración del token
            expires_at = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
            
            # Agregar token a la blacklist
            blacklisted_token = InvalidatedToken(
                token_hash=token_hash,
                user_id=user_id,
                company_id=company_id,
                expires_at=expires_at,
                token_type="access"
            )
            
            self.db.add(blacklisted_token)
            self.db.commit()
            
            return True
            
        except Exception as e:
            self.db.rollback()
            print(f"Error invalidando access token: {e}")
            return False
    
    def _invalidate_user_access_tokens(self, user_id: str, company_id: str):
        """
        Invalidar todos los tokens de acceso de un usuario para una empresa específica
        Este método es opcional y más agresivo - invalida tokens incluso si no se han usado
        
        Args:
            user_id: ID del usuario
            company_id: ID de la empresa
        """
        try:
            # Buscar tokens de acceso que aún no han expirado
            current_time = datetime.now(timezone.utc)
            
            # Nota: Esta implementación es conceptual ya que no tenemos un registro
            # de todos los tokens emitidos. En una implementación real, podrías:
            # 1. Mantener un registro de tokens emitidos
            # 2. Usar un sistema de rotación de claves secretas
            # 3. Implementar un mecanismo de "family tokens"
            
            pass
            
        except Exception as e:
            print(f"Error invalidando tokens de acceso: {e}") 