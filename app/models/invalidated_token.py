"""
Modelo para tokens invalidados (blacklist)
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.models.base import Base


class InvalidatedToken(Base):
    """Modelo para almacenar tokens invalidados"""
    
    __tablename__ = "invalidated_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    token_hash = Column(String(255), nullable=False, index=True, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("app_user.id"), nullable=False, index=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("company.id"), nullable=False, index=True)
    invalidated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    token_type = Column(String(20), nullable=False, default="access")  # "access" o "refresh"
    
    def __repr__(self):
        return f"<InvalidatedToken(id={self.id}, user_id={self.user_id}, expires_at={self.expires_at})>" 