# 🚀 Configuración SMTP - Instrucciones Paso a Paso

## ⚠️ **IMPORTANTE: Antes de continuar**

Este error indica que las credenciales SMTP de Gmail no son válidas:
```
(535, b'5.7.8 Username and Password not accepted. For more information, go to\n5.7.8  https://support.google.com/mail/?p=BadCredentials')
```

## 🔧 **PASOS PARA RESOLVER EL PROBLEMA**

### **PASO 1: Crear archivo `.env`**

1. En la raíz del proyecto, crea un archivo llamado `.env`
2. Copia el contenido de `env.example` y modifica las credenciales:

```bash
# Configuración del Servidor SMTP para Gmail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USERNAME=TU_EMAIL_REAL@gmail.com
SMTP_PASSWORD=TU_APP_PASSWORD_16_CARACTERES

# Configuración de la aplicación
SMTP_FROM_EMAIL=TU_EMAIL_REAL@gmail.com
SMTP_FROM_NAME=Base Auth Backend

# URLs de la aplicación (para enlaces en emails)
APP_BASE_URL=http://localhost:4200
PASSWORD_RESET_URL=/token-validate
EMAIL_VERIFICATION_URL=/email-validate
```

### **PASO 2: Obtener App Password de Gmail**

1. Ve a [myaccount.google.com](https://myaccount.google.com/)
2. Navega a **Seguridad** → **Verificación en 2 pasos**
3. En la parte inferior, haz clic en **Contraseñas de aplicación**
4. Selecciona **Otra (nombre personalizado)** y escribe "Base Auth Backend"
5. Copia la contraseña generada (16 caracteres)

### **PASO 3: Verificar configuración**

Ejecuta el script de verificación:
```bash
python scripts/verify_smtp_config.py
```

### **PASO 4: Probar envío de emails**

Si la verificación pasa, prueba el envío:
```bash
python scripts/test_email_service.py
```

### **PASO 5: Reiniciar servicios Docker**

```bash
docker-compose down
docker-compose up -d
```

## 🔍 **VERIFICACIONES ADICIONALES**

### **Verificar que 2FA esté habilitado**
- Gmail requiere 2FA para usar App Passwords
- Sin 2FA, solo funcionan contraseñas normales (menos seguras)

### **Verificar App Password**
- Debe tener exactamente 16 caracteres
- No incluir espacios al inicio o final
- Copiar exactamente como aparece en Gmail

### **Verificar cuenta de Gmail**
- La cuenta no debe estar suspendida
- No debe tener restricciones de seguridad
- Debe permitir acceso de aplicaciones menos seguras

## 🐳 **CONFIGURACIÓN EN DOCKER**

El `docker-compose.yml` ya está configurado para usar las variables de entorno del archivo `.env`.

## 📝 **LOGS Y DEBUGGING**

### **Ver logs del servicio**
```bash
docker-compose logs -f base_auth_backend
```

### **Verificar variables de entorno en Docker**
```bash
docker-compose exec base_auth_backend env | grep SMTP
```

## 🚨 **PROBLEMAS COMUNES**

### **Error 535 - Credenciales inválidas**
- Verificar que el App Password sea correcto
- Confirmar que 2FA esté habilitado
- Revisar que no haya espacios extra

### **Error de conexión SMTP**
- Verificar que el puerto 587 esté abierto
- Confirmar que TLS esté habilitado
- Revisar firewall/antivirus

### **Emails no se envían**
- Verificar logs del servicio
- Confirmar que las variables estén en el archivo `.env`
- Revisar que el archivo `.env` esté en la raíz del proyecto

## ✅ **VERIFICACIÓN FINAL**

Después de completar todos los pasos:

1. ✅ Archivo `.env` creado con credenciales reales
2. ✅ App Password de Gmail configurado
3. ✅ Script de verificación pasa sin errores
4. ✅ Script de prueba envía emails correctamente
5. ✅ Servicios Docker reiniciados
6. ✅ API funciona sin errores SMTP

## 📞 **SOPORTE**

Si persisten los problemas:
1. Revisar logs completos del servicio
2. Verificar configuración de Gmail
3. Probar con una cuenta de Gmail diferente
4. Verificar que no haya restricciones de red
