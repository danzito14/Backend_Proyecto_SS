import os

import sib_api_v3_sdk

BREVO_APIKEY = os.getenv("BREVO_APIKEY")
SENDER_EMAIL = "serviciosocialruizcortinesuas@gmail.com"
SENDER_NAME = "Servicio Social Ruiz Cortines UAS"


def enviar_link_activacion(email: str, nombre: str, token: str):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_APIKEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    link = f"http://localhost:8000/activar/activar?token={token}"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Activa tu cuenta</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f5f5f5;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px 0;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">

                        <!-- Header verde -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 40px 30px; text-align: center;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600; letter-spacing: -0.5px;">
                                    RUIZ CORTINES
                                </h1>
                                <p style="margin: 10px 0 0 0; color: #ffffff; font-size: 14px; opacity: 0.95;">
                                    Directorio de Negocios
                                </p>
                            </td>
                        </tr>

                        <!-- Contenido principal -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h2 style="margin: 0 0 20px 0; color: #1f2937; font-size: 24px; font-weight: 600;">
                                    ¡Hola, {nombre}! 👋
                                </h2>

                                <p style="margin: 0 0 20px 0; color: #4b5563; font-size: 16px; line-height: 1.6;">
                                    ¡Bienvenido/a al <strong>Directorio de Negocios de Ruiz Cortines</strong>! Estamos muy contentos de que te unas a nuestra comunidad.
                                </p>

                                <p style="margin: 0 0 20px 0; color: #4b5563; font-size: 16px; line-height: 1.6;">
                                    Para comenzar a explorar los negocios locales y conectar con tu comunidad, solo necesitas activar tu cuenta haciendo clic en el botón de abajo:
                                </p>

                                <!-- Botón de activación -->
                                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                    <tr>
                                        <td align="center">
                                            <a href="{link}" style="display: inline-block; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: #ffffff; text-decoration: none; padding: 16px 40px; border-radius: 6px; font-size: 16px; font-weight: 600; box-shadow: 0 4px 6px rgba(16, 185, 129, 0.3);">
                                                ✓ Activar mi cuenta
                                            </a>
                                        </td>
                                    </tr>
                                </table>

                                <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 16px; border-radius: 4px; margin: 25px 0;">
                                    <p style="margin: 0; color: #92400e; font-size: 14px; line-height: 1.5;">
                                        ⏰ <strong>Importante:</strong> Este enlace expirará en <strong>30 minutos</strong> por seguridad. Si no activas tu cuenta a tiempo, tendrás que registrarte nuevamente.
                                    </p>
                                </div>

                                <p style="margin: 25px 0 10px 0; color: #6b7280; font-size: 14px; line-height: 1.6;">
                                    Si el botón no funciona, copia y pega el siguiente enlace en tu navegador:
                                </p>

                                <p style="margin: 0; padding: 12px; background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 4px; word-break: break-all; font-size: 13px; color: #4b5563;">
                                    {link}
                                </p>
                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f9fafb; padding: 30px; text-align: center; border-top: 1px solid #e5e7eb;">
                                <p style="margin: 0 0 10px 0; color: #6b7280; font-size: 13px; line-height: 1.5;">
                                    Si no creaste una cuenta en nuestro directorio, puedes ignorar este correo de forma segura.
                                </p>

                                <p style="margin: 15px 0 0 0; color: #9ca3af; font-size: 12px;">
                                    © 2026 Servicio Social Ruiz Cortines UAS<br>
                                    Todos los derechos reservados
                                </p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    email_data = sib_api_v3_sdk.SendSmtpEmail(
        sender={
            "name": SENDER_NAME,
            "email": SENDER_EMAIL
        },
        to=[{
            "email": email,
            "name": nombre
        }],
        subject="🎉 Activa tu cuenta en el Directorio de Negocios",
        html_content=html_content
    )

    api_instance.send_transac_email(email_data)