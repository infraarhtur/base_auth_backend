"""
Modelo UserIdentity - Autenticación con terceros (Google, Facebook, etc.)
"""

from sqlalchemy import Column, String, ForeignKey, Boolean, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel


class UserIdentity(BaseModel):
    """
    Modelo para autenticación con terceros (OAuth).
    Permite que un usuario se autentique con Google, Facebook, etc.
    """
    
    __tablename__ = "user_identity"
    
    # Clave foránea
    user_id = Column(UUID(as_uuid=True), ForeignKey("app_user.id", ondelete="CASCADE"), nullable=False)
    
    # Información del proveedor
    provider = Column(Text, nullable=False)  # google, facebook, github, etc.
    provider_user_id = Column(Text, nullable=False)
    
    # Información del usuario en el proveedor
    email = Column(Text, nullable=True)
    name = Column(Text, nullable=True)
    
    # Relaciones
    user = relationship("AppUser", back_populates="identities")
    
    # Índices
    __table_args__ = (
        Index("ix_user_identity_user_id", "user_id"),
        Index("ix_user_identity_provider", "provider"),
        Index("ix_user_identity_provider_user_id", "provider_user_id"),
    )
    
    def __repr__(self) -> str:
        return f"<UserIdentity(user_id={self.user_id}, provider='{self.provider}')>" 