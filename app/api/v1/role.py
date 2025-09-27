"""
Rutas de roles y permisos - Gestión de roles y permisos
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import (
    get_db, 
    get_role_service, 
    get_current_active_user,
    require_role_read,
    require_role_create,
    require_role_update,
    require_role_delete,
    require_permission_read,
    require_permission_assign,
    get_current_company_id
)
from app.schemas.role import (
    RoleCreate, 
    RoleRead, 
    RoleUpdate, 
    RoleList,
    UserRoleCreate,
    UserRoleRead
)
from app.schemas.permission import PermissionRead, PermissionList
from app.schemas.response import SuccessResponse
from app.models.user import AppUser

router = APIRouter()


# ===== RUTAS DE ROLES =====

@router.post("/", response_model=RoleRead, summary="Crear rol")
async def create_role(
    role_data: RoleCreate,
    role_service = Depends(get_role_service),
    _: bool = Depends(require_role_create)
):
    """
    Crear un nuevo rol
    
    - **name**: Nombre del rol
    - **company_id**: ID de la empresa (opcional, para roles globales)
    - **permissions**: Lista de IDs de permisos (opcional)
    
    Returns:
        Rol creado
    """
    role = role_service.create_role(role_data)
    return role


@router.get("/", response_model=RoleList, summary="Listar roles")
async def get_roles(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros"),
   
    search: Optional[str] = Query(None, description="Término de búsqueda"),
    role_service = Depends(get_role_service),
    company_id: str = Depends(get_current_company_id),
    _: bool = Depends(require_role_read)
):
    """
    Obtener lista de roles con filtros
    
    - **skip**: Número de registros a saltar
    - **limit**: Límite de registros (máximo 100)    
    - **search**: Término de búsqueda en nombre
    
    Returns:
        Lista paginada de roles
    """
    roles = role_service.get_roles(
        skip=skip, 
        limit=limit, 
        company_id=company_id, 
        search=search
    )
    
    # En una implementación real, aquí se calcularía el total
    total = len(roles)  # Placeholder
    
    return RoleList(
        roles=roles,
        total=total,
        page=(skip // limit) + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{role_id}", response_model=RoleRead, summary="Obtener rol")
async def get_role(
    role_id: str,
    role_service = Depends(get_role_service),
    _: bool = Depends(require_role_read)
):
    """
    Obtener rol por ID
    
    - **role_id**: ID del rol
    
    Returns:
        Información del rol
    """
    role = role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return role


@router.put("/{role_id}", response_model=RoleRead, summary="Actualizar rol")
async def update_role(
    role_id: str,
    role_data: RoleUpdate,
    role_service = Depends(get_role_service),
    _: bool = Depends(require_role_update)
):
    """
    Actualizar rol
    
    - **role_id**: ID del rol
    - **role_data**: Datos a actualizar
    
    Returns:
        Rol actualizado
    """
    role = role_service.update_role(role_id, role_data)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return role


@router.delete("/{role_id}", response_model=SuccessResponse, summary="Eliminar rol")
async def delete_role(
    role_id: str,
    role_service = Depends(get_role_service),
    _: bool = Depends(require_role_delete)
):
    """
    Eliminar rol
    
    - **role_id**: ID del rol
    
    Returns:
        Confirmación de eliminación
    """
    success = role_service.delete_role(role_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return SuccessResponse(message="Rol eliminado correctamente")


@router.post("/assign", response_model=SuccessResponse, summary="Asignar rol a usuario")
async def assign_role_to_user(
    assignment_data: UserRoleCreate,
    role_service = Depends(get_role_service),
    _: bool = Depends(require_role_update)
):
    """
    Asignar rol a usuario
    
    - **user_id**: ID del usuario
    - **role_id**: ID del rol
    
    Returns:
        Confirmación de asignación
    """
    try:
        role_service.assign_role_to_user(assignment_data.user_id, assignment_data.role_id)
        return SuccessResponse(message="Rol asignado correctamente")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{role_id}/users/{user_id}", response_model=SuccessResponse, summary="Remover rol de usuario")
async def remove_role_from_user(
    role_id: str,
    user_id: str,
    role_service = Depends(get_role_service),
    _: bool = Depends(require_role_update)
):
    """
    Remover rol de usuario
    
    - **role_id**: ID del rol
    - **user_id**: ID del usuario
    
    Returns:
        Confirmación de remoción
    """
    success = role_service.remove_role_from_user(user_id, role_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no tiene asignado este rol"
        )
    return SuccessResponse(message="Rol removido correctamente")


@router.get("/users/{user_id}", summary="Obtener roles de usuario")
async def get_user_roles(
    user_id: str,
    role_service = Depends(get_role_service),
    _: bool = Depends(require_role_read)
):
    """
    Obtener roles de un usuario
    
    - **user_id**: ID del usuario
    
    Returns:
        Lista de roles del usuario
    """
    roles = role_service.get_user_roles(user_id)
    return {"roles": roles}


# ===== RUTAS DE PERMISOS =====

@router.get("/permissions/", response_model=PermissionList, summary="Listar permisos")
async def get_permissions(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros"),
    role_service = Depends(get_role_service),
    _: bool = Depends(require_permission_read)
):
    """
    Obtener lista de permisos
    
    - **skip**: Número de registros a saltar
    - **limit**: Límite de registros (máximo 100)
    
    Returns:
        Lista paginada de permisos
    """
    permissions = role_service.get_all_permissions()
    
    # En una implementación real, aquí se calcularía el total
    total = len(permissions)  # Placeholder
    
    return PermissionList(
        permissions=permissions,
        total=total,
        page=(skip // limit) + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{role_id}/permissions", summary="Obtener permisos de rol")
async def get_role_permissions(
    role_id: str,
    role_service = Depends(get_role_service),
    _: bool = Depends(require_permission_read)
):
    """
    Obtener permisos de un rol
    
    - **role_id**: ID del rol
    
    Returns:
        Lista de permisos del rol
    """
    permissions = role_service.get_role_permissions(role_id)
    return {"permissions": permissions} 