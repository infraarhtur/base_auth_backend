"""
Modelo Permission - Permisos globales del sistema
"""

from sqlalchemy import Column, String, Text, Boolean, Index
from sqlalchemy.orm import relationship

from .base import BaseModel


class Permission(BaseModel):
    """
    Modelo para representar permisos globales del sistema.
    Los permisos son independientes de las empresas y se asignan a roles.
    """
    
    __tablename__ = "permission"
    
    # Campos básicos
    name = Column(Text, nullable=False, unique=True)
    is_super_admin = Column(Boolean, nullable=False, default=False)
    
    # Override created_at to exclude it
    created_at = None
    
    # Relaciones
    roles = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")
    
    # Índices
    __table_args__ = (
        Index("ix_permission_name", "name"),
    )
    
    def __repr__(self) -> str:
        return f"<Permission(id={self.id}, name='{self.name}', is_super_admin={self.is_super_admin})>" 