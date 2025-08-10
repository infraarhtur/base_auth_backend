.PHONY: start stop restart build logs clean help db-up db-down db-migrate db-upgrade db-downgrade db-reset db-seed

# Comando principal para iniciar el entorno de desarrollo
start:
	docker-compose up -d --build  

# Detener los contenedores
stop:
	docker-compose down

# Reiniciar los contenedores
restart:
	docker-compose restart

# Construir las imágenes
build:
	docker-compose build

# Ver los logs de los contenedores
logs:
	docker-compose logs -f

# Limpiar contenedores, volúmenes e imágenes
clean:
	docker-compose down -v --rmi all --remove-orphans

# Comandos de base de datos
db-up:
	docker-compose up -d db

db-down:
	docker-compose stop db

db-migrate:
	docker-compose exec api alembic revision --autogenerate -m "$(message)"

db-upgrade:
	docker-compose exec api alembic upgrade head

db-downgrade:
	docker-compose exec api alembic downgrade -1

db-reset:
	docker-compose exec api alembic downgrade base
	docker-compose exec api alembic upgrade head

db-seed:
	docker-compose exec api python -m app.db.seeds

# Mostrar ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make start         - Iniciar el entorno de desarrollo"
	@echo "  make stop          - Detener los contenedores"
	@echo "  make restart       - Reiniciar los contenedores"
	@echo "  make build         - Construir las imágenes"
	@echo "  make logs          - Ver logs de los contenedores"
	@echo "  make clean         - Limpiar contenedores y volúmenes"
	@echo ""
	@echo "Comandos de base de datos:"
	@echo "  make db-up         - Iniciar solo la base de datos"
	@echo "  make db-down       - Detener la base de datos"
	@echo "  make db-migrate    - Crear nueva migración (message='descripción')"
	@echo "  make db-upgrade    - Aplicar migraciones pendientes"
	@echo "  make db-downgrade  - Revertir última migración"
	@echo "  make db-reset      - Resetear base de datos (downgrade + upgrade)"
	@echo "  make db-seed       - Ejecutar datos de prueba"
	@echo "  make help          - Mostrar esta ayuda"

# Comando por defecto
.DEFAULT_GOAL := help 