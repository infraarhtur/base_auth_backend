"""
Modelo CompanyUser - Relación muchos-a-muchos entre usuarios y empresas
"""

from sqlalchemy import Column, ForeignKey, Index, Table, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .base import Base


class CompanyUser(Base):
    """
    Modelo para la relación muchos-a-muchos entre usuarios y empresas.
    Permite que un usuario pertenezca a múltiples empresas con diferentes roles.
    """
    
    __tablename__ = "company_user"
    
    # Claves foráneas
    user_id = Column(UUID(as_uuid=True), ForeignKey("app_user.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("company.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    
    # Campos adicionales
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relaciones
    user = relationship("AppUser", back_populates="companies")
    company = relationship("Company", back_populates="users")
    
    # Índices
    __table_args__ = (
        Index("ix_company_user_user_id", "user_id"),
        Index("ix_company_user_company_id", "company_id"),
    )
    
    def __repr__(self) -> str:
        return f"<CompanyUser(user_id={self.user_id}, company_id={self.company_id})>" 