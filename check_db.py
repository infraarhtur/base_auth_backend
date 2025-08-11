#!/usr/bin/env python3
"""Script para verificar el contenido de la base de datos"""

from sqlalchemy import create_engine, text
from app.core.config import settings

def check_database():
    """Verificar el contenido de la base de datos"""
    try:
        print("Conectando a la base de datos...")
        engine = create_engine(settings.database.url)
        
        with engine.connect() as conn:
            # Verificar usuarios
            result = conn.execute(text("SELECT COUNT(*) FROM app_user"))
            user_count = result.fetchone()[0]
            print(f"Usuarios en la base de datos: {user_count}")
            
            # Verificar empresas
            result = conn.execute(text("SELECT COUNT(*) FROM company"))
            company_count = result.fetchone()[0]
            print(f"Empresas en la base de datos: {company_count}")
            
            # Listar algunos usuarios
            if user_count > 0:
                print("\nPrimeros 5 usuarios:")
                result = conn.execute(text("SELECT id, name, email, is_active FROM app_user LIMIT 5"))
                for row in result:
                    print(f"  - {row[1]} ({row[2]}) - Activo: {row[3]}")
            
            # Listar algunas empresas
            if company_count > 0:
                print("\nPrimeras 5 empresas:")
                result = conn.execute(text("SELECT id, name, is_active FROM company LIMIT 5"))
                for row in result:
                    print(f"  - {row[1]} - Activo: {row[2]}")
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_database() 