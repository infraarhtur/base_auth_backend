"""
Modelo UserRole - Asignación de roles a usuarios
"""

from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class UserRole(Base):
    """
    Modelo para la asignación de roles a usuarios.
    Un usuario puede tener múltiples roles en diferentes empresas.
    """
    
    __tablename__ = "user_role"
    
    # Claves foráneas
    user_id = Column(UUID(as_uuid=True), ForeignKey("app_user.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("role.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    
    # Relaciones
    user = relationship("AppUser", back_populates="roles")
    role = relationship("Role", back_populates="users")
    
    # Índices
    __table_args__ = (
        Index("ix_user_role_user_id", "user_id"),
        Index("ix_user_role_role_id", "role_id"),
    )
    
    def __repr__(self) -> str:
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>" 