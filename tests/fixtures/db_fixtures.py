"""
Fixtures específicas para base de datos de pruebas.
Contiene fixtures para manejo de transacciones, limpieza y configuración de BD.
"""

import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Generator, Dict, Any


@pytest.fixture
def db_transaction(db_session: Session) -> Generator[Session, None, None]:
    """
    Fixture que proporciona una transacción aislada para cada prueba.
    Los cambios se revierten automáticamente al final de la prueba.
    
    Args:
        db_session: Sesión de base de datos de conftest.py
        
    Yields:
        Sesión con transacción anidada
    """
    # Iniciar transacción anidada
    db_session.begin_nested()
    
    yield db_session
    
    # Rollback automático
    db_session.rollback()


@pytest.fixture
def isolated_db(db_session: Session) -> Generator[Session, None, None]:
    """
    Fixture que proporciona una base de datos completamente aislada.
    Útil para pruebas que necesitan un estado limpio y aislado.
    
    Args:
        db_session: Sesión de base de datos de conftest.py
        
    Yields:
        Sesión aislada
    """
    # Crear punto de guardado
    db_session.begin_nested()
    
    yield db_session
    
    # Revertir todos los cambios
    db_session.rollback()


@pytest.fixture
def db_with_data(db_session: Session) -> Generator[Session, None, None]:
    """
    Fixture que proporciona una base de datos con datos de prueba básicos.
    Los datos se crean al inicio y se limpian al final.
    
    Args:
        db_session: Sesión de base de datos de conftest.py
        
    Yields:
        Sesión con datos de prueba
    """
    # Aquí se crearían datos básicos de prueba
    # Por ahora solo retornamos la sesión limpia
    
    yield db_session
    
    # La limpieza se hace automáticamente por el rollback


@pytest.fixture
def db_connection_info(db_session: Session) -> Dict[str, Any]:
    """
    Fixture que proporciona información sobre la conexión de base de datos.
    
    Args:
        db_session: Sesión de base de datos de conftest.py
        
    Returns:
        Diccionario con información de la conexión
    """
    try:
        # Obtener información de la conexión
        result = db_session.execute(text("PRAGMA database_list"))
        databases = result.fetchall()
        
        # Obtener información de configuración SQLite
        pragma_results = {}
        pragmas = [
            "foreign_keys",
            "journal_mode", 
            "synchronous",
            "temp_store",
            "cache_size"
        ]
        
        for pragma in pragmas:
            try:
                result = db_session.execute(text(f"PRAGMA {pragma}"))
                pragma_results[pragma] = result.scalar()
            except:
                pragma_results[pragma] = "N/A"
        
        return {
            "databases": databases,
            "sqlite_pragmas": pragma_results,
            "session_info": {
                "autocommit": db_session.autocommit,
                "autoflush": db_session.autoflush,
                "expire_on_commit": db_session.expire_on_commit
            }
        }
    except Exception as e:
        return {
            "error": str(e),
            "databases": [],
            "sqlite_pragmas": {},
            "session_info": {}
        }


@pytest.fixture
def db_performance_monitor(db_session: Session) -> Generator[Dict[str, Any], None, None]:
    """
    Fixture para monitorear el rendimiento de la base de datos durante las pruebas.
    
    Args:
        db_session: Sesión de base de datos de conftest.py
        
    Yields:
        Diccionario con métricas de rendimiento
    """
    import time
    
    # Métricas de inicio
    start_time = time.time()
    start_memory = 0  # En un entorno real se mediría la memoria
    
    # Obtener estadísticas iniciales de SQLite
    try:
        result = db_session.execute(text("PRAGMA stats"))
        start_stats = result.fetchall()
    except:
        start_stats = []
    
    metrics = {
        "start_time": start_time,
        "start_stats": start_stats,
        "operations": [],
        "queries": []
    }
    
    yield metrics
    
    # Métricas de fin
    end_time = time.time()
    duration = end_time - start_time
    
    try:
        result = db_session.execute(text("PRAGMA stats"))
        end_stats = result.fetchall()
    except:
        end_stats = []
    
    metrics.update({
        "end_time": end_time,
        "duration": duration,
        "end_stats": end_stats,
        "total_operations": len(metrics["operations"]),
        "total_queries": len(metrics["queries"])
    })


@pytest.fixture
def db_constraint_checker(db_session: Session) -> Generator[Dict[str, Any], None, None]:
    """
    Fixture para verificar la integridad de las restricciones de la base de datos.
    
    Args:
        db_session: Sesión de base de datos de conftest.py
        
    Yields:
        Diccionario con información de restricciones
    """
    constraints = {}
    
    try:
        # Verificar foreign keys
        result = db_session.execute(text("PRAGMA foreign_key_check"))
        fk_check = result.fetchall()
        constraints["foreign_keys"] = {
            "enabled": True,
            "check_result": fk_check,
            "violations": len(fk_check)
        }
    except:
        constraints["foreign_keys"] = {
            "enabled": False,
            "check_result": [],
            "violations": 0
        }
    
    try:
        # Obtener información de índices
        result = db_session.execute(text("PRAGMA index_list"))
        indexes = result.fetchall()
        constraints["indexes"] = {
            "count": len(indexes),
            "list": indexes
        }
    except:
        constraints["indexes"] = {
            "count": 0,
            "list": []
        }
    
    try:
        # Obtener información de triggers
        result = db_session.execute(text("PRAGMA trigger_list"))
        triggers = result.fetchall()
        constraints["triggers"] = {
            "count": len(triggers),
            "list": triggers
        }
    except:
        constraints["triggers"] = {
            "count": 0,
            "list": []
        }
    
    yield constraints


@pytest.fixture
def db_backup_restore(db_session: Session) -> Generator[Dict[str, Any], None, None]:
    """
    Fixture para crear y restaurar backups de la base de datos durante las pruebas.
    Útil para pruebas que necesitan restaurar un estado específico.
    
    Args:
        db_session: Sesión de base de datos de conftest.py
        
    Yields:
        Diccionario con funciones de backup y restore
    """
    backup_data = {}
    
    def create_backup():
        """Crea un backup del estado actual de la base de datos"""
        try:
            # Obtener el estado actual de todas las tablas
            tables = []
            result = db_session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            
            for row in result.fetchall():
                table_name = row[0]
                if table_name != "sqlite_sequence":
                    # Obtener datos de la tabla
                    data_result = db_session.execute(text(f"SELECT * FROM {table_name}"))
                    table_data = data_result.fetchall()
                    tables.append({
                        "name": table_name,
                        "data": table_data,
                        "columns": [desc[0] for desc in data_result.description] if data_result.description else []
                    })
            
            backup_data["tables"] = tables
            backup_data["created_at"] = "now"  # En un entorno real sería timestamp
            
            return True
        except Exception as e:
            backup_data["error"] = str(e)
            return False
    
    def restore_backup():
        """Restaura el backup creado anteriormente"""
        if "tables" not in backup_data:
            return False
        
        try:
            # Limpiar todas las tablas
            for table_info in backup_data["tables"]:
                table_name = table_info["name"]
                db_session.execute(text(f"DELETE FROM {table_name}"))
            
            # Restaurar datos
            for table_info in backup_data["tables"]:
                table_name = table_info["name"]
                table_data = table_info["data"]
                
                if table_data:
                    # Construir INSERT statements
                    columns = table_info["columns"]
                    placeholders = ", ".join(["?" for _ in columns])
                    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                    
                    for row in table_data:
                        db_session.execute(text(insert_sql), row)
            
            db_session.commit()
            return True
        except Exception as e:
            backup_data["restore_error"] = str(e)
            db_session.rollback()
            return False
    
    backup_restore = {
        "create_backup": create_backup,
        "restore_backup": restore_backup,
        "backup_data": backup_data
    }
    
    yield backup_restore 