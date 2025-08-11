"""
Fixtures para datos de empresas en pruebas
"""

import pytest
from typing import Dict, Any


@pytest.fixture
def sample_company_data() -> Dict[str, Any]:
    """Datos de ejemplo para una empresa"""
    return {
        "name": "Test Company Inc.",
        "description": "A test company for integration testing",
        "is_active": True
    }


@pytest.fixture
def sample_company() -> Dict[str, Any]:
    """Empresa de ejemplo con ID"""
    return {
        "id": 1,
        "name": "Test Company Inc.",
        "description": "A test company for integration testing",
        "is_active": True
    }


@pytest.fixture
def active_company_data() -> Dict[str, Any]:
    """Datos de ejemplo para una empresa activa"""
    return {
        "name": "Active Company Ltd.",
        "description": "An active company for testing",
        "is_active": True
    }


@pytest.fixture
def inactive_company_data() -> Dict[str, Any]:
    """Datos de ejemplo para una empresa inactiva"""
    return {
        "name": "Inactive Company Corp.",
        "description": "An inactive company for testing",
        "is_active": False
    }


@pytest.fixture
def multiple_companies_data() -> list[Dict[str, Any]]:
    """Lista de datos de ejemplo para múltiples empresas"""
    return [
        {
            "name": "Company A",
            "description": "First company for testing",
            "is_active": True
        },
        {
            "name": "Company B",
            "description": "Second company for testing",
            "is_active": True
        },
        {
            "name": "Company C",
            "description": "Third company for testing",
            "is_active": False
        }
    ]


@pytest.fixture
def company_update_data() -> Dict[str, Any]:
    """Datos de ejemplo para actualizar una empresa"""
    return {
        "name": "Updated Company Name",
        "description": "Updated company description",
        "is_active": False
    }


@pytest.fixture
def company_search_filters() -> Dict[str, Any]:
    """Filtros de ejemplo para búsqueda de empresas"""
    return {
        "is_active": True,
        "name_contains": "Test"
    }


@pytest.fixture
def invalid_company_data() -> Dict[str, Any]:
    """Datos de ejemplo inválidos para una empresa"""
    return {
        "name": "",  # Nombre vacío
        "description": "Company with empty name",
        "is_active": True
    }


@pytest.fixture
def large_company_data() -> Dict[str, Any]:
    """Datos de ejemplo para una empresa con descripción larga"""
    return {
        "name": "Large Description Company",
        "description": "A" * 1000,  # Descripción muy larga
        "is_active": True
    } 