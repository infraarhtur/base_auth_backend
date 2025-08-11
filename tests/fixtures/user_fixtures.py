"""
Fixtures para datos de usuarios en pruebas
"""

import pytest
from typing import Dict, Any


@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """Datos de ejemplo para un usuario"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPassword123!",
        "is_active": True,
        "is_verified": True
    }


@pytest.fixture
def sample_user() -> Dict[str, Any]:
    """Usuario de ejemplo con ID"""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "hashed_password": "hashed_password_here",
        "is_active": True,
        "is_verified": True
    }


@pytest.fixture
def admin_user_data() -> Dict[str, Any]:
    """Datos de ejemplo para un usuario administrador"""
    return {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "AdminPassword123!",
        "is_active": True,
        "is_verified": True
    }


@pytest.fixture
def inactive_user_data() -> Dict[str, Any]:
    """Datos de ejemplo para un usuario inactivo"""
    return {
        "name": "Inactive User",
        "email": "inactive@example.com",
        "password": "InactivePassword123!",
        "is_active": False,
        "is_verified": True
    }


@pytest.fixture
def unverified_user_data() -> Dict[str, Any]:
    """Datos de ejemplo para un usuario no verificado"""
    return {
        "name": "Unverified User",
        "email": "unverified@example.com",
        "password": "UnverifiedPassword123!",
        "is_active": True,
        "is_verified": False
    }


@pytest.fixture
def multiple_users_data() -> list[Dict[str, Any]]:
    """Lista de datos de ejemplo para múltiples usuarios"""
    return [
        {
            "name": "User 1",
            "email": "user1@example.com",
            "password": "Password123!",
            "is_active": True,
            "is_verified": True
        },
        {
            "name": "User 2",
            "email": "user2@example.com",
            "password": "Password456!",
            "is_active": True,
            "is_verified": True
        },
        {
            "name": "User 3",
            "email": "user3@example.com",
            "password": "Password789!",
            "is_active": False,
            "is_verified": True
        }
    ]


@pytest.fixture
def user_update_data() -> Dict[str, Any]:
    """Datos de ejemplo para actualizar un usuario"""
    return {
        "name": "Updated User Name",
        "is_active": False
    }


@pytest.fixture
def user_search_filters() -> Dict[str, Any]:
    """Filtros de ejemplo para búsqueda de usuarios"""
    return {
        "is_active": True,
        "is_verified": True,
        "email_contains": "test"
    }


@pytest.fixture
def invalid_user_data() -> Dict[str, Any]:
    """Datos de ejemplo inválidos para un usuario"""
    return {
        "name": "",  # Nombre vacío
        "email": "invalid-email",  # Email inválido
        "password": "123"  # Contraseña muy corta
    } 