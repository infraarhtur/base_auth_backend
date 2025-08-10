"""
Base declarativa SQLAlchemy para todos los modelos
"""

from app.models.base import Base

# Importar todos los modelos para que Alembic los detecte
from app.models.user import AppUser
from app.models.company import Company
from app.models.company_user import CompanyUser
from app.models.role import Role
from app.models.permission import Permission
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission
from app.models.user_identity import UserIdentity 