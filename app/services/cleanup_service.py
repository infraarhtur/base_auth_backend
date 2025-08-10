"""
Servicio de limpieza - Limpieza automática de tokens expirados
"""

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.invalidated_token import InvalidatedToken


class CleanupService:
    """Servicio para operaciones de limpieza y mantenimiento"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def cleanup_expired_tokens(self) -> int:
        """
        Limpiar tokens expirados de la blacklist
        
        Returns:
            Número de tokens eliminados
        """
        try:
            current_time = datetime.now(timezone.utc)
            
            # Buscar y eliminar tokens expirados
            expired_tokens = (
                self.db.query(InvalidatedToken)
                .filter(InvalidatedToken.expires_at < current_time)
                .all()
            )
            
            count = len(expired_tokens)
            
            if count > 0:
                for token in expired_tokens:
                    self.db.delete(token)
                
                self.db.commit()
                print(f"🧹 Limpieza completada: {count} tokens expirados eliminados")
            else:
                print("🧹 No hay tokens expirados para limpiar")
            
            return count
            
        except Exception as e:
            self.db.rollback()
            print(f"❌ Error durante la limpieza: {e}")
            return 0
    
    def get_blacklist_stats(self) -> dict:
        """
        Obtener estadísticas de la blacklist
        
        Returns:
            Diccionario con estadísticas
        """
        try:
            current_time = datetime.now(timezone.utc)
            
            # Total de tokens en blacklist
            total_tokens = self.db.query(InvalidatedToken).count()
            
            # Tokens expirados
            expired_tokens = (
                self.db.query(InvalidatedToken)
                .filter(InvalidatedToken.expires_at < current_time)
                .count()
            )
            
            # Tokens activos (no expirados)
            active_tokens = total_tokens - expired_tokens
            
            # Tokens por tipo
            access_tokens = (
                self.db.query(InvalidatedToken)
                .filter(InvalidatedToken.token_type == "access")
                .count()
            )
            
            refresh_tokens = (
                self.db.query(InvalidatedToken)
                .filter(InvalidatedToken.token_type == "refresh")
                .count()
            )
            
            return {
                "total_tokens": total_tokens,
                "expired_tokens": expired_tokens,
                "active_tokens": active_tokens,
                "access_tokens": access_tokens,
                "refresh_tokens": refresh_tokens,
                "last_updated": current_time.isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}
    
    def cleanup_old_tokens(self, days_old: int = 30) -> int:
        """
        Limpiar tokens antiguos (más de X días)
        
        Args:
            days_old: Número de días para considerar un token como antiguo
            
        Returns:
            Número de tokens eliminados
        """
        try:
            from datetime import timedelta
            
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)
            
            # Buscar tokens más antiguos que la fecha límite
            old_tokens = (
                self.db.query(InvalidatedToken)
                .filter(InvalidatedToken.invalidated_at < cutoff_date)
                .all()
            )
            
            count = len(old_tokens)
            
            if count > 0:
                for token in old_tokens:
                    self.db.delete(token)
                
                self.db.commit()
                print(f"🧹 Limpieza de tokens antiguos completada: {count} tokens eliminados")
            else:
                print(f"🧹 No hay tokens más antiguos que {days_old} días")
            
            return count
            
        except Exception as e:
            self.db.rollback()
            print(f"❌ Error durante la limpieza de tokens antiguos: {e}")
            return 0 