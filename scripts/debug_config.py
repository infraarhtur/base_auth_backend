#!/usr/bin/env python3
"""
Script para debuggear la configuración y ver qué valores están siendo tomados
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))

def debug_config():
    """Debuggear la configuración completa"""
    
    print("🔍 Debuggeando configuración...")
    print("=" * 60)
    
    # Verificar archivo .env
    env_path = Path(__file__).parent.parent / ".env"
    print(f"📁 Archivo .env existe: {env_path.exists()}")
    
    if env_path.exists():
        print("📄 Contenido del archivo .env:")
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Ocultar contraseñas por seguridad
                    if 'PASSWORD' in line:
                        key, value = line.split('=', 1)
                        print(f"   {key}=***{value[-4:] if len(value) > 4 else '***'}")
                    else:
                        print(f"   {line}")
    
    print("\n🌐 Variables de entorno del sistema:")
    smtp_vars = ['SMTP_SERVER', 'SMTP_PORT', 'SMTP_USE_TLS', 'SMTP_USERNAME', 
                 'SMTP_FROM_EMAIL', 'SMTP_FROM_NAME', 'APP_BASE_URL', 
                 'PASSWORD_RESET_URL', 'EMAIL_VERIFICATION_URL']
    
    for var in smtp_vars:
        value = os.getenv(var, "NO DEFINIDA")
        if 'PASSWORD' in var and value != "NO DEFINIDA":
            print(f"   {var}=***{value[-4:] if len(value) > 4 else '***'}")
        else:
            print(f"   {var}={value}")
    
    print("\n⚙️  Configuración de la aplicación:")
    try:
        from app.core.config import get_settings
        settings = get_settings()
        
        print(f"   SMTP Server: {settings.email.smtp_server}")
        print(f"   SMTP Port: {settings.email.smtp_port}")
        print(f"   SMTP Use TLS: {settings.email.smtp_use_tls}")
        print(f"   SMTP Username: {settings.email.smtp_username}")
        print(f"   SMTP From Email: {settings.email.smtp_from_email}")
        print(f"   SMTP From Name: {settings.email.smtp_from_name}")
        print(f"   App Base URL: {settings.email.app_base_url}")
        print(f"   Password Reset URL: {settings.email.password_reset_url}")
        print(f"   Email Verification URL: {settings.email.email_verification_url}")
        
    except Exception as e:
        print(f"   ❌ Error cargando configuración: {e}")
    
    print("\n🔧 Servicio de Email:")
    try:
        from app.services.email_service import EmailService
        email_service = EmailService()
        
        print(f"   App Base URL (desde servicio): {email_service.app_base_url}")
        print(f"   SMTP Username (desde servicio): {email_service.smtp_username}")
        print(f"   SMTP From Email (desde servicio): {email_service.smtp_from_email}")
        
    except Exception as e:
        print(f"   ❌ Error cargando servicio de email: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    debug_config()
