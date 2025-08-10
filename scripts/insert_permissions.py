#!/usr/bin/env python3
"""
Script para insertar permisos en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission


def insert_permissions():
    """Insertar permisos básicos del sistema"""
    
    db = SessionLocal()
    try:
        # Lista de permisos a insertar
        permissions_data = [
            # Usuarios
            {"name": "user:read"},
            {"name": "user:create"},
            {"name": "user:update"},
            {"name": "user:delete"},
            
            # Empresas
            {"name": "company:read"},
            {"name": "company:create"},
            {"name": "company:update"},
            {"name": "company:delete"},
            
            # Roles
            {"name": "role:read"},
            {"name": "role:create"},
            {"name": "role:update"},
            {"name": "role:delete"},
            
            # Permisos
            {"name": "permission:read"},
            {"name": "permission:assign"},
            
            # Sistema
            {"name": "system:admin"},
            
            # Permisos adicionales que puedas necesitar
            {"name": "dashboard:read"},
            {"name": "reports:read"},
            {"name": "settings:read"},
            {"name": "settings:update"},
        ]
        
        # Insertar permisos
        inserted_permissions = []
        for perm_data in permissions_data:
            # Verificar si el permiso ya existe
            existing = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
            if existing:
                print(f"⚠️  Permiso '{perm_data['name']}' ya existe")
                inserted_permissions.append(existing)
            else:
                permission = Permission(**perm_data)
                db.add(permission)
                db.flush()  # Para obtener el ID
                inserted_permissions.append(permission)
                print(f"✅ Permiso '{perm_data['name']}' insertado")
        
        db.commit()
        print(f"\n🎉 Se insertaron {len(inserted_permissions)} permisos correctamente")
        
        # Mostrar todos los permisos
        print("\n📋 Lista de permisos en la base de datos:")
        all_permissions = db.query(Permission).all()
        for perm in all_permissions:
            print(f"  - {perm.name}")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Error al insertar permisos: {e}")
        raise
    finally:
        db.close()


def assign_permissions_to_role(role_name: str, permission_names: list):
    """Asignar permisos a un rol específico"""
    
    db = SessionLocal()
    try:
        # Buscar el rol
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            print(f"❌ Rol '{role_name}' no encontrado")
            return
        
        # Buscar los permisos
        permissions = db.query(Permission).filter(Permission.name.in_(permission_names)).all()
        if not permissions:
            print(f"❌ No se encontraron permisos: {permission_names}")
            return
        
        # Asignar permisos al rol
        for permission in permissions:
            # Verificar si ya existe la asignación
            existing = db.query(RolePermission).filter(
                RolePermission.role_id == role.id,
                RolePermission.permission_id == permission.id
            ).first()
            
            if existing:
                print(f"⚠️  Permiso '{permission.name}' ya está asignado al rol '{role_name}'")
            else:
                role_permission = RolePermission(
                    role_id=role.id,
                    permission_id=permission.id
                )
                db.add(role_permission)
                print(f"✅ Permiso '{permission.name}' asignado al rol '{role_name}'")
        
        db.commit()
        print(f"\n🎉 Permisos asignados correctamente al rol '{role_name}'")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al asignar permisos: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Iniciando inserción de permisos...")
    
    # Insertar permisos básicos
    insert_permissions()
    
    # Ejemplo: Asignar permisos a un rol específico
    # assign_permissions_to_role("Company Admin", ["user:read", "user:create", "company:read"])
    
    print("\n✨ Proceso completado!") 