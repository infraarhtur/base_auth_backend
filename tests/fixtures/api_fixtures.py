"""
Fixtures específicas para tests de API
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

from app.main import app
from app.models.user import AppUser
from app.models.company import Company
from app.models.role import Role
from app.models.permission import Permission


@pytest.fixture
def api_client():
    """Cliente de prueba para la API"""
    return TestClient(app)


@pytest.fixture
def mock_auth_service():
    """Mock del servicio de autenticación"""
    mock_service = Mock()
    
    # Mock para login
    mock_service.login.return_value = {
        "access_token": "mock_access_token_123",
        "refresh_token": "mock_refresh_token_456",
        "token_type": "bearer"
    }
    
    # Mock para refresh token
    mock_service.refresh_token.return_value = {
        "access_token": "new_mock_access_token_789",
        "refresh_token": "mock_refresh_token_456",
        "token_type": "bearer"
    }
    
    # Mock para logout
    mock_service.logout.return_value = True
    
    # Mock para get_current_user_from_token
    mock_user = Mock(spec=AppUser)
    mock_user.id = "550e8400-e29b-41d4-a716-446655440000"
    mock_user.email = "test@example.com"
    mock_user.name = "Test User"
    mock_user.is_active = True
    mock_user.created_at = "2024-01-01T00:00:00"
    
    mock_service.get_current_user_from_token.return_value = mock_user
    
    # Mock para métodos adicionales
    mock_service.request_password_reset.return_value = True
    mock_service.confirm_password_reset.return_value = True
    mock_service.validate_password_reset_token.return_value = {
        "valid": True,
        "email": "test@example.com"
    }
    mock_service.request_email_verification.return_value = True
    mock_service.confirm_email_verification.return_value = True
    mock_service.encrypt_string.return_value = "encrypted_text_123"
    
    return mock_service


@pytest.fixture
def mock_user_service():
    """Mock del servicio de usuarios"""
    mock_service = Mock()
    
    # Mock para create_user
    mock_user = Mock(spec=AppUser)
    mock_user.id = "550e8400-e29b-41d4-a716-446655440000"
    mock_user.email = "newuser@example.com"
    mock_user.name = "New User"
    mock_user.is_active = True
    mock_user.created_at = "2024-01-01T00:00:00"
    
    mock_service.create_user.return_value = mock_user
    
    # Mock para get_users
    mock_users = [
        Mock(spec=AppUser, id="user1", email="user1@example.com", name="User 1"),
        Mock(spec=AppUser, id="user2", email="user2@example.com", name="User 2")
    ]
    mock_service.get_users.return_value = mock_users
    
    # Mock para get_user_by_id
    mock_service.get_user_by_id.return_value = mock_user
    
    # Mock para update_user
    mock_service.update_user.return_value = mock_user
    
    # Mock para delete_user
    mock_service.delete_user.return_value = True
    
    # Mock para get_user_companies
    mock_companies = [
        Mock(spec=Company, id="company1", name="Company 1"),
        Mock(spec=Company, id="company2", name="Company 2")
    ]
    mock_service.get_user_companies.return_value = mock_companies
    
    # Mock para change_password
    mock_service.change_password.return_value = True
    
    return mock_service


@pytest.fixture
def mock_company_service():
    """Mock del servicio de empresas"""
    mock_service = Mock()
    
    # Mock para create_company
    mock_company = Mock(spec=Company)
    mock_company.id = "550e8400-e29b-41d4-a716-446655440000"
    mock_company.name = "Test Company"
    mock_company.created_at = "2024-01-01T00:00:00"
    
    mock_service.create_company.return_value = mock_company
    
    # Mock para get_companies
    mock_companies = [
        Mock(spec=Company, id="company1", name="Company 1"),
        Mock(spec=Company, id="company2", name="Company 2")
    ]
    mock_service.get_companies.return_value = mock_companies
    
    # Mock para get_company_by_id
    mock_service.get_company_by_id.return_value = mock_company
    
    # Mock para update_company
    mock_service.update_company.return_value = mock_company
    
    # Mock para delete_company
    mock_service.delete_company.return_value = True
    
    # Mock para add_user_to_company
    mock_service.add_user_to_company.return_value = True
    
    # Mock para remove_user_from_company
    mock_service.remove_user_from_company.return_value = True
    
    # Mock para get_company_users
    mock_users = [
        Mock(spec=AppUser, id="user1", email="user1@example.com", name="User 1"),
        Mock(spec=AppUser, id="user2", email="user2@example.com", name="User 2")
    ]
    mock_service.get_company_users.return_value = mock_users
    
    return mock_service


@pytest.fixture
def mock_role_service():
    """Mock del servicio de roles"""
    mock_service = Mock()
    
    # Mock para create_role
    mock_role = Mock(spec=Role)
    mock_role.id = "550e8400-e29b-41d4-a716-446655440000"
    mock_role.name = "Test Role"
    mock_role.company_id = "550e8400-e29b-41d4-a716-446655440001"
    mock_role.created_at = "2024-01-01T00:00:00"
    
    mock_service.create_role.return_value = mock_role
    
    # Mock para get_roles
    mock_roles = [
        Mock(spec=Role, id="role1", name="Role 1"),
        Mock(spec=Role, id="role2", name="Role 2")
    ]
    mock_service.get_roles.return_value = mock_roles
    
    # Mock para get_role_by_id
    mock_service.get_role_by_id.return_value = mock_role
    
    # Mock para update_role
    mock_service.update_role.return_value = mock_role
    
    # Mock para delete_role
    mock_service.delete_role.return_value = True
    
    # Mock para assign_role_to_user
    mock_service.assign_role_to_user.return_value = True
    
    # Mock para remove_role_from_user
    mock_service.remove_role_from_user.return_value = True
    
    # Mock para get_user_roles
    mock_user_roles = [
        Mock(spec=Role, id="role1", name="Role 1"),
        Mock(spec=Role, id="role2", name="Role 2")
    ]
    mock_service.get_user_roles.return_value = mock_user_roles
    
    # Mock para get_permissions
    mock_permissions = [
        Mock(spec=Permission, id="perm1", name="read_users"),
        Mock(spec=Permission, id="perm2", name="write_users")
    ]
    mock_service.get_permissions.return_value = mock_permissions
    
    # Mock para get_role_permissions
    mock_service.get_role_permissions.return_value = mock_permissions
    
    return mock_service


@pytest.fixture
def mock_cleanup_service():
    """Mock del servicio de limpieza"""
    mock_service = Mock()
    
    # Mock para get_blacklist_stats
    mock_service.get_blacklist_stats.return_value = {
        "total_tokens": 100,
        "expired_tokens": 25,
        "active_tokens": 75
    }
    
    # Mock para cleanup_expired_tokens
    mock_service.cleanup_expired_tokens.return_value = 25
    
    # Mock para cleanup_old_tokens
    mock_service.cleanup_old_tokens.return_value = 10
    
    return mock_service


@pytest.fixture
def auth_headers():
    """Headers de autenticación para tests"""
    return {"Authorization": "Bearer mock_access_token_123"}


@pytest.fixture
def login_data():
    """Datos de prueba para login"""
    return {
        "email": "test@example.com",
        "hashed_password": "hashed_password_123",
        "company_name": "Test Company",
        "remember_me": False
    }


@pytest.fixture
def user_create_data():
    """Datos de prueba para crear usuario"""
    return {
        "name": "New User",
        "email": "newuser@example.com",
        "password": "TestPassword123!",
        "company_name": "Test Company",
        "rol": "user"
    }


@pytest.fixture
def company_create_data():
    """Datos de prueba para crear empresa"""
    return {
        "name": "Test Company"
    }


@pytest.fixture
def role_create_data():
    """Datos de prueba para crear rol"""
    return {
        "name": "Test Role",
        "company_id": "550e8400-e29b-41d4-a716-446655440001",
        "permissions": ["550e8400-e29b-41d4-a716-446655440002"]
    }


@pytest.fixture
def mock_permission_dependencies():
    """Mock de las dependencias de permisos"""
    def mock_require_permission(permission_name: str):
        def permission_dependency():
            return True
        return permission_dependency
    
    return mock_require_permission


# Fixtures para mocks globales de dependencias
@pytest.fixture(autouse=True)
def mock_dependencies():
    """Mock global de todas las dependencias de la API"""
    with patch('app.api.deps.get_auth_service') as mock_auth, \
         patch('app.api.deps.get_user_service') as mock_user, \
         patch('app.api.deps.get_company_service') as mock_company, \
         patch('app.api.deps.get_role_service') as mock_role, \
         patch('app.api.deps.require_user_create', return_value=True), \
         patch('app.api.deps.require_user_read', return_value=True), \
         patch('app.api.deps.require_user_update', return_value=True), \
         patch('app.api.deps.require_user_delete', return_value=True), \
         patch('app.api.deps.require_company_create', return_value=True), \
         patch('app.api.deps.require_company_read', return_value=True), \
         patch('app.api.deps.require_company_update', return_value=True), \
         patch('app.api.deps.require_company_delete', return_value=True), \
         patch('app.api.deps.require_role_create', return_value=True), \
         patch('app.api.deps.require_role_read', return_value=True), \
         patch('app.api.deps.require_role_update', return_value=True), \
         patch('app.api.deps.require_role_delete', return_value=True), \
         patch('app.api.deps.require_permission_read', return_value=True), \
         patch('app.api.deps.require_permission_assign', return_value=True):
        
        # Configurar mocks básicos
        mock_auth.return_value = Mock()
        mock_user.return_value = Mock()
        mock_company.return_value = Mock()
        mock_role.return_value = Mock()
        
        yield 