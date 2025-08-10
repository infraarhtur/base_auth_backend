# 🛡️ base_auth - Backend de Autenticación Multitenant

Este proyecto es un servicio de autenticación backend desarrollado con **FastAPI** que permite gestionar múltiples empresas (tenants), usuarios, roles y permisos, con un enfoque escalable y seguro para aplicaciones SaaS.

Diseñado para ser desacoplado y reutilizable en otros módulos como sistemas de inventario, ventas u otras plataformas que requieran autenticación robusta y control de acceso granular.

---

## 🚀 Stack Tecnológico

- **[FastAPI](https://fastapi.tiangolo.com/)** – API web moderna, rápida y basada en Python
- **[SQLAlchemy](https://www.sqlalchemy.org/)** – ORM para la capa de persistencia
- **[Alembic](https://alembic.sqlalchemy.org/)** – Control de versiones/migraciones de base de datos
- **[PostgreSQL](https://www.postgresql.org/)** – Base de datos relacional de alto rendimiento
- **[Poetry](https://python-poetry.org/)** – Gestión de dependencias y empaquetado
- **[Pydantic v2](https://docs.pydantic.dev/)** – Validación y tipado de datos
- **[PyYAML](https://pyyaml.org/)** – Carga de configuración desde archivos `.yaml`
- **[JWT](https://jwt.io/)** – Autenticación mediante tokens seguros
- **[Black](https://black.readthedocs.io/)** – Formateador de código
- **[GitHub](https://github.com/)** – Control de versiones y colaboración

---

## 🧱 Entidades Principales

- `company` – Empresa o tenant del sistema
- `app_user` – Usuario del sistema, desacoplado de una empresa
- `company_user` – Asociación muchos-a-muchos entre usuarios y empresas
- `role` – Rol definido por empresa
- `permission` – Permisos globales del sistema
- `user_role` – Asignación de roles a usuarios
- `role_permission` – Permisos asignados a roles
- `user_identity` – Autenticación con terceros (Google, Facebook, etc.)

---

## 🧩 Arquitectura del Proyecto
``` base_auth_backend
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
│ └── main.py # Punto de entrada FastAPI
│
├── alembic/ # Migraciones de BD
├── tests/ # Pruebas automatizadas con Pytest
├── .env # Variables de entorno
├── pyproject.toml # Configuración de Poetry
├── docker-compose.yml # PostgreSQL, PGAdmin, etc.
└── README.md

```




---

## 📦 Características

- Registro de empresas con usuarios administradores
- Autenticación con JWT
- Control de acceso basado en roles y permisos
- Multitenencia con aislamiento lógico por empresa
- Integración preparada para autenticación con Google/Facebook
- Base lista para integrar con microservicios como inventario, ventas, etc.
- Listo para despliegue en contenedores (Docker)

---

## 🔧 En desarrollo

- [ ] CLI para administración de usuarios y empresas
- [ ] Sistema de invitación por email
- [ ] Auditoría de acciones por usuario
- [ ] Integración con Keycloak u otros IdPs (opcional)

---

## 🚀 Configuración Rápida

### Prerrequisitos
- Docker y Docker Compose
- Python 3.8+ (para desarrollo local)
- Poetry (opcional, para gestión de dependencias)

### Configuración Automática
```bash
# Ejecutar script de configuración
./scripts/setup_dev.sh
```

### Configuración Manual

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd base_auth_backend
```

2. **Crear archivo .env**
```bash
cp .env.example .env
# Editar las variables según tu entorno
```

3. **Iniciar PostgreSQL**
```bash
make db-up
```

4. **Instalar dependencias**
```bash
# Con Poetry
poetry install

# O con pip
pip install -r requirements.txt
```

5. **Ejecutar migraciones**
```bash
make db-upgrade
```

6. **Ejecutar datos de prueba**
```bash
make db-seed
```

7. **Iniciar la aplicación**
```bash
make start
```

### Comandos Útiles

```bash
# Gestión de contenedores
make start          # Iniciar todo el entorno
make stop           # Detener contenedores
make restart        # Reiniciar contenedores
make logs           # Ver logs

# Gestión de base de datos
make db-up          # Solo iniciar PostgreSQL
make db-down        # Detener PostgreSQL
make db-migrate     # Crear nueva migración
make db-upgrade     # Aplicar migraciones
make db-downgrade   # Revertir migración
make db-reset       # Resetear base de datos
make db-seed        # Ejecutar datos de prueba

# Desarrollo
make build          # Construir imágenes
make clean          # Limpiar todo
```

### Acceso a la Aplicación

- **API**: http://localhost:8002
- **Documentación**: http://localhost:8002/docs
- **PostgreSQL**: localhost:5432
  - Usuario: `postgres`
  - Contraseña: `1234`
  - Base de datos: `base_auth`

### Usuario de Prueba

Se crea automáticamente un usuario administrador:
- **Email**: `admin@system.com`
- **Contraseña**: `admin123`

---

## 📄 Licencia

MIT © 2025 - Arthur Monsalve
