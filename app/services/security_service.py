"""
Servicio de seguridad - Hash y verificación de contraseñas
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from app.core.config import get_settings
from app.core.security import verify_password as core_verify_password, get_password_hash as core_get_password_hash

# Obtener configuración
settings = get_settings()


class SecurityService:
    """Servicio para operaciones de seguridad"""
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generar hash de contraseña usando bcrypt
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            Hash de la contraseña
        """
        return core_get_password_hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verificar contraseña contra su hash
        
        Args:
            plain_password: Contraseña en texto plano
            hashed_password: Hash de la contraseña
            
        Returns:
            True si la contraseña es correcta
        """
        return core_verify_password(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Crear token JWT de acceso
        
        Args:
            data: Datos a incluir en el token
            expires_delta: Tiempo de expiración personalizado
            
        Returns:
            Token JWT
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.security.access_token_expire_minutes)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.security.secret_key, algorithm=settings.security.algorithm)
        
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """
        Crear token JWT de refresco
        
        Args:
            data: Datos a incluir en el token
            
        Returns:
            Token JWT de refresco
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.security.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        
        encoded_jwt = jwt.encode(to_encode, settings.security.secret_key, algorithm=settings.security.algorithm)
        
        return encoded_jwt
    
    @staticmethod
    def verify_access_token(token: str) -> Optional[dict]:
        """
        Verificar y decodificar token JWT de acceso
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            Datos del token si es válido, None si no
        """
        try:
            payload = jwt.decode(token, settings.security.secret_key, algorithms=[settings.security.algorithm])
            
            # Verificar que es un token de acceso
            if payload.get("type") != "access":
                return None
            
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def verify_refresh_token(token: str) -> Optional[dict]:
        """
        Verificar y decodificar token JWT de refresco
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            Datos del token si es válido, None si no
        """
        try:
            payload = jwt.decode(token, settings.security.secret_key, algorithms=[settings.security.algorithm])
            
            # Verificar que es un token de refresco
            if payload.get("type") != "refresh":
                return None
            
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """
        Verificar y decodificar token JWT (método genérico)
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            Datos del token si es válido, None si no
        """
        try:
            payload = jwt.decode(token, settings.security.secret_key, algorithms=[settings.security.algorithm])
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def generate_password_reset_token(email: str) -> str:
        """
        Generar token para reset de contraseña
        
        Args:
            email: Email del usuario
            
        Returns:
            Token JWT para reset de contraseña
        """
        data = {
            "email": email,
            "type": "password_reset",
            "exp": datetime.utcnow() + timedelta(hours=1)  # 1 hora de validez
        }
        
        return jwt.encode(data, settings.security.secret_key, algorithm=settings.security.algorithm)
    
    @staticmethod
    def verify_password_reset_token(token: str) -> Optional[str]:
        """
        Verificar token de reset de contraseña
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            Email del usuario si el token es válido, None si no
        """
        try:
            payload = jwt.decode(token, settings.security.secret_key, algorithms=[settings.security.algorithm])
            
            # Verificar que es un token de reset de contraseña
            if payload.get("type") != "password_reset":
                return None
            
            return payload.get("email")
        except JWTError:
            return None
    
    @staticmethod
    def generate_email_verification_token(email: str) -> str:
        """
        Generar token para verificación de email
        
        Args:
            email: Email del usuario
            
        Returns:
            Token JWT para verificación de email
        """
        data = {
            "email": email,
            "type": "email_verification",
            "exp": datetime.utcnow() + timedelta(hours=24)  # 24 horas de validez
        }
        
        return jwt.encode(data, settings.security.secret_key, algorithm=settings.security.algorithm)
    
    @staticmethod
    def verify_email_verification_token(token: str) -> Optional[str]:
        """
        Verificar token de verificación de email
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            Email del usuario si el token es válido, None si no
        """
        try:
            payload = jwt.decode(token, settings.security.secret_key, algorithms=[settings.security.algorithm])
            
            # Verificar que es un token de verificación de email
            if payload.get("type") != "email_verification":
                return None
            
            return payload.get("email")
        except JWTError:
            return None 