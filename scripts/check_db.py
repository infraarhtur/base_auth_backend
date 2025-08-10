#!/usr/bin/env python3
"""
Script para verificar el estado de la base de datos y reiniciar conexiones si es necesario
"""

import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, InternalError

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import get_settings

def check_database_connection():
    """Verificar la conexión a la base de datos"""
    settings = get_settings()
    
    try:
        # Crear engine temporal para verificar conexión
        engine = create_engine(
            settings.database.url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        
        # Probar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexión a la base de datos exitosa")
            
            # Verificar si hay transacciones activas
            result = conn.execute(text("SELECT count(*) FROM pg_stat_activity WHERE state = 'active'"))
            active_connections = result.scalar()
            print(f"📊 Conexiones activas: {active_connections}")
            
            # Verificar si hay transacciones abortadas
            result = conn.execute(text("""
                SELECT count(*) 
                FROM pg_stat_activity 
                WHERE state = 'idle in transaction (aborted)'
            """))
            aborted_transactions = result.scalar()
            print(f"⚠️  Transacciones abortadas: {aborted_transactions}")
            
            if aborted_transactions > 0:
                print("🔧 Limpiando transacciones abortadas...")
                conn.execute(text("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle in transaction (aborted)'"))
                print("✅ Transacciones abortadas limpiadas")
            
        engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
        return False

def reset_database_connections():
    """Reiniciar todas las conexiones de la base de datos"""
    settings = get_settings()
    
    try:
        # Crear engine temporal
        engine = create_engine(
            settings.database.url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        
        with engine.connect() as conn:
            # Terminar todas las conexiones excepto la actual
            conn.execute(text("""
                SELECT pg_terminate_backend(pid) 
                FROM pg_stat_activity 
                WHERE pid <> pg_backend_pid() 
                AND datname = current_database()
            """))
            print("✅ Todas las conexiones han sido terminadas")
            
        engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Error al reiniciar conexiones: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Verificando estado de la base de datos...")
    
    if check_database_connection():
        print("✅ La base de datos está funcionando correctamente")
    else:
        print("🔄 Intentando reiniciar conexiones...")
        if reset_database_connections():
            print("✅ Conexiones reiniciadas exitosamente")
            if check_database_connection():
                print("✅ La base de datos ahora está funcionando correctamente")
            else:
                print("❌ La base de datos sigue teniendo problemas")
        else:
            print("❌ No se pudieron reiniciar las conexiones") 