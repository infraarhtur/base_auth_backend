"""
Fixtures para datos de roles en pruebas
"""

import pytest
from typing import Dict, Any


@pytest.fixture
def sample_role_data() -> Dict[str, Any]:
    """Datos de ejemplo para un rol"""
    return {
        "name": "test_role",
        "description": "A test role for integration testing",
        "is_active": True
    }


@pytest.fixture
def sample_role() -> Dict[str, Any]:
    """Rol de ejemplo con ID"""
    return {
        "id": 1,
        "name": "test_role",
        "description": "A test role for integration testing",
        "is_active": True
    }


@pytest.fixture
def admin_role_data() -> Dict[str, Any]:
    """Datos de ejemplo para un rol de administrador"""
    return {
        "name": "admin",
        "description": "Administrator role with full permissions",
        "is_active": True
    }


@pytest.fixture
def user_role_data() -> Dict[str, Any]:
    """Datos de ejemplo para un rol de usuario básico"""
    return {
        "name": "user",
        "description": "Basic user role with limited permissions",
        "is_active": True
    }


@pytest.fixture
def manager_role_data() -> Dict[str, Any]:
    """Datos de ejemplo para un rol de manager"""
    return {
        "name": "manager",
        "description": "Manager role with moderate permissions",
        "is_active": True
    }


@pytest.fixture
def inactive_role_data() -> Dict[str, Any]:
    """Datos de ejemplo para un rol inactivo"""
    return {
        "name": "inactive_role",
        "description": "An inactive role for testing",
        "is_active": False
    }


@pytest.fixture
def multiple_roles_data() -> list[Dict[str, Any]]:
    """Lista de datos de ejemplo para múltiples roles"""
    return [
        {
            "name": "role_1",
            "description": "First role for testing",
            "is_active": True
        },
        {
            "name": "role_2",
            "description": "Second role for testing",
            "is_active": True
        },
        {
            "name": "role_3",
            "description": "Third role for testing",
            "is_active": False
        }
    ]


@pytest.fixture
def role_update_data() -> Dict[str, Any]:
    """Datos de ejemplo para actualizar un rol"""
    return {
        "name": "updated_role",
        "description": "Updated role description",
        "is_active": False
    }


@pytest.fixture
def role_search_filters() -> Dict[str, Any]:
    """Filtros de ejemplo para búsqueda de roles"""
    return {
        "is_active": True,
        "name_contains": "test"
    }


@pytest.fixture
def invalid_role_data() -> Dict[str, Any]:
    """Datos de ejemplo inválidos para un rol"""
    return {
        "name": "",  # Nombre vacío
        "description": "Role with empty name",
        "is_active": True
    }


@pytest.fixture
def long_name_role_data() -> Dict[str, Any]:
    """Datos de ejemplo para un rol con nombre muy largo"""
    return {
        "name": "A" * 100,  # Nombre muy largo
        "description": "Role with very long name",
        "is_active": True
    } 