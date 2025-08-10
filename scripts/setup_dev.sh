#!/bin/bash

# Script de configuración para desarrollo local
# Configura PostgreSQL y la aplicación

set -e

echo "🚀 Configurando entorno de desarrollo para base_auth_backend..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi

echo "✅ Docker y Docker Compose están instalados"

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cat > .env << 'EOF'
# Configuración de la aplicación
APP_TITLE=Base Auth Backend
APP_VERSION=0.1.0
DEBUG=true
LOG_LEVEL=DEBUG

# Configuración de la base de datos PostgreSQL
DATABASE_URL=postgresql://postgres:1234@localhost:5432/base_auth
DATABASE_ECHO=true
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Configuración de seguridad
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
EOF
    echo "✅ Archivo .env creado"
else
    echo "✅ Archivo .env ya existe"
fi

# Iniciar solo la base de datos
echo "🐘 Iniciando PostgreSQL..."
docker-compose up -d db

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando a que PostgreSQL esté listo..."
sleep 10

# Verificar que PostgreSQL esté funcionando
echo "🔍 Verificando conexión a PostgreSQL..."
if docker-compose exec db pg_isready -U postgres; then
    echo "✅ PostgreSQL está funcionando correctamente"
else
    echo "❌ Error: PostgreSQL no está funcionando"
    exit 1
fi

# Instalar dependencias de Python
echo "📦 Instalando dependencias de Python..."
if command -v poetry &> /dev/null; then
    poetry install
else
    pip install -r requirements.txt
fi

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones..."
docker-compose exec api alembic upgrade head

# Ejecutar datos de prueba
echo "🌱 Ejecutando datos de prueba..."
docker-compose exec api python -m app.db.seeds

echo ""
echo "🎉 ¡Configuración completada!"
echo ""
echo "📋 Comandos útiles:"
echo "  make start         - Iniciar todo el entorno"
echo "  make stop          - Detener todo"
echo "  make db-up         - Solo iniciar PostgreSQL"
echo "  make db-migrate    - Crear nueva migración"
echo "  make db-upgrade    - Aplicar migraciones"
echo "  make logs          - Ver logs"
echo ""
echo "🌐 La API estará disponible en: http://localhost:8002"
echo "📊 PostgreSQL estará disponible en: localhost:5432"
echo "   Usuario: postgres"
echo "   Contraseña: 1234"
echo "   Base de datos: base_auth"
echo ""
echo "👤 Usuario de prueba creado:"
echo "   Email: admin@system.com"
echo "   Contraseña: admin123" 