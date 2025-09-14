# Configuración del Servicio de Email

## 📧 Configuración SMTP para Gmail

### 1. Crear App Password en Gmail

1. Ve a tu [Cuenta de Google](https://myaccount.google.com/)
2. Navega a **Seguridad** → **Verificación en 2 pasos**
3. En la parte inferior, haz clic en **Contraseñas de aplicación**
4. Selecciona **Otra (nombre personalizado)** y escribe "Base Auth Backend"
5. Copia la contraseña generada (16 caracteres)

### 2. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con:

```bash
# Configuración del Servidor SMTP para Gmail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_USERNAME=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password

# Configuración de la aplicación
SMTP_FROM_EMAIL=tu-email@gmail.com
SMTP_FROM_NAME=Base Auth Backend

# URLs de la aplicación (para enlaces en emails)
APP_BASE_URL=http://localhost:4200
PASSWORD_RESET_URL=/token-validate
EMAIL_VERIFICATION_URL=/email-validate
```

### 3. Verificar Configuración

Ejecuta el script de prueba:

```bash
python scripts/test_email_service.py
```

## 🚀 Funcionalidades Implementadas

### Reset de Contraseña

1. **Solicitar Reset**: `POST /auth/password-reset`
   - Envía email con token de reset
   - Token válido por 1 hora

2. **Confirmar Reset**: `POST /auth/password-reset/confirm`
   - Valida token y actualiza contraseña
   - Valida fortaleza de nueva contraseña

### Verificación de Email

1. **Solicitar Verificación**: `POST /auth/email-verification`
   - Envía email con token de verificación
   - Token válido por 24 horas

2. **Confirmar Verificación**: `POST /auth/email-verification/confirm`
   - Valida token y marca email como verificado

## 📋 Endpoints de la API

### Reset de Contraseña

```http
POST /auth/password-reset
Content-Type: application/json

{
  "email": "usuario@ejemplo.com"
}
```

```http
POST /auth/password-reset/confirm
Content-Type: application/json

{
  "token": "jwt-token-aqui",
  "new_password": "NuevaContraseña123!"
}
```

### Verificación de Email

```http
POST /auth/email-verification
Content-Type: application/json

{
  "email": "usuario@ejemplo.com"
}
```

```http
POST /auth/email-verification/confirm
Content-Type: application/json

{
  "token": "jwt-token-aqui"
}
```

## 🔧 Estructura del Proyecto

```
app/
├── services/
│   ├── email_service.py      # Servicio de email
│   └── auth_service.py       # Servicio de autenticación (actualizado)
├── core/
│   └── config.py             # Configuración (actualizada)
├── models/
│   └── user.py               # Modelo de usuario (actualizado)
└── api/v1/
    └── auth.py               # Endpoints (actualizados)
```

## 📝 Templates de Email

### Reset de Contraseña
- Diseño responsive con colores azules
- Botón de acción prominente
- Información de seguridad
- Enlace alternativo

### Verificación de Email
- Diseño responsive con colores verdes
- Botón de acción prominente
- Información de expiración
- Enlace alternativo

## 🧪 Testing

### Probar Conexión SMTP
```bash
python scripts/test_email_service.py
```

### Probar Endpoints
1. Inicia el servidor: `uvicorn app.main:app --reload`
2. Ve a: `http://localhost:8000/docs`
3. Prueba los endpoints de autenticación

## ⚠️ Consideraciones de Seguridad

1. **App Passwords**: Usa App Passwords, no contraseñas normales
2. **Tokens JWT**: Los tokens tienen tiempo de expiración limitado
3. **Validación**: Se valida fortaleza de contraseñas
4. **Logging**: Se registran todas las operaciones
5. **Rate Limiting**: Considera implementar limitación de tasa

## 🐛 Troubleshooting

### Error de Conexión SMTP
- Verifica credenciales de Gmail
- Asegúrate de usar App Password
- Verifica que 2FA esté habilitado

### Emails no se envían
- Revisa logs del servidor
- Verifica configuración SMTP
- Prueba conexión con script de test

### Tokens inválidos
- Verifica expiración (1h para reset, 24h para verificación)
- Asegúrate de usar el token correcto
- Verifica configuración de JWT

## 📚 Recursos Adicionales

- [Documentación de Gmail SMTP](https://support.google.com/mail/answer/7126229)
- [Configuración de App Passwords](https://support.google.com/accounts/answer/185833)
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de Alembic](https://alembic.sqlalchemy.org/) 