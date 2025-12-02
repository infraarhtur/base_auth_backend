"""
Modelo AppUser - Usuario del sistema
"""

from sqlalchemy import Column, String, Boolean, Text, Index
from sqlalchemy.orm import relationship

from .base import BaseModel


class AppUser(BaseModel):
    """
    Modelo para representar usuarios del sistema.
    Los usuarios están desacoplados de las empresas y pueden pertenecer a múltiples.
    """
    
    __tablename__ = "app_user"
    
    # Información personal
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    
    # Autenticación
    hashed_password = Column(Text, nullable=False)
    
    # Estado
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relaciones
    companies = relationship("CompanyUser", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    identities = relationship("UserIdentity", back_populates="user", cascade="all, delete-orphan")
    
    # Índices
    __table_args__ = (
        Index("ix_app_user_email", "email"),
    )
    
    def __repr__(self) -> str:
        return f"<AppUser(id={self.id}, email='{self.email}', name='{self.name}')>" 