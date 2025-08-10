"""
Modelo Role - Roles definidos por empresa
"""

from sqlalchemy import Column, String, Text, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .base import Base


class RoleBase(Base):
    """
    Clase base para Role sin created_at.
    """
    
    __abstract__ = True
    
    # Campos comunes sin created_at
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    def __repr__(self) -> str:
        """Representación string del modelo"""
        return f"<{self.__class__.__name__}(id={self.id})>"


class Role(RoleBase):
    """
    Modelo para representar roles definidos por empresa.
    Los roles pueden ser globales (company_id=None) o específicos de una empresa.
    """
    
    __tablename__ = "role"
    
    # Campos básicos
    name = Column(Text, nullable=False)
    
    # Relación con empresa (None para roles globales)
    company_id = Column(UUID(as_uuid=True), ForeignKey("company.id", ondelete="CASCADE"), nullable=True)
    
    # Relaciones
    company = relationship("Company", back_populates="roles")
    users = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")
    permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")
    
    # Índices
    __table_args__ = (
        Index("ix_role_name", "name"),
        Index("ix_role_company_id", "company_id"),
    )
    
    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name='{self.name}', company_id={self.company_id})>" 

