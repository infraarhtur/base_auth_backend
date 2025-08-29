"""
Servicio de email - Envío de emails para verificación y reset de contraseña
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from fastapi import HTTPException, status

from app.core.config import get_settings

# Obtener configuración
settings = get_settings()


class EmailService:
    """Servicio para envío de emails"""
    
    def __init__(self):
        self.smtp_server = settings.email.smtp_server
        self.smtp_port = settings.email.smtp_port
        self.smtp_use_tls = settings.email.smtp_use_tls
        self.smtp_username = settings.email.smtp_username
        self.smtp_password = settings.email.smtp_password
        self.smtp_from_email = settings.email.smtp_from_email
        self.smtp_from_name = settings.email.smtp_from_name
        self.app_base_url = settings.email.app_base_url
    
    def _create_message(self, to_email: str, subject: str, html_content: str) -> MIMEMultipart:
        """
        Crear mensaje de email
        
        Args:
            to_email: Email del destinatario
            subject: Asunto del email
            html_content: Contenido HTML del email
            
        Returns:
            Mensaje MIME configurado
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{self.smtp_from_name} <{self.smtp_from_email}>"
        message["To"] = to_email
        
        # Agregar contenido HTML
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        return message
    
    def _send_email(self, message: MIMEMultipart) -> bool:
        """
        Enviar email usando SMTP
        
        Args:
            message: Mensaje MIME a enviar
            
        Returns:
            True si se envió correctamente
        """
        try:
            # Crear conexión SMTP
            if self.smtp_use_tls:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            
            # Autenticación
            server.login(self.smtp_username, self.smtp_password)
            
            # Enviar email
            server.send_message(message)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error enviando email: {e}")
            return False
    
    def _get_password_reset_template(self, token: str, user_name: str) -> str:
        """
        Generar template HTML para reset de contraseña
        
        Args:
            token: Token de reset
            user_name: Nombre del usuario
            
        Returns:
            Template HTML del email
        """
        passwordReset = settings.email.password_reset_url
        print('passwordReset', passwordReset  )
        print('app_base_url', self.app_base_url)

        reset_url = f"{self.app_base_url}{passwordReset}/{token}"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset de Contraseña</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #007bff;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 0 0 5px 5px;
                }}
                .button {{
                    display: inline-block;
                    background-color: #007bff;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔐 Reset de Contraseña</h1>
            </div>
            <div class="content">
                <p>Hola <strong>{user_name}</strong>,</p>
                
                <p>Has solicitado restablecer tu contraseña. Haz clic en el botón de abajo para continuar:</p>
                
                <div style="text-align: center;">
                    <a href="{reset_url}" class="button">Restablecer Contraseña</a>
                </div>
                
                <p>Si no solicitaste este cambio, puedes ignorar este email.</p>
                
                <p><strong>Importante:</strong> Este enlace expirará en 1 hora por seguridad.</p>
                
                <p>Si el botón no funciona, copia y pega este enlace en tu navegador:</p>
                <p style="word-break: break-all; color: #007bff;">{reset_url}</p>
            </div>
            <div class="footer">
                <p>Este email fue enviado por {self.smtp_from_name}</p>
                <p>Si tienes alguna pregunta, contacta con soporte.</p>
            </div>
        </body>
        </html>
        """
    
    def _get_email_verification_template(self, token: str, user_name: str) -> str:
        """
        Generar template HTML para verificación de email
        
        Args:
            token: Token de verificación
            user_name: Nombre del usuario
            
        Returns:
            Template HTML del email
        """
        verification_url = f"{self.app_base_url}{settings.email.email_verification_url}?token={token}"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verificación de Email</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #28a745;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 0 0 5px 5px;
                }}
                .button {{
                    display: inline-block;
                    background-color: #28a745;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>✅ Verifica tu Email</h1>
            </div>
            <div class="content">
                <p>Hola <strong>{user_name}</strong>,</p>
                
                <p>Gracias por registrarte. Para completar tu registro, necesitamos verificar tu dirección de email.</p>
                
                <div style="text-align: center;">
                    <a href="{verification_url}" class="button">Verificar Email</a>
                </div>
                
                <p>Si no creaste esta cuenta, puedes ignorar este email.</p>
                
                <p><strong>Importante:</strong> Este enlace expirará en 24 horas.</p>
                
                <p>Si el botón no funciona, copia y pega este enlace en tu navegador:</p>
                <p style="word-break: break-all; color: #28a745;">{verification_url}</p>
            </div>
            <div class="footer">
                <p>Este email fue enviado por {self.smtp_from_name}</p>
                <p>Si tienes alguna pregunta, contacta con soporte.</p>
            </div>
        </body>
        </html>
        """
    
    def send_password_reset_email(self, email: str, token: str, user_name: str) -> bool:
        """
        Enviar email de reset de contraseña
        
        Args:
            email: Email del destinatario
            token: Token de reset
            user_name: Nombre del usuario
            
        Returns:
            True si se envió correctamente
        """
        subject = "🔐 Reset de Contraseña - Base Auth Backend"
        html_content = self._get_password_reset_template(token, user_name)
        
        message = self._create_message(email, subject, html_content)
        return self._send_email(message)
    
    def send_verification_email(self, email: str, token: str, user_name: str) -> bool:
        """
        Enviar email de verificación
        
        Args:
            email: Email del destinatario
            token: Token de verificación
            user_name: Nombre del usuario
            
        Returns:
            True si se envió correctamente
        """
        subject = "✅ Verifica tu Email - Base Auth Backend"
        html_content = self._get_email_verification_template(token, user_name)
        
        message = self._create_message(email, subject, html_content)
        return self._send_email(message)
    
    def test_connection(self) -> bool:
        """
        Probar conexión SMTP
        
        Returns:
            True si la conexión es exitosa
        """
        try:
            if self.smtp_use_tls:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            
            server.login(self.smtp_username, self.smtp_password)
            server.quit()
            return True
            
        except Exception as e:
            print(f"Error en conexión SMTP: {e}")
            return False 