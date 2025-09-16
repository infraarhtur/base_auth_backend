"""
Servicio de usuarios - CRUD y lógica de negocio
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status

from app.models.user import AppUser
from app.models.company_user import CompanyUser
from app.models.user_role import UserRole
from app.models.role import Role
from app.models.company import Company
from app.schemas.user import UserCreate, UserUpdate, UserRead, UserWithRoles
from app.services.security_service import SecurityService
from sqlalchemy.dialects import postgresql


class UserService:
    """Servicio para operaciones con usuarios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> AppUser:
        """
        Crear un nuevo usuario
        
        Args:
            user_data: Datos del usuario a crear
            
        Returns:
            Usuario creado
            
        Raises:
            HTTPException: Si el email ya existe, la compañía no existe, o el rol no existe
        """
        user_data.name = user_data.name.lower()
        user_data.company_id= user_data.company_id.lower()
        user_data.email = user_data.email.lower()
        user_data.role = user_data.role.lower()
        # Buscar la compañía por nombre
        company = self.db.query(Company).filter(Company.id == user_data.company_id).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La compañía especificada no existe"
            )
        
        # Verificar si el email ya existe en la misma empresa
        existing_user_in_company = (
            self.db.query(AppUser)
            .join(CompanyUser, AppUser.id == CompanyUser.user_id)
            .filter(
                and_(
                    AppUser.email == user_data.email,
                    CompanyUser.company_id == company.id
                )
            )
            .first()
        )
        if existing_user_in_company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado en esta empresa"
            )
        
        # Buscar el rol por nombre en la compañía
        role = (
            self.db.query(Role)
            .filter(
                and_(
                    Role.name == user_data.role,
                    Role.company_id == company.id
                )
            )
            .first()
        )
        if not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El rol especificado no existe en la compañía"
            )
        
        # Crear hash de la contraseña
        hashed_password = SecurityService.get_password_hash(user_data.password)
        
        # Crear usuario
        user = AppUser(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password
        )
        
        self.db.add(user)
        self.db.flush()  # Para obtener el ID del usuario
        
        # Crear relación usuario-compañía
        company_user = CompanyUser(
            user_id=user.id,
            company_id=company.id
        )
        self.db.add(company_user)
        
        # Crear relación usuario-rol
        user_role = UserRole(
            user_id=user.id,
            role_id=role.id
        )
        self.db.add(user_role)
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[AppUser]:
        """
        Obtener usuario por ID
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Usuario si existe, None si no
        """
        return self.db.query(AppUser).filter(AppUser.id == user_id).first()
    
    def get_user_by_id_with_company_roles(self, user_id: str, company_name: str) -> Optional[Dict[str, Any]]:
        """
        Obtener usuario por ID con sus roles en una compañía específica
        
        Args:
            user_id: ID del usuario
            company_name: Nombre de la compañía
            
        Returns:
            Diccionario con información del usuario y sus roles en la compañía, None si no existe
        """
        # Buscar la compañía por nombre
        company = self.db.query(Company).filter(Company.name == company_name).first()
        if not company:
            return None
        
        # Buscar el usuario
        user = self.db.query(AppUser).filter(AppUser.id == user_id).first()
        if not user:
            return None
        
        # Verificar que el usuario pertenece a la compañía
        company_user = (
            self.db.query(CompanyUser)
            .filter(
                and_(
                    CompanyUser.user_id == user_id,
                    CompanyUser.company_id == company.id
                )
            )
            .first()
        )
        
        if not company_user:
            return None
        
        # Obtener los roles del usuario en esta compañía
        user_roles = (
            self.db.query(UserRole)
            .join(Role, UserRole.role_id == Role.id)
            .filter(
                and_(
                    UserRole.user_id == user_id,
                    Role.company_id == company.id
                )
            )
            .all()
        )
        
        # Extraer los nombres de los roles
        role_names = [user_role.role.name for user_role in user_roles]
        
        return {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "company_name": company.name,
            "roles": role_names
        }
    
    def get_user_by_email(self, email: str) -> Optional[AppUser]:
        """
        Obtener usuario por email
        
        Args:
            email: Email del usuario
            
        Returns:
            Usuario si existe, None si no
        """
        return self.db.query(AppUser).filter(AppUser.email == email).first()
    
    def get_users(
        self, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[AppUser]:
        """
        Obtener lista de usuarios con filtros
        
        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros
            search: Término de búsqueda
            is_active: Filtrar por estado activo
            
        Returns:
            Lista de usuarios
        """
        query = self.db.query(AppUser)
        
        # Aplicar filtros
        if search:
            query = query.filter(
                or_(
                    AppUser.name.ilike(f"%{search}%"),
                    AppUser.email.ilike(f"%{search}%")
                )
            )
        
        if is_active is not None:
            query = query.filter(AppUser.is_active == is_active)
        
        #print(query.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        
        return query.offset(skip).limit(limit).all()
    
    def update_user(self, user_id: str, user_data: UserUpdate,company_id: str) -> Optional[AppUser]:
        """
        Actualizar usuario
        
        Args:
            user_id: ID del usuario
            user_data: Datos a actualizar
            company_id: ID de la compañía
            
        Returns:
            Usuario actualizado si existe, None si no
            
        Raises:
            HTTPException: Si el email ya existe
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Verificar que el usuario pertenece a la compañía
        company_user = self.db.query(CompanyUser).filter(
            CompanyUser.user_id == user_id,
            CompanyUser.company_id == company_id
        ).first()
        if not company_user:
            return None
        
        # Actualizar campos del usuario (excluyendo el rol)
        update_data = user_data.dict(exclude_unset=True, exclude={'role'})
        for field, value in update_data.items():
            setattr(user, field, value)
        
        # Actualizar el rol del usuario en la compañía si se proporciona
        if user_data.role is not None:
            # Verificar que el rol existe en la compañía
            role = self.db.query(Role).filter(
                Role.name == user_data.role,
                Role.company_id == company_id
            ).first()
            if not role:
                return None
            
            # Verificar si el usuario ya tiene este rol en esta compañía
            current_user_role = self.db.query(UserRole).join(Role).filter(
                UserRole.user_id == user_id,
                Role.company_id == company_id
            ).first()
            
            # Si el usuario ya tiene un rol diferente, eliminarlo
            if current_user_role and current_user_role.role_id != role.id:
                self.db.delete(current_user_role)
                # Crear la nueva relación usuario-rol
                new_user_role = UserRole(
                    user_id=user_id,
                    role_id=role.id
                )
                self.db.add(new_user_role)
            # Si el usuario no tiene ningún rol, asignar el nuevo
            elif not current_user_role:
                new_user_role = UserRole(
                    user_id=user_id,
                    role_id=role.id
                )
                self.db.add(new_user_role)
            # Si el usuario ya tiene este mismo rol, no hacer nada
        
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def delete_user(self, user_id: str, company_id: str) -> bool:
        """
        Eliminar usuario de una compañía específica (soft delete)
        
        Args:
            user_id: ID del usuario
            
            company_id: ID de la compañía
        Returns:
            True si se eliminó, False si no existe la relación
        """
        # Obtener la compañía por nombre
        company = self.db.query(Company).filter(Company.id == company_id).first()
        if not company:
            return False
        
        # Buscar la relación usuario-compañía
        company_user = self.db.query(CompanyUser).filter(
            CompanyUser.user_id == user_id,
            CompanyUser.company_id == company.id
        ).first()
        
        if not company_user:
            return False
        
        # Soft delete: actualizar is_active a False
        company_user.is_active = False
        self.db.commit()
        
        return True
    
    def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """
        Cambiar contraseña de usuario
        
        Args:
            user_id: ID del usuario
            current_password: Contraseña actual
            new_password: Nueva contraseña
            
        Returns:
            True si se cambió, False si la contraseña actual es incorrecta
            
        Raises:
            HTTPException: Si el usuario no existe
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar contraseña actual
        if not SecurityService.verify_password(current_password, user.hashed_password):
            return False
        
        # Cambiar contraseña
        user.hashed_password = SecurityService.get_password_hash(new_password)
        self.db.commit()
        
        return True
    
    def get_user_companies(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Obtener empresas del usuario
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de empresas del usuario
        """
        companies = (
            self.db.query(CompanyUser)
            .filter(CompanyUser.user_id == user_id)
            .all()
        )
        
        return [
            {
                "company_id": str(cu.company_id),
                "company_name": cu.company.name,
                "is_active": cu.is_active
            }
            for cu in companies
        ] 