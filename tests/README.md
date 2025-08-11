# Estructura de Pruebas

Este directorio contiene todas las pruebas del proyecto base_auth_backend.

## Estructura de Directorios

```
tests/
├── unit/                          # Pruebas unitarias
│   ├── test_models/              # Pruebas de modelos de BD
│   ├── test_schemas/             # Pruebas de esquemas Pydantic
│   ├── test_services/            # Pruebas de servicios de negocio
│   ├── test_api/                 # Pruebas de endpoints API
│   └── test_utils/               # Pruebas de utilidades
├── integration/                   # Pruebas de integración
│   ├── test_api/                 # Pruebas de API completa
│   └── test_database/            # Pruebas con BD real
├── fixtures/                      # Fixtures compartidas
└── utils/                         # Utilidades para pruebas
```

## Tipos de Pruebas

### Pruebas Unitarias (`unit/`)
- **test_models/**: Pruebas de modelos de base de datos
- **test_schemas/**: Pruebas de validación de esquemas
- **test_services/**: Pruebas de lógica de negocio
- **test_api/**: Pruebas de endpoints individuales
- **test_utils/**: Pruebas de funciones de utilidad

### Pruebas de Integración (`integration/`)
- **test_api/**: Pruebas de flujos completos de API
- **test_database/**: Pruebas con base de datos real

## Marcadores de Pruebas

- `@pytest.mark.unit`: Pruebas unitarias
- `@pytest.mark.integration`: Pruebas de integración
- `@pytest.mark.slow`: Pruebas lentas
- `@pytest.mark.auth`: Pruebas de autenticación
- `@pytest.mark.user`: Pruebas de gestión de usuarios
- `@pytest.mark.company`: Pruebas de gestión de empresas
- `@pytest.mark.role`: Pruebas de roles y permisos

## Ejecución de Pruebas

### Ejecutar todas las pruebas
```bash
pytest
```

### Ejecutar solo pruebas unitarias
```bash
pytest tests/unit/
```

### Ejecutar solo pruebas de integración
```bash
pytest tests/integration/
```

### Ejecutar con cobertura
```bash
pytest --cov=app --cov-report=html
```

### Ejecutar pruebas específicas por marcador
```bash
pytest -m "unit and not slow"
pytest -m "auth"
```

### Ejecutar pruebas en paralelo
```bash
pytest -n auto
```

## Configuración

- **pyproject.toml**: Configuración principal de pytest
- **pytest.ini**: Configuración alternativa
- **.coveragerc**: Configuración de cobertura de código

## Dependencias de Desarrollo

Instalar dependencias de desarrollo:
```bash
pip install -r requirements-dev.txt
```

## Convenciones de Nomenclatura

- Archivos de prueba: `test_*.py`
- Clases de prueba: `Test*`
- Funciones de prueba: `test_*`
- Fixtures: `*_fixture` o `*_data`
- Factories: `*Factory` 