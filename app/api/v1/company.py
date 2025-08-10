"""
Rutas de empresas - CRUD y gestión de empresas
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import (
    get_db, 
    get_company_service, 
    get_current_active_user,
    require_company_read,
    require_company_create,
    require_company_update,
    require_company_delete
)
from app.schemas.company import (
    CompanyCreate, 
    CompanyRead, 
    CompanyUpdate, 
    CompanyList
)
from app.schemas.response import SuccessResponse
from app.models.user import AppUser

router = APIRouter()


@router.post("/", response_model=CompanyRead, summary="Crear empresa")
async def create_company(
    company_data: CompanyCreate,
    company_service = Depends(get_company_service),
    current_user: AppUser = Depends(get_current_active_user),
    _: bool = Depends(require_company_create)
):
    """
    Crear una nueva empresa
    
    - **name**: Nombre de la empresa
    
    Returns:
        Empresa creada
    """
    company = company_service.create_company(company_data)
    return company


@router.get("/", response_model=CompanyList, summary="Listar empresas")
async def get_companies(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Límite de registros"),
    search: Optional[str] = Query(None, description="Término de búsqueda"),
    company_service = Depends(get_company_service),
    _: bool = Depends(require_company_read)
):
    """
    Obtener lista de empresas con filtros
    
    - **skip**: Número de registros a saltar
    - **limit**: Límite de registros (máximo 100)
    - **search**: Término de búsqueda en nombre
    
    Returns:
        Lista paginada de empresas
    """
    companies = company_service.get_companies(skip=skip, limit=limit, search=search)
    
    # En una implementación real, aquí se calcularía el total
    total = len(companies)  # Placeholder
    
    return CompanyList(
        companies=companies,
        total=total,
        page=(skip // limit) + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{company_id}", response_model=CompanyRead, summary="Obtener empresa")
async def get_company(
    company_id: str,
    company_service = Depends(get_company_service),
    _: bool = Depends(require_company_read)
):
    """
    Obtener empresa por ID
    
    - **company_id**: ID de la empresa
    
    Returns:
        Información de la empresa
    """
    company = company_service.get_company_by_id(company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa no encontrada"
        )
    return company


@router.put("/{company_id}", response_model=CompanyRead, summary="Actualizar empresa")
async def update_company(
    company_id: str,
    company_data: CompanyUpdate,
    company_service = Depends(get_company_service),
    _: bool = Depends(require_company_update)
):
    """
    Actualizar empresa
    
    - **company_id**: ID de la empresa
    - **company_data**: Datos a actualizar
    
    Returns:
        Empresa actualizada
    """
    company = company_service.update_company(company_id, company_data)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa no encontrada"
        )
    return company


@router.delete("/{company_id}", response_model=SuccessResponse, summary="Eliminar empresa")
async def delete_company(
    company_id: str,
    company_service = Depends(get_company_service),
    _: bool = Depends(require_company_delete)
):
    """
    Eliminar empresa
    
    - **company_id**: ID de la empresa
    
    Returns:
        Confirmación de eliminación
    """
    success = company_service.delete_company(company_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa no encontrada"
        )
    return SuccessResponse(message="Empresa eliminada correctamente")


@router.post("/{company_id}/users/{user_id}", response_model=SuccessResponse, summary="Agregar usuario a empresa")
async def add_user_to_company(
    company_id: str,
    user_id: str,
    company_service = Depends(get_company_service),
    _: bool = Depends(require_company_update)
):
    """
    Agregar usuario a una empresa
    
    - **company_id**: ID de la empresa
    - **user_id**: ID del usuario
    
    Returns:
        Confirmación de asignación
    """
    try:
        company_service.add_user_to_company(company_id, user_id)
        return SuccessResponse(message="Usuario agregado a la empresa correctamente")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{company_id}/users/{user_id}", response_model=SuccessResponse, summary="Remover usuario de empresa")
async def remove_user_from_company(
    company_id: str,
    user_id: str,
    company_service = Depends(get_company_service),
    _: bool = Depends(require_company_update)
):
    """
    Remover usuario de una empresa
    
    - **company_id**: ID de la empresa
    - **user_id**: ID del usuario
    
    Returns:
        Confirmación de remoción
    """
    success = company_service.remove_user_from_company(company_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no pertenece a esta empresa"
        )
    return SuccessResponse(message="Usuario removido de la empresa correctamente")


@router.get("/{company_id}/users", summary="Obtener usuarios de empresa")
async def get_company_users(
    company_id: str,
    company_service = Depends(get_company_service),
    _: bool = Depends(require_company_read)
):
    """
    Obtener usuarios de una empresa
    
    - **company_id**: ID de la empresa
    
    Returns:
        Lista de usuarios de la empresa
    """
    users = company_service.get_company_users(company_id)
    return {"users": users}
