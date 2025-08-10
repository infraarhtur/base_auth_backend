"""
Modelo RolePermission - Asignación de permisos a roles
"""

from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class RolePermission(Base):
    """
    Modelo para la asignación de permisos a roles.
    Un rol puede tener múltiples permisos.
    """
    
    __tablename__ = "role_permission"
    
    # Claves foráneas
    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey("permission.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    
    # Relaciones
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")
    
    # Índices
    __table_args__ = (
        Index("ix_role_permission_role_id", "role_id"),
        Index("ix_role_permission_permission_id", "permission_id"),
    )
    
    def __repr__(self) -> str:
        return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>" 