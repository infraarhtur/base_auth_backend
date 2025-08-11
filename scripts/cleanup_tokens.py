#!/usr/bin/env python3
"""
Script de limpieza de tokens expirados
"""

import sys
import os
import argparse
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import get_db
from app.services.cleanup_service import CleanupService


def main():
    """Función principal del script"""
    parser = argparse.ArgumentParser(description="Limpieza de tokens expirados")
    parser.add_argument(
        "--stats", 
        action="store_true", 
        help="Mostrar estadísticas de la blacklist"
    )
    parser.add_argument(
        "--cleanup-expired", 
        action="store_true", 
        help="Limpiar tokens expirados"
    )
    parser.add_argument(
        "--cleanup-old", 
        type=int, 
        metavar="DAYS",
        help="Limpiar tokens más antiguos que X días"
    )
    parser.add_argument(
        "--all", 
        action="store_true", 
        help="Ejecutar todas las operaciones de limpieza"
    )
    
    args = parser.parse_args()
    
    # Si no se especifican argumentos, mostrar ayuda
    if not any([args.stats, args.cleanup_expired, args.cleanup_old, args.all]):
        parser.print_help()
        return
    
    try:
        db = next(get_db())
        cleanup_service = CleanupService(db)
        
        print("🧹 Servicio de limpieza de tokens")
        print("=" * 40)
        
        # Mostrar estadísticas
        if args.stats or args.all:
            print("\n📊 Estadísticas de la blacklist:")
            stats = cleanup_service.get_blacklist_stats()
            if stats:
                print(f"   Total de tokens: {stats['total_tokens']}")
                print(f"   Tokens expirados: {stats['expired_tokens']}")
                print(f"   Tokens activos: {stats['active_tokens']}")
                print(f"   Tokens de acceso: {stats['access_tokens']}")
                print(f"   Tokens de refresco: {stats['refresh_tokens']}")
                print(f"   Última actualización: {stats['last_updated']}")
            else:
                print("   ❌ No se pudieron obtener estadísticas")
        
        # Limpiar tokens expirados
        if args.cleanup_expired or args.all:
            print("\n🧹 Limpiando tokens expirados...")
            count = cleanup_service.cleanup_expired_tokens()
            print(f"   ✅ {count} tokens expirados eliminados")
        
        # Limpiar tokens antiguos
        if args.cleanup_old or args.all:
            days = args.cleanup_old or 30
            print(f"\n🧹 Limpiando tokens más antiguos que {days} días...")
            count = cleanup_service.cleanup_old_tokens(days)
            print(f"   ✅ {count} tokens antiguos eliminados")
        
        print("\n🎉 Operación completada")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 