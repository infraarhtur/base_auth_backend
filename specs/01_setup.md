# 🛠️ Configuración Inicial del Proyecto `base_auth_backend`

Este documento describe cómo crear y estructurar un proyecto básico en **FastAPI** para un microservicio de autenticación llamado `base_auth_backend`.

Primero lo configuraremos para funcionar localmente y luego procederemos a su **dockerización**.

---

## 🔧 Stack Tecnológico

Este microservicio usará el siguiente stack:

- **FastAPI** – Framework web moderno y asíncrono basado en Python.
- **SQLAlchemy** – ORM para la capa de persistencia.
- **Alembic** – Herramienta de migraciones y control de versiones de la base de datos.
- **PostgreSQL** – Base de datos relacional robusta y de alto rendimiento.
- **Poetry** – Gestor de dependencias y empaquetado de proyectos Python.
- **Pydantic v2** – Tipado y validación de datos.
- **PyYAML** – Carga de configuración desde archivos `.yaml`.
- **JWT** – Autenticación basada en tokens seguros.
- **Black** – Formateador automático de código.
- **Docker** – Contenedores para entorno de desarrollo y despliegue.
- **GitHub** – Control de versiones y colaboración.

---

## ✅ Paso 1: Crear la estructura base del proyecto

Genera la siguiente estructura de carpetas y archivos para organizar el microservicio:
```
base_auth_backend/
│
├── app/
│ ├── api/ # Rutas organizadas por entidad
│ │ ├── deps.py # Dependencias comunes (get_db, get_user, etc.)
│ │ ├── v1/ # Versionado de la API
│ │ │ ├── auth.py
│ │ │ ├── user.py
│ │ │ └── company.py
│ │ └── init.py
│ │
│ ├── core/ # Configuración, seguridad, logging
│ │ ├── config.py
│ │ ├── security.py
│ │ └── logging.py
│ │
│ ├── models/ # Modelos SQLAlchemy
│ ├── schemas/ # Esquemas Pydantic v2 (entrada/salida)
│ ├── services/ # Lógica de negocio y autenticación
│ ├── db/ # Sesión, base declarativa y seeding
│ └── main.py # Punto de entrada de la aplicación FastAPI
│
├── alembic/ # Migraciones de base de datos
├── tests/ # Pruebas automatizadas con Pytest
├── .env # Variables de entorno
├── pyproject.toml # Configuración de dependencias con Poetry
├── docker-compose.yml # Servicios como PostgreSQL, pgAdmin, etc.
└── README.md # Documentación general del proyecto
```


---

## ✅ Paso 2: Configurar el entorno y las dependencias

Inicializa el proyecto con Poetry y añade las siguientes dependencias:

```bash
poetry init --name base_auth_backend --python "^3.11"
poetry add fastapi sqlalchemy alembic psycopg2-binary pydantic PyYAML python-jose[cryptography]
poetry add --group dev black pytest isort

## ✅ Paso 3: Coloca la configuracion del proyecto 
en config.py
Incluir PROJECT_NAME, VERSION
- Incluir DATABASE_URL para PostgreSQL
- Configurar para leer variables de entorno

## PASO 4: Crear aplicación FastAPI básica

En app/main.py:
- Crear instancia FastAPI con título y versión desde config
- Endpoint GET "/" que retorne mensaje de bienvenida
- Endpoint GET "/health" que retorne status, service name y version
- NO crear otros endpoints aún

## PASO 5: Verificar funcionamiento local

## ✅ PASO 5: Verificar el funcionamiento local del proyecto

En este paso vamos a asegurarnos de que el proyecto puede ejecutarse correctamente en tu máquina utilizando `poetry` para gestionar las dependencias y `uv` para crear el entorno de desarrollo.

### 🔧 1. Crear el entorno virtual con Python 3.13 (usando `uv`)

Asegúrate de tener instalada la versión **3.13** de Python y `uv`. Luego, ejecuta:

```bash
uv venv --python=3.13
- crea un entorno virtual  en UV  python en la version 3.13 
Verificar que respondan:
- http://localhost:8002/ (mensaje bienvenida)
- http://localhost:8002/health (status ok)
- http://localhost:8002/docs (documentación automática)

## PASO 6: Crear Dockerfile

- Usar imagen Python python:3.11-slim
- Instalar uv para gestión de dependencias
- Copiar y instalar dependencias del pyproject.toml
- Copiar código de la aplicación
- Exponer puerto 8002
- Comando para ejecutar uvicorn con hot reload

## PASO 7: Crear docker-compose.yml

Configurar dos servicios:

**Servicio db:**
- PostgreSQL 15
- Variables de entorno: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
- Puerto 5432
- Volume para persistencia de datos

**Servicio api:**
- Build desde Dockerfile local
- Puerto 8002
- Volume para desarrollo (hot reload)
- Variables de entorno para conexión a DB
- Depende del servicio db

## PASO 8: Verificar funcionamiento en Docker

Ejecutar:
```bash
docker-compose up --build
```

Verificar que respondan igual que en local:
- http://localhost:8002/


## PASO 9: Configurar conexión a base de datos

En app/db/base.py:
- Configurar SQLAlchemy engine
- Crear SessionLocal para sesiones de DB
- Crear Base declarativa para futuros modelos
- Función get_db() para dependency injection