"""
Rutas de autenticación - Login, logout, refresh token
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_auth_service, get_current_user
from app.schemas.auth import (
    LoginRequest, 
    Token, 
    RefreshRequest, 
    LogoutRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    EmailVerificationRequest,
    EmailVerificationConfirm
)
from app.schemas.response import SuccessResponse
from app.models.user import AppUser

router = APIRouter()


@router.post("/login", response_model=Token, summary="Iniciar sesión")
async def login(
    login_data: LoginRequest,
    auth_service = Depends(get_auth_service)
):
    """
    Autenticar usuario y generar tokens JWT
    
    - **email**: Email del usuario
    - **hashed_password**: Hash de la contraseña del usuario
    - **company_name**: Nombre de la empresa
    - **remember_me**: Recordar sesión (opcional)
    
    Returns:
        Token con access_token y refresh_token
    """
    return auth_service.login(login_data)


@router.post("/refresh", response_model=Token, summary="Refrescar token")
async def refresh_token(
    refresh_data: RefreshRequest,
    auth_service = Depends(get_auth_service)
):
    """
    Refrescar token de acceso usando refresh token
    
    - **refresh_token**: Token de refresco
    
    Returns:
        Nuevo token de acceso
    """
    return auth_service.refresh_token(refresh_data.refresh_token)


@router.post("/logout", response_model=SuccessResponse, summary="Cerrar sesión")
async def logout(
    logout_data: LogoutRequest,
    auth_service = Depends(get_auth_service)
):
    """
    Cerrar sesión
    
    - **refresh_token**: Token de refresco a invalidar
    - **access_token**: Token de acceso a invalidar (opcional)
    
    Returns:
        Confirmación de logout
    """
    success = auth_service.logout(logout_data.refresh_token, logout_data.access_token)
    
    return SuccessResponse(
        message="Sesión cerrada correctamente",
        data={"success": success}
    )


@router.get("/me", summary="Obtener usuario actual")
async def get_current_user_info(
    current_user: AppUser = Depends(get_current_user)
):
    """
    Obtener información del usuario actual
    
    Returns:
        Información del usuario autenticado
    """
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at
    }


@router.post("/password-reset", response_model=SuccessResponse, summary="Solicitar reset de contraseña")
async def request_password_reset(
    reset_data: PasswordResetRequest,
    auth_service = Depends(get_auth_service)
):
    """
    Solicitar reset de contraseña
    
    - **email**: Email del usuario
    
    Returns:
        Confirmación de solicitud
    """
    # En una implementación real, aquí se enviaría un email
    # Por ahora, solo simulamos el proceso
    return SuccessResponse(
        message="Si el email existe, se enviará un enlace de reset",
        data={"email": reset_data.email}
    )


@router.post("/password-reset/confirm", response_model=SuccessResponse, summary="Confirmar reset de contraseña")
async def confirm_password_reset(
    confirm_data: PasswordResetConfirm,
    auth_service = Depends(get_auth_service)
):
    """
    Confirmar reset de contraseña
    
    - **token**: Token de reset
    - **new_password**: Nueva contraseña
    
    Returns:
        Confirmación de cambio de contraseña
    """
    # En una implementación real, aquí se validaría el token
    # y se cambiaría la contraseña
    return SuccessResponse(
        message="Contraseña cambiada correctamente",
        data={"success": True}
    )


@router.post("/email-verification", response_model=SuccessResponse, summary="Solicitar verificación de email")
async def request_email_verification(
    verification_data: EmailVerificationRequest,
    auth_service = Depends(get_auth_service)
):
    """
    Solicitar verificación de email
    
    - **email**: Email del usuario
    
    Returns:
        Confirmación de solicitud
    """
    # En una implementación real, aquí se enviaría un email
    # Por ahora, solo simulamos el proceso
    return SuccessResponse(
        message="Si el email existe, se enviará un enlace de verificación",
        data={"email": verification_data.email}
    )


@router.post("/email-verification/confirm", response_model=SuccessResponse, summary="Confirmar verificación de email")
async def confirm_email_verification(
    confirm_data: EmailVerificationConfirm,
    auth_service = Depends(get_auth_service)
):
    """
    Confirmar verificación de email
    
    - **token**: Token de verificación
    
    Returns:
        Confirmación de verificación
    """
    # En una implementación real, aquí se validaría el token
    # y se marcaría el email como verificado
    return SuccessResponse(
        message="Email verificado correctamente",
        data={"success": True}
    )
