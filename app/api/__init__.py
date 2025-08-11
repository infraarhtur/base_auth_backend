"""
API routes para la aplicación base_auth_backend
"""

from fastapi import FastAPI

from .v1 import auth, user, company, role, admin


def register_routes(app: FastAPI):
    """
    Registrar todas las rutas de la API en la aplicación FastAPI
    
    Args:
        app: Instancia de FastAPI
    """
    # Rutas de la API v1
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])
    app.include_router(user.router, prefix="/api/v1/users", tags=["Usuarios"])
    app.include_router(company.router, prefix="/api/v1/companies", tags=["Empresas"])
    app.include_router(role.router, prefix="/api/v1/roles", tags=["Roles y Permisos"])
    app.include_router(admin.router, prefix="/api/v1/admin", tags=["Administración"])


__all__ = ["register_routes"]
