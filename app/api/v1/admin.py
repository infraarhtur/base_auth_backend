"""
Endpoints de administración del sistema
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.api.deps import get_db, get_current_user
from app.models.user import AppUser
from app.services.cleanup_service import CleanupService

router = APIRouter()


@router.get("/blacklist/stats", summary="Estadísticas de la blacklist")
async def get_blacklist_stats(
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Obtener estadísticas de la blacklist de tokens
    
    Returns:
        Estadísticas de la blacklist
    """
    try:
        cleanup_service = CleanupService(db)
        stats = cleanup_service.get_blacklist_stats()
        
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudieron obtener estadísticas"
            )
        
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo estadísticas: {str(e)}"
        )


@router.post("/blacklist/cleanup/expired", summary="Limpiar tokens expirados")
async def cleanup_expired_tokens(
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Limpiar tokens expirados de la blacklist
    
    Returns:
        Resultado de la limpieza
    """
    try:
        cleanup_service = CleanupService(db)
        count = cleanup_service.cleanup_expired_tokens()
        
        return {
            "message": "Limpieza completada",
            "tokens_eliminados": count,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante la limpieza: {str(e)}"
        )


@router.post("/blacklist/cleanup/old", summary="Limpiar tokens antiguos")
async def cleanup_old_tokens(
    days: int = 30,
    current_user: AppUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Limpiar tokens más antiguos que X días
    
    Args:
        days: Número de días para considerar un token como antiguo
        
    Returns:
        Resultado de la limpieza
    """
    try:
        if days < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El número de días debe ser mayor a 0"
            )
        
        cleanup_service = CleanupService(db)
        count = cleanup_service.cleanup_old_tokens(days)
        
        return {
            "message": "Limpieza completada",
            "tokens_eliminados": count,
            "dias_limite": days,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante la limpieza: {str(e)}"
        ) 