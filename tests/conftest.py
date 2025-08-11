"""
Configuración principal de pytest para el proyecto base_auth_backend.
Este archivo contiene todas las fixtures y configuración compartida entre pruebas.
"""

import pytest
from typing import Generator, Dict, Any
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.config import settings


# Configuración de base de datos de pruebas
def get_test_database_url():
    """Genera una URL única para cada test"""
    import uuid
    return f"sqlite:///./test_{uuid.uuid4().hex[:8]}.db?mode=memory&cache=shared"

def create_test_engine():
    """Crea un engine único para cada test"""
    db_url = get_test_database_url()
    return create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,  # Desactivar logging SQL
    )

# Crear sesión de pruebas
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False)


@pytest.fixture(scope="function")
def db_engine():
    """Engine de base de datos para cada prueba individual"""
    engine = create_test_engine()
    yield engine
    # Limpiar al final
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Sesión de base de datos para cada prueba individual"""
    # Crear todas las tablas al inicio de cada test
    Base.metadata.create_all(bind=db_engine)
    
    # Crear una nueva sesión para cada prueba
    connection = db_engine.connect()
    transaction = connection.begin()
    
    # Crear sesión con la transacción
    session = TestingSessionLocal(bind=connection)
    
    # Configurar rollback automático
    session.begin_nested()
    
    yield session
    
    # Rollback automático al final de cada prueba
    session.rollback()
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Cliente de pruebas FastAPI con base de datos mock"""
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Override de la dependencia de base de datos
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Limpiar override
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def test_settings() -> Dict[str, Any]:
    """Configuración de pruebas"""
    return {
        "database_url": "sqlite:///./test.db",
        "secret_key": "test-secret-key-for-testing-only",
        "algorithm": "HS256",
        "access_token_expire_minutes": 30,
        "refresh_token_expire_days": 7,
        "email_verification_expire_hours": 24,
        "password_reset_expire_hours": 1,
    }


@pytest.fixture(scope="function")
def clean_db(db_session: Session):
    """Fixture para limpiar la base de datos antes de cada prueba"""
    # Limpiar todas las tablas en orden inverso (por dependencias)
    tables_to_clean = [
        "role_permission",
        "user_role", 
        "company_user",
        "user_identity",
        "invalidated_token",
        "permission",
        "role",
        "user",
        "company"
    ]
    
    for table in tables_to_clean:
        try:
            db_session.execute(f"DELETE FROM {table}")
        except:
            pass  # La tabla puede no existir aún
    
    db_session.commit()
    yield
    # La limpieza se hace automáticamente por el rollback de db_session


# Configuración de pytest para evitar warnings de SQLAlchemy
@pytest.fixture(autouse=True)
def setup_test_environment(db_engine):
    """Configuración automática del entorno de pruebas"""
    # Configurar SQLite para pruebas
    import sqlite3
    
    def _sqlite_on_connect(dbapi_connection, connection_record):
        # Habilitar foreign keys
        dbapi_connection.execute("PRAGMA foreign_keys=ON")
        # Configurar modo WAL para mejor rendimiento
        dbapi_connection.execute("PRAGMA journal_mode=WAL")
    
    event.listen(db_engine, "connect", _sqlite_on_connect)
    
    yield
    
    # Limpiar listeners
    event.remove(db_engine, "connect", _sqlite_on_connect)


# Importar fixtures específicas de API
pytest_plugins = [
    "tests.fixtures.api_fixtures",
    "tests.fixtures.auth_fixtures",
    "tests.fixtures.user_fixtures",
    "tests.fixtures.company_fixtures",
    "tests.fixtures.role_fixtures",
    "tests.fixtures.db_fixtures"
] 