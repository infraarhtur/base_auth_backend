"""
Servicio de roles - Gestión de roles y permisos
"""

from typing import Optional, List, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.models.role import Role
from app.models.permission import Permission
from app.models.user_role import UserRole
from app.models.role_permission import RolePermission
from app.schemas.role import RoleCreate, RoleUpdate, RoleRead
from app.models.user import AppUser


class RoleWithPermissions:
    """Clase auxiliar para roles con permisos cargados"""
    def __init__(self, role: Role, permissions: List[Permission]):
        self.id = role.id  # Mantener como UUID
        self.name = role.name
        self.company_id = role.company_id  # Mantener como UUID
        # Usar los objetos de permisos directamente sin conversión
        self.permissions = permissions


class RoleService:
    """Servicio para operaciones con roles y permisos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_role(self, role_data: RoleCreate) -> Union[Role, RoleWithPermissions]:
        """
        Crear un nuevo rol
        
        Args:
            role_data: Datos del rol a crear
            
        Returns:
            Rol creado
            
        Raises:
            HTTPException: Si el nombre ya existe
        """
        role_data.name = role_data.name.lower()
        # Verificar si el nombre ya existe en la misma empresa
        existing_role = (
            self.db.query(Role)
            .filter(Role.name == role_data.name, Role.company_id == role_data.company_id)
            .first()
        )
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de rol ya existe en esta empresa"
            )
        
        # Crear rol
        role = Role(
            name=role_data.name,
            company_id=role_data.company_id
        )
        
        self.db.add(role)
        self.db.flush()  # Para obtener el ID
        
        # Asignar permisos si se proporcionan
        if role_data.permissions:
            for permission_id in role_data.permissions:
                role_permission = RolePermission(
                    role_id=role.id,
                    permission_id=permission_id
                )
                self.db.add(role_permission)
        
        self.db.commit()
        self.db.refresh(role)
        
        # Cargar los permisos reales para la respuesta
        permissions_query = (
            self.db.query(Permission)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .filter(RolePermission.role_id == role.id)
            .all()
        )
        
        # Crear un objeto de respuesta que incluya los permisos
        # Usar la clase auxiliar para evitar problemas con SQLAlchemy
        return RoleWithPermissions(role, permissions_query)
    
    def get_role_by_id(self, role_id: str) -> Optional[RoleWithPermissions]:
        """
        Obtener rol por ID con permisos cargados
        
        Args:
            role_id: ID del rol
            
        Returns:
            Rol con permisos si existe, None si no
        """
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return None
            
        # Cargar permisos del rol
        permissions_query = (
            self.db.query(Permission)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .filter(RolePermission.role_id == role.id)
            .all()
        )
        
        return RoleWithPermissions(role, permissions_query)
    
    def get_roles(
        self, 
        skip: int = 0, 
        limit: int = 100,
        company_id: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[RoleWithPermissions]:
        """
        Obtener lista de roles con filtros
        
        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros
            company_id: Filtrar por empresa
            search: Término de búsqueda
            
        Returns:
            Lista de roles con permisos cargados
        """
        query = self.db.query(Role)
        
        # Aplicar filtros
        if company_id is not None:
            query = query.filter(Role.company_id == company_id)
        
        if search:
            query = query.filter(Role.name.ilike(f"%{search}%"))
        
        roles = query.offset(skip).limit(limit).all()
        
        # Para cada rol, cargar sus permisos
        result = []
        for role in roles:
            permissions = (
                self.db.query(Permission)
                .join(RolePermission, Permission.id == RolePermission.permission_id)
                .filter(RolePermission.role_id == role.id)
                .all()
            )
            result.append(RoleWithPermissions(role, permissions))
        
        return result
    
    def update_role(self, role_id: str, role_data: RoleUpdate) -> Optional[RoleWithPermissions]:
        """
        Actualizar rol
        
        Args:
            role_id: ID del rol
            role_data: Datos a actualizar
            
        Returns:
            Rol actualizado si existe, None si no
            
        Raises:
            HTTPException: Si el nombre ya existe
        """
        # Obtener el rol directamente de la base de datos como instancia de SQLAlchemy
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            return None
        
        # Verificar si el nombre ya existe (si se está cambiando)
        if role_data.name and role_data.name != role.name:
            existing_role = (
                self.db.query(Role)
                .filter(Role.name == role_data.name, Role.company_id == role.company_id)
                .first()
            )
            if existing_role:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de rol ya existe en esta empresa"
                )
        
        # Actualizar campos
        update_data = role_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field != "permissions":  # Los permisos se manejan por separado
                setattr(role, field, value)
        
        # Actualizar permisos si se proporcionan
        if role_data.permissions is not None:
            # Eliminar permisos existentes
            self.db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
            
            # Agregar nuevos permisos
            for permission_id in role_data.permissions:
                role_permission = RolePermission(
                    role_id=role_id,
                    permission_id=permission_id
                )
                self.db.add(role_permission)
        
        self.db.commit()
        self.db.refresh(role)
        
        # Cargar permisos del rol actualizado
        permissions = (
            self.db.query(Permission)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .filter(RolePermission.role_id == role.id)
            .all()
        )
        
        return RoleWithPermissions(role, permissions)
    
    def delete_role(self, role_id: str) -> bool:
        """
        Eliminar rol en cascada con todas sus relaciones
        
        Args:
            role_id: ID del rol
            
        Returns:
            True si se eliminó, False si no existe
        """
        try:
            # Obtener el rol directamente de la base de datos como instancia de SQLAlchemy
            role = self.db.query(Role).filter(Role.id == role_id).first()
            if not role:
                return False
            
            # SQLAlchemy debería eliminar automáticamente las relaciones debido a cascade="all, delete-orphan"
            # y ondelete="CASCADE" en las claves foráneas
            self.db.delete(role)
            self.db.commit()
            
            return True
            
        except Exception as e:
            # Si hay algún error, hacer rollback
            self.db.rollback()
            # Log del error para debugging
            print(f"Error eliminando rol {role_id}: {str(e)}")
            return False
    
    def assign_role_to_user(self, user_id: str, role_id: str) -> UserRole:
        """
        Asignar rol a usuario
        
        Args:
            user_id: ID del usuario
            role_id: ID del rol
            
        Returns:
            Asignación de rol creada
            
        Raises:
            HTTPException: Si el usuario o rol no existen, o si ya están relacionados
        """
        # Verificar que el usuario existe
        user = self.db.query(AppUser).filter(AppUser.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar que el rol existe
        role = self.get_role_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        
        # Verificar si ya existe la asignación
        existing_assignment = (
            self.db.query(UserRole)
            .filter(UserRole.user_id == user_id, UserRole.role_id == role_id)
            .first()
        )
        
        if existing_assignment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya tiene asignado este rol"
            )
        
        # Crear asignación
        user_role = UserRole(
            user_id=user_id,
            role_id=role_id
        )
        
        self.db.add(user_role)
        self.db.commit()
        self.db.refresh(user_role)
        
        return user_role
    
    def remove_role_from_user(self, user_id: str, role_id: str) -> bool:
        """
        Remover rol de usuario
        
        Args:
            user_id: ID del usuario
            role_id: ID del rol
            
        Returns:
            True si se removió, False si no existe la asignación
        """
        # Buscar asignación
        user_role = (
            self.db.query(UserRole)
            .filter(UserRole.user_id == user_id, UserRole.role_id == role_id)
            .first()
        )
        
        if not user_role:
            return False
        
        self.db.delete(user_role)
        self.db.commit()
        
        return True
    
    def get_user_roles(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Obtener roles de un usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de roles del usuario
        """
        roles = (
            self.db.query(UserRole)
            .filter(UserRole.user_id == user_id)
            .all()
        )
        
        from datetime import datetime
        
        return [
            {
                "role_id": ur.role_id,
                "role_name": ur.role.name,
                "company_id": ur.role.company_id,
                "assigned_at": datetime.utcnow()  # Usar timestamp actual ya que no hay created_at en UserRole
            }
            for ur in roles
        ]
    
    def get_role_permissions(self, role_id: str) -> List[Permission]:
        """
        Obtener permisos de un rol
        
        Args:
            role_id: ID del rol
            
        Returns:
            Lista de permisos del rol
        """
        permissions = (
            self.db.query(Permission)
            .join(RolePermission)
            .filter(RolePermission.role_id == role_id)
            .all()
        )
        
        return permissions
    
    def get_all_permissions(self) -> List[Permission]:
        """
        Obtener todos los permisos
        
        Returns:
            Lista de todos los permisos
        """
        return self.db.query(Permission).all() 