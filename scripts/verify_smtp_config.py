#!/usr/bin/env python3
"""
Script para verificar la configuración SMTP antes de ejecutar la aplicación
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar la configuración
sys.path.append(str(Path(__file__).parent.parent))

def check_env_file():
    """Verificar que existe el archivo .env"""
    env_path = Path(__file__).parent.parent / ".env"
    if not env_path.exists():
        print("❌ ERROR: No se encontró el archivo .env")
        print("   Crea el archivo .env basado en env.example")
        return False
    
    print("✅ Archivo .env encontrado")
    return True

def check_smtp_variables():
    """Verificar que las variables SMTP estén configuradas"""
    required_vars = [
        "SMTP_USERNAME",
        "SMTP_PASSWORD", 
        "SMTP_FROM_EMAIL",
        "APP_BASE_URL"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ ERROR: Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("   Asegúrate de que estén definidas en tu archivo .env")
        return False
    
    print("✅ Todas las variables SMTP están configuradas")
    return True

def check_smtp_credentials():
    """Verificar que las credenciales SMTP no sean valores por defecto"""
    username = os.getenv("SMTP_USERNAME", "")
    password = os.getenv("SMTP_PASSWORD", "")
    
    if username == "tu-email@gmail.com" or username == "":
        print("❌ ERROR: SMTP_USERNAME no está configurado correctamente")
        print("   Debe ser tu email real de Gmail")
        return False
    
    if password == "tu-app-password-de-16-caracteres" or password == "":
        print("❌ ERROR: SMTP_PASSWORD no está configurado correctamente")
        print("   Debe ser tu App Password de Gmail (16 caracteres)")
        return False
    
    if len(password) != 16:
        print("⚠️  ADVERTENCIA: SMTP_PASSWORD debe tener exactamente 16 caracteres")
        print("   Verifica que estés usando un App Password válido")
    
    print("✅ Credenciales SMTP configuradas")
    return True

def main():
    """Función principal de verificación"""
    print("🔍 Verificando configuración SMTP...")
    print("-" * 50)
    
    checks = [
        check_env_file(),
        check_smtp_variables(),
        check_smtp_credentials()
    ]
    
    print("-" * 50)
    if all(checks):
        print("✅ Todas las verificaciones pasaron. La configuración SMTP está lista.")
        print("\n📧 Para probar el envío de emails, ejecuta:")
        print("   python scripts/test_email_service.py")
    else:
        print("❌ Algunas verificaciones fallaron. Revisa la configuración antes de continuar.")
        sys.exit(1)

if __name__ == "__main__":
    main()
