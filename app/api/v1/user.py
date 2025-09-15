"""
Rutas de usuarios - CRUD y gestión de usuarios
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_user,
    get_db, 
    get_user_service, 
    get_current_active_user,
    get_current_company_id,
    require_user_read,
    require_user_create,
    require_user_update,
    require_user_delete
)
from app.schemas.user import (
    UserCreate, 
    UserRead, 
    UserUpdate, 
    UserList,
    UserPasswordChange,
    UserWithRoles
)
from app.schemas.response import SuccessResponse
from app.models.user import AppUser

router = APIRouter()


@router.post("/", response_model=UserRead, summary="Crear usuario")
async def create_user(
    user_data: UserCreate,
    user_service = Depends(get_user_service),
    _: bool = Depends(require_user_create)
):
    """
    Crear un nuevo usuario
    
    - **name**: Nombre del usuario
    - **email**: Email del usuario
    - **password**: Contraseña del usuario
    - **company_id**: Id de la compañía
    - **role**: Rol del usuario en la compañía
    
    Returns:
        Usuario creado
    """
    user = user_service.create_user(user_data)
    return user


@router.get("/", response_model=UserList, summary="Listar usuarios")
async def get_users(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros"),
    search: Optional[str] = Query(None, description="Término de búsqueda"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    user_service = Depends(get_user_service),
    _: bool = Depends(require_user_read)
):
    """
    Obtener lista de usuarios con filtros
    
    - **skip**: Número de registros a saltar
    - **limit**: Límite de registros (máximo 100)
    - **search**: Término de búsqueda en email, nombre
    - **is_active**: Filtrar por estado activo
    
    Returns:
        Lista paginada de usuarios
    """
    users = user_service.get_users(skip=skip, limit=limit, search=search, is_active=is_active)
    
    # En una implementación real, aquí se calcularía el total
    total = len(users)  # Placeholder
    
    return UserList(
        users=users,
        total=total,
        page=(skip // limit) + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/me/companies", summary="Obtener empresas del usuario actual")
async def get_my_companies(
    current_user: AppUser = Depends(get_current_active_user),
    user_service = Depends(get_user_service)
):
    """
    Obtener empresas del usuario autenticado
    
    Returns:
        Lista de empresas del usuario
    """
    companies = user_service.get_user_companies(str(current_user.id))
    return {"companies": companies}


@router.get("/{user_id}/companies", summary="Obtener empresas de un usuario")
async def get_user_companies(
    user_id: str,
    user_service = Depends(get_user_service),
    _: bool = Depends(require_user_read)
):
    """
    Obtener empresas de un usuario específico
    
    - **user_id**: ID del usuario
    
    Returns:
        Lista de empresas del usuario
    """
    companies = user_service.get_user_companies(user_id)
    return {"companies": companies}


@router.get("/{user_id}/{company_name}", response_model=UserWithRoles, summary="Obtener usuario")
async def get_user(
    user_id: str,
    company_name: str,
    user_service = Depends(get_user_service),
    _: bool = Depends(require_user_read)
):
    """
    Obtener usuario por ID con sus roles en una compañía específica
    
    - **user_id**: ID del usuario
    - **company_name**: Nombre de la compañía
    
    Returns:
        Usuario encontrado con sus roles en la compañía
    """
    user_data = user_service.get_user_by_id_with_company_roles(user_id, company_name)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado o no pertenece a la compañía especificada"
        )
    return user_data


@router.put("/{user_id}", response_model=UserRead, summary="Actualizar usuario")
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    user_service = Depends(get_user_service),
    company_id: str = Depends(get_current_company_id),
    _: bool = Depends(require_user_update)
):
    """
    Actualizar usuario
    
    - **user_id**: ID del usuario
    - **user_data**: Datos a actualizar
    
    Returns:
        Usuario actualizado
    """

    print(f"user_data: {user_data}")
    print(f"user_service: {user_service}")
    print(f"company_id: {company_id}")
    user = user_service.update_user(user_id, user_data,company_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user


@router.delete("/{user_id}/{company_name}", response_model=SuccessResponse, summary="Eliminar usuario")
async def delete_user(
    user_id: str,
    company_name: str,
    user_service = Depends(get_user_service),
    _: bool = Depends(require_user_delete)
):
    """
    Eliminar usuario (soft delete)
    
    - **user_id**: ID del usuario
    - **company_name**: Nombre de la compañía
    
    Returns:
        Confirmación de eliminación
    """
    success = user_service.delete_user(user_id, company_name)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return SuccessResponse(message="Usuario eliminado correctamente")


@router.post("/{user_id}/change-password", response_model=SuccessResponse, summary="Cambiar contraseña")
async def change_password(
    user_id: str,
    password_data: UserPasswordChange,
    user_service = Depends(get_user_service),
    current_user: AppUser = Depends(get_current_active_user)
):
    """
    Cambiar contraseña de usuario
    
    - **user_id**: ID del usuario
    - **password_data**: Datos de cambio de contraseña
    
    Returns:
        Confirmación de cambio de contraseña
    """
    # Verificar que el usuario puede cambiar su propia contraseña
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes cambiar tu propia contraseña"
        )
    
    # Verificar que las contraseñas coinciden
    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas no coinciden"
        )
    
    success = user_service.change_password(
        user_id, 
        password_data.current_password, 
        password_data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )
    
    return SuccessResponse(message="Contraseña cambiada correctamente")