"""
Fixtures para datos de autenticación en pruebas
"""

import pytest
from typing import Dict, Any


@pytest.fixture
def valid_access_token() -> str:
    """Token de acceso válido de ejemplo"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3MzU2ODAwMDB9.example_signature"


@pytest.fixture
def expired_access_token() -> str:
    """Token de acceso expirado de ejemplo"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3MzU2ODAwMDB9.expired_signature"


@pytest.fixture
def valid_refresh_token() -> str:
    """Token de refresh válido de ejemplo"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJleHAiOjE3MzU2ODAwMDB9.refresh_signature"


@pytest.fixture
def expired_refresh_token() -> str:
    """Token de refresh expirado de ejemplo"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJleHAiOjE3MzU2ODAwMDB9.expired_refresh_signature"


@pytest.fixture
def valid_password_reset_token() -> str:
    """Token de reset de contraseña válido de ejemplo"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3MzU2ODAwMDB9.reset_signature"


@pytest.fixture
def expired_password_reset_token() -> str:
    """Token de reset de contraseña expirado de ejemplo"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3MzU2ODAwMDB9.expired_reset_signature"


@pytest.fixture
def valid_email_verification_token() -> str:
    """Token de verificación de email válido de ejemplo"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3MzU2ODAwMDB9.verification_signature"


@pytest.fixture
def expired_email_verification_token() -> str:
    """Token de verificación de email expirado de ejemplo"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3MzU2ODAwMDB9.expired_verification_signature"


@pytest.fixture
def valid_session_token() -> str:
    """Token de sesión válido de ejemplo"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzIiwiZXhwIjoxNzM1NjgwMDAwfQ.session_signature"


@pytest.fixture
def expired_session_token() -> str:
    """Token de sesión expirado de ejemplo"""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzIiwiZXhwIjoxNzM1NjgwMDAwfQ.expired_session_signature"


@pytest.fixture
def invalid_token() -> str:
    """Token inválido de ejemplo"""
    return "invalid.token.format"


@pytest.fixture
def malformed_token() -> str:
    """Token malformado de ejemplo"""
    return "not.a.valid.jwt.token"


@pytest.fixture
def token_payload() -> Dict[str, Any]:
    """Payload de ejemplo para tokens"""
    return {
        "sub": "123",
        "email": "test@example.com",
        "permissions": ["read", "write"],
        "role": "user"
    }


@pytest.fixture
def refresh_token_payload() -> Dict[str, Any]:
    """Payload de ejemplo para refresh tokens"""
    return {
        "sub": "123",
        "type": "refresh"
    }


@pytest.fixture
def password_reset_payload() -> Dict[str, Any]:
    """Payload de ejemplo para tokens de reset de contraseña"""
    return {
        "email": "test@example.com",
        "type": "password_reset"
    }


@pytest.fixture
def email_verification_payload() -> Dict[str, Any]:
    """Payload de ejemplo para tokens de verificación de email"""
    return {
        "email": "test@example.com",
        "type": "email_verification"
    }


@pytest.fixture
def session_payload() -> Dict[str, Any]:
    """Payload de ejemplo para tokens de sesión"""
    return {
        "user_id": "123",
        "permissions": ["read", "write", "delete"],
        "company_id": "456"
    }


@pytest.fixture
def login_credentials() -> Dict[str, str]:
    """Credenciales de ejemplo para login"""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!"
    }


@pytest.fixture
def invalid_login_credentials() -> Dict[str, str]:
    """Credenciales de ejemplo inválidas para login"""
    return {
        "email": "invalid@example.com",
        "password": "wrongpassword"
    }


@pytest.fixture
def registration_data() -> Dict[str, Any]:
    """Datos de ejemplo para registro de usuario"""
    return {
        "name": "New User",
        "email": "newuser@example.com",
        "password": "NewPassword123!",
        "confirm_password": "NewPassword123!"
    }


@pytest.fixture
def invalid_registration_data() -> Dict[str, Any]:
    """Datos de ejemplo inválidos para registro de usuario"""
    return {
        "name": "",
        "email": "invalid-email",
        "password": "123",
        "confirm_password": "different"
    }


@pytest.fixture
def invalid_auth_headers() -> Dict[str, str]:
    """Headers de autenticación inválidos"""
    return {"Authorization": "Bearer invalid_token_here"}


@pytest.fixture
def no_auth_headers() -> Dict[str, str]:
    """Headers sin autenticación"""
    return {}


@pytest.fixture
def change_password_data() -> Dict[str, str]:
    """Datos para cambio de contraseña válidos"""
    return {
        "current_password": "currentpassword",
        "new_password": "newpassword123",
        "confirm_password": "newpassword123"
    }


@pytest.fixture
def invalid_change_password_data() -> Dict[str, str]:
    """Datos para cambio de contraseña inválidos"""
    return {
        "current_password": "wrongpassword",
        "new_password": "newpassword123",
        "confirm_password": "newpassword123"
    } 