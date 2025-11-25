"""
Servicio de empresas - CRUD y lógica de negocio
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, text
from fastapi import HTTPException, status

from app.models.company import Company
from app.models.company_user import CompanyUser
from app.models.user import AppUser
from app.models.user_role import UserRole
from app.models.role import Role
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyRead


class CompanyService:
    """Servicio para operaciones con empresas"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_company(self, company_data: CompanyCreate) -> Company:
        """
        Crear una nueva empresa
        
        Args:
            company_data: Datos de la empresa a crear
            admin_user_id: ID del usuario administrador
            
        Returns:
            Empresa creada
            
        Raises:
            HTTPException: Si el nombre ya existe
        """
        company_data.name = company_data.name.lower()        
        # Verificar si el nombre ya existe
        existing_company = self.db.query(Company).filter(Company.name == company_data.name).first()
        if existing_company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de empresa ya está registrado"
            )
        
        # Crear empresa
        company = Company(
            name=company_data.name
        )
        
        self.db.add(company)
        self.db.flush()  # Para obtener el ID
        self.db.commit()  # Confirmar la transacción
        self.db.refresh(company)
        
        return company
    
    def get_company_by_id(self, company_id: str) -> Optional[Company]:
        """
        Obtener empresa por ID
        
        Args:
            company_id: ID de la empresa
            
        Returns:
            Empresa si existe, None si no
        """
        return self.db.query(Company).filter(Company.id == company_id).first()
    
    def get_companies(
        self, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Company]:
        """
        Obtener lista de empresas con filtros
        
        Args:
            skip: Número de registros a saltar
            limit: Número máximo de registros
            search: Término de búsqueda
            
        Returns:
            Lista de empresas
        """
        query = self.db.query(Company)
        
        # Aplicar filtros
        if search:
            query = query.filter(Company.name.ilike(f"%{search}%"))
        
        return query.offset(skip).limit(limit).all()
    
    def update_company(self, company_id: str, company_data: CompanyUpdate) -> Optional[Company]:
        """
        Actualizar empresa
        
        Args:
            company_id: ID de la empresa
            company_data: Datos a actualizar
            
        Returns:
            Empresa actualizada si existe, None si no
            
        Raises:
            HTTPException: Si el nombre ya existe
        """
        company = self.get_company_by_id(company_id)
        if not company:
            return None
        
        # Verificar si el nombre ya existe (si se está cambiando)
        if company_data.name and company_data.name != company.name:
            existing_company = self.db.query(Company).filter(Company.name == company_data.name).first()
            if existing_company:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de empresa ya está registrado"
                )
        
        # Actualizar campos
        update_data = company_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(company, field, value)
        
        self.db.commit()
        self.db.refresh(company)
        
        return company
    
    def delete_company(self, company_id: str) -> bool:
        """
        Eliminar empresa (soft delete)
        
        Args:
            company_id: ID de la empresa
            
        Returns:
            True si se desactivó, False si no existe
        """
        company = self.get_company_by_id(company_id)
        if not company:
            return False
        
        company.is_active = False
        self.db.commit()
        
        return True
    
    def add_user_to_company(self, company_id: str, user_id: str) -> CompanyUser:
        """
        Agregar usuario a una empresa
        
        Args:
            company_id: ID de la empresa
            user_id: ID del usuario
            
        Returns:
            Relación usuario-empresa creada
            
        Raises:
            HTTPException: Si la empresa o usuario no existen, o si ya están relacionados
        """
        # Verificar que la empresa existe
        company = self.get_company_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa no encontrada"
            )
        
        # Verificar que el usuario existe
        user = self.db.query(AppUser).filter(AppUser.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Verificar si ya existe la relación
        existing_relation = (
            self.db.query(CompanyUser)
            .filter(CompanyUser.company_id == company_id, CompanyUser.user_id == user_id)
            .first()
        )
        
        if existing_relation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya pertenece a esta empresa"
            )
        
        # Crear relación
        company_user = CompanyUser(
            company_id=company_id,
            user_id=user_id
        )
        
        self.db.add(company_user)
        self.db.commit()
        self.db.refresh(company_user)
        
        return company_user
    
    def remove_user_from_company(self, company_id: str, user_id: str) -> bool:
        """
        Remover usuario de una empresa
        
        Args:
            company_id: ID de la empresa
            user_id: ID del usuario
            
        Returns:
            True si se removió, False si no existe la relación
        """
        # Buscar relación
        company_user = (
            self.db.query(CompanyUser)
            .filter(CompanyUser.company_id == company_id, CompanyUser.user_id == user_id)
            .first()
        )
        
        if not company_user:
            return False
        
        # Marcar como inactivo en lugar de eliminar
        company_user.is_active = False
        self.db.commit()
        
        return True
    
    def get_company_users(self, company_id: str) -> List[Dict[str, Any]]:
        """
        Obtener usuarios de una empresa con sus roles
        
        Args:
            company_id: ID de la empresa
            
        Returns:
            Lista de usuarios de la empresa con sus roles
        """
        # Consulta con joins para obtener usuarios y sus roles en la empresa
        users_with_roles = (
            self.db.query(CompanyUser, AppUser, UserRole, Role)
            .filter(CompanyUser.company_id == company_id)
            #.filter(CompanyUser.is_active == True)
            .join(AppUser, CompanyUser.user_id == AppUser.id)
            .outerjoin(UserRole, UserRole.user_id == AppUser.id)
            .outerjoin(Role, 
                      (Role.id == UserRole.role_id) & 
                      (Role.company_id == company_id))
            .all()
        )
        
        # Agrupar por usuario para manejar múltiples roles
        users_dict = {}
        for cu, user, user_role, role in users_with_roles:
            user_id = str(cu.user_id)
            
            if user_id not in users_dict:
                users_dict[user_id] = {
                    "user_id": cu.user_id,
                    "user_name": user.name,
                    "user_email": user.email,
                    "joined_at": cu.created_at,
                    "is_active": cu.is_active,
                    "is_verified": cu.is_verified,
                    "roles": []
                }
            
            # Agregar rol si existe
            if role and role.name:
                users_dict[user_id]["roles"].append(role.name)
        
        # Convertir a lista y eliminar duplicados en roles
        result = []
        for user_data in users_dict.values():
            user_data["roles"] = list(set(user_data["roles"]))  # Eliminar duplicados
            result.append(user_data)
        
        return result
    
    def create_company_with_user(self, company_name: str, user_name: str, user_email: str) -> Dict[str, Any]:
        """
        Crear una empresa con un usuario usando la función SQL almacenada
        
        Esta función crea:
        - Una nueva empresa
        - Un nuevo usuario
        - Relaciona el usuario con la empresa
        - Crea un rol admin para la empresa
        - Asigna todos los permisos al rol admin
        - Asigna el rol admin al usuario
        
        Args:
            company_name: Nombre de la empresa
            user_name: Nombre del usuario
            user_email: Email del usuario
            
        Returns:
            Diccionario con los IDs creados:
            {
                "company_id": UUID,
                "user_id": UUID,
                "admin_role_id": UUID
            }
            
        Raises:
            HTTPException: Si el email o nombre de empresa ya existen
        """
        try:
            # Llamar a la función SQL almacenada
            result = self.db.execute(
                text("SELECT * FROM create_company_with_user(:company_name, :user_name, :user_email)"),
                {
                    "company_name": company_name.lower(),
                    "user_name": user_name,
                    "user_email": user_email.lower()
                }
            )
            
            # Obtener el resultado (la función retorna una fila)
            row = result.fetchone()
            
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error al crear la empresa y usuario"
                )
            
            # Confirmar la transacción
            self.db.commit()
            
            # Retornar los IDs creados
            # La función retorna: out_company_id, out_user_id, out_admin_role_id
            return {
                "company_id": str(row[0]),  # out_company_id
                "user_id": str(row[1]),     # out_user_id
                "admin_role_id": str(row[2])  # out_admin_role_id
            }
            
        except Exception as e:
            # Hacer rollback en caso de error
            self.db.rollback()
            
            # Si es una excepción de PostgreSQL (email o nombre duplicado)
            error_message = str(e)
            if "ya está registrado" in error_message or "ya existe" in error_message:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_message
                )
            
            # Para otros errores, lanzar excepción genérica
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear empresa con usuario: {error_message}"
            )

