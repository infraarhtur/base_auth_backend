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
    EmailVerificationConfirm,
    PasswordResetValidationResponse,
    EncryptStringRequest,
    EncryptStringResponse
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
    - **password**: Contraseña del usuario en texto plano
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
        "company_id": str(current_user.companies[0].company_id),
        "company_name": current_user.companies[0].company.name,
        "roles": [user_role.role.name for user_role in current_user.roles],
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
    try:
        success = auth_service.request_password_reset(reset_data.email)
        
        if success:
            return SuccessResponse(
                message="Si el email existe, se enviará un enlace de reset",
                data={"email": reset_data.email}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error procesando la solicitud de reset"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
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
    try:
        success, error_message = auth_service.confirm_password_reset(
            confirm_data.token, 
            confirm_data.new_password
        )
        
        if success:
            return SuccessResponse(
                message="Contraseña cambiada correctamente",
                data={"success": True}
            )
        else:
            # Manejar diferentes tipos de errores con mensajes específicos
            if "Token inválido" in error_message or "expirado" in error_message:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_message
                )
            elif "Usuario no encontrado" in error_message:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_message
                )
            elif "debe tener al menos" in error_message or "debe contener" in error_message:
                # Errores de validación de contraseña
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=error_message
                )
            else:
                # Otros errores
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_message
                )
    except HTTPException:
        # Re-lanzar HTTPException sin modificar
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )


@router.get("/password-reset/validate", summary="Validar token de reset de contraseña")
async def validate_password_reset_token(
    token: str,
    auth_service = Depends(get_auth_service)
):
    """
    Validar token de reset de contraseña antes de mostrar formulario
    
    - **token**: Token de reset a validar
    
    Returns:
        Información del usuario si el token es válido
    """
    try:
        validation_result = auth_service.validate_password_reset_token(token)
        
        if validation_result:
            user_info, expires_at = validation_result
            return PasswordResetValidationResponse(
                valid=True,
                user=user_info,
                expires_at=expires_at,
                message="Token válido"
            )
        else:
            # Devolver respuesta estructurada para token inválido
            return PasswordResetValidationResponse(
                valid=False,
                user=None,
                expires_at=None,
                message="Token inválido o expirado"
            )
    except Exception as e:
        # Solo errores internos del servidor
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
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
    try:
        success = auth_service.request_email_verification(verification_data.email)
        
        if success:
            return SuccessResponse(
                message="Si el email existe, se enviará un enlace de verificación",
                data={"email": verification_data.email}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error procesando la solicitud de verificación"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
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
    try:
        success = auth_service.confirm_email_verification(confirm_data.token)
        
        if success:
            return SuccessResponse(
                message="Email verificado correctamente",
                data={"success": True}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido o expirado"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )


@router.post("/encrypt", response_model=EncryptStringResponse, summary="Encriptar string")
async def encrypt_string(
    encrypt_data: EncryptStringRequest,
    auth_service = Depends(get_auth_service)
):
    """
    Encriptar un string usando el mismo algoritmo que las contraseñas
    
    - **plain_string**: String en texto plano a encriptar
    
    Returns:
        String encriptado que puede usarse como contraseña
    """
    try:
        encrypted_string = auth_service.encrypt_string(encrypt_data.plain_string)
        
        return EncryptStringResponse(
            encrypted_string=encrypted_string,
            message="String encriptado correctamente"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )
