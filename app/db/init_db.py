"""
Script de inicialización de la base de datos
Crea las tablas y ejecuta los datos de prueba
"""

import logging
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.db.seeds import run_seeds

logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    Inicializa la base de datos:
    1. Crea todas las tablas
    2. Ejecuta los datos de prueba
    """
    try:
        # Crear todas las tablas
        logger.info("Creando tablas de la base de datos...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tablas creadas exitosamente")
        
        # Ejecutar datos de prueba
        logger.info("Ejecutando datos de prueba...")
        run_seeds()
        logger.info("✅ Datos de prueba ejecutados exitosamente")
        
    except SQLAlchemyError as e:
        logger.error(f"❌ Error al inicializar la base de datos: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        raise


def drop_db() -> None:
    """
    Elimina todas las tablas de la base de datos
    """
    try:
        logger.info("Eliminando todas las tablas...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ Tablas eliminadas exitosamente")
    except SQLAlchemyError as e:
        logger.error(f"❌ Error al eliminar las tablas: {e}")
        raise


def reset_db() -> None:
    """
    Resetea la base de datos: elimina y recrea todo
    """
    try:
        logger.info("Reseteando base de datos...")
        drop_db()
        init_db()
        logger.info("✅ Base de datos reseteada exitosamente")
    except Exception as e:
        logger.error(f"❌ Error al resetear la base de datos: {e}")
        raise


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "init":
            init_db()
        elif command == "drop":
            drop_db()
        elif command == "reset":
            reset_db()
        else:
            print("Comandos disponibles: init, drop, reset")
    else:
        print("Uso: python -m app.db.init_db [init|drop|reset]") 