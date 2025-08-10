# Usar imagen Python 3.11-slim (versión estable)
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar uv para gestión de dependencias
RUN pip install uv

# Copiar archivos de dependencias
COPY pyproject.toml poetry.lock README.md ./

# Copiar código de la aplicación primero
COPY app/ ./app/
COPY alembic.ini ./
COPY tests/ ./tests/

# Instalar dependencias usando uv
RUN uv pip install --system -e .

# Exponer puerto 8002
EXPOSE 8002

# Comando para ejecutar uvicorn con hot reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"] 