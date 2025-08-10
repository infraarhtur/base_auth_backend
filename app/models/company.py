"""
Modelo Company - Empresa o tenant del sistema
"""

from sqlalchemy import Column, String, Text, Boolean, Index
from sqlalchemy.orm import relationship

from .base import BaseModel


class Company(BaseModel):
    """
    Modelo para representar empresas o tenants del sistema.
    Cada empresa puede tener múltiples usuarios y roles.
    """
    
    __tablename__ = "company"
    
    # Campos básicos
    name = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relaciones
    users = relationship("CompanyUser", back_populates="company", cascade="all, delete-orphan")
    roles = relationship("Role", back_populates="company", cascade="all, delete-orphan")
    
    # Índices
    __table_args__ = (
        Index("ix_company_name", "name"),
    )
    
    def __repr__(self) -> str:
        return f"<Company(id={self.id}, name='{self.name}')>" 