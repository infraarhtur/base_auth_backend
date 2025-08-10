"""
Datos de semilla para inicializar la base de datos
"""

import logging
from sqlalchemy.orm import Session
from app.services.security_service import SecurityService
from app.models.user import AppUser
from app.models.company import Company
from app.models.permission import Permission
from app.models.role import Role
from app.models.company_user import CompanyUser
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


def run_seeds() -> None:
    """
    Ejecuta todos los datos de semilla
    """
    db = SessionLocal()
    try:
        create_initial_data(db)
        logger.info("✅ Datos de semilla ejecutados correctamente")
    except Exception as e:
        logger.error(f"❌ Error al ejecutar datos de semilla: {e}")
        raise
    finally:
        db.close()


def create_initial_data(db: Session) -> None:
    """
    Crear datos iniciales de la aplicación.
    
    Args:
        db: Sesión de base de datos
    """
    # Crear permisos básicos
    permissions = create_basic_permissions(db)
    
    # Crear roles básicos
    roles = create_basic_roles(db)
    
    # Asignar permisos a roles
    assign_permissions_to_roles(db, roles, permissions)
    
    # Crear usuario administrador del sistema
    create_system_admin(db)
    
    logger.info("🌱 Datos de semilla creados correctamente")


def create_basic_permissions(db: Session) -> dict:
    """Crear permisos básicos del sistema"""
    
    permissions_data = [
        # Usuarios
        {"name": "user:read"},
        {"name": "user:create"},
        {"name": "user:update"},
        {"name": "user:delete"},
        
        # Empresas
        {"name": "company:read"},
        {"name": "company:create"},
        {"name": "company:update"},
        {"name": "company:delete"},
        
        # Roles
        {"name": "role:read"},
        {"name": "role:create"},
        {"name": "role:update"},
        {"name": "role:delete"},
        
        # Permisos
        {"name": "permission:read"},
        {"name": "permission:assign"},
        
        # Sistema
        {"name": "system:admin"},
    ]
    
    permissions = {}
    for perm_data in permissions_data:
        permission = Permission(**perm_data)
        db.add(permission)
        db.flush()  # Para obtener el ID
        permissions[perm_data["name"]] = permission
    
    db.commit()
    return permissions


def create_basic_roles(db: Session) -> dict:
    """Crear roles básicos del sistema"""
    
    roles_data = [
        {"name": "System Admin", "company_id": None},
        {"name": "Company Admin", "company_id": None},
        {"name": "User", "company_id": None},
    ]
    
    roles = {}
    for role_data in roles_data:
        role = Role(**role_data)
        db.add(role)
        db.flush()  # Para obtener el ID
        roles[role_data["name"]] = role
    
    db.commit()
    return roles


def assign_permissions_to_roles(db: Session, roles: dict, permissions: dict) -> None:
    """Asignar permisos a roles"""
    
    # System Admin - todos los permisos
    system_admin_role = roles["System Admin"]
    for permission in permissions.values():
        role_permission = RolePermission(
            role_id=system_admin_role.id,
            permission_id=permission.id
        )
        db.add(role_permission)
    
    # Company Admin - permisos de empresa
    company_admin_role = roles["Company Admin"]
    company_admin_permissions = [
        "user:read", "user:create", "user:update",
        "company:read", "company:update",
        "role:read", "role:create", "role:update",
        "permission:read", "permission:assign"
    ]
    
    for perm_name in company_admin_permissions:
        if perm_name in permissions:
            role_permission = RolePermission(
                role_id=company_admin_role.id,
                permission_id=permissions[perm_name].id
            )
            db.add(role_permission)
    
    # User - permisos básicos
    user_role = roles["User"]
    user_permissions = ["user:read"]
    
    for perm_name in user_permissions:
        if perm_name in permissions:
            role_permission = RolePermission(
                role_id=user_role.id,
                permission_id=permissions[perm_name].id
            )
            db.add(role_permission)
    
    db.commit()


def create_system_admin(db: Session) -> None:
    """Crear usuario administrador del sistema"""
    
    # Verificar si ya existe el admin
    admin_user = db.query(AppUser).filter(AppUser.email == "admin@system.com").first()
    if admin_user:
        return
    
    # Crear usuario admin
    admin_user = AppUser(
        email="admin@system.com",
        name="System Administrator",
        hashed_password=SecurityService.get_password_hash("admin123"),
        is_active=True
    )
    
    db.add(admin_user)
    db.flush()  # Para obtener el ID
    
    # Asignar rol de System Admin
    system_admin_role = db.query(Role).filter(Role.name == "System Admin").first()
    if system_admin_role:
        user_role = UserRole(
            user_id=admin_user.id,
            role_id=system_admin_role.id
        )
        db.add(user_role)
    
    db.commit()
    print("👤 Usuario administrador creado: admin@system.com / admin123") 