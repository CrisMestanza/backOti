from rest_framework.response import Response
from rest_framework.decorators import api_view
import pandas as pd
import smtplib
import time  # Opcional, para evitar bloqueos
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from django.conf import settings
import os

@api_view(['POST'])
def enviar_correo_simple(request):
    destinatario = request.data.get('correo')
    mensaje_usuario = request.data.get('mensaje')
    asunto = request.data.get('asunto')

    if not destinatario or not mensaje_usuario or not asunto:
        return Response({
            "error": "Faltan datos (correo, mensaje o asunto)"
        }, status=400)

    remitente = "informatica@unsm.edu.pe"
    password = "jkdn rigo zsel tltj"

    try:
        # Crear mensaje
        mensaje = MIMEMultipart()
        mensaje["From"] = remitente
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto

        html = f"""
<html>
<body style="margin:0; padding:0; font-family: Arial, sans-serif; background-color:#f4f6f8;">
    
    <table width="100%" bgcolor="#f4f6f8" cellpadding="0" cellspacing="0">
        <tr>
            <td align="center">
                
                <table width="600" bgcolor="#ffffff" cellpadding="0" cellspacing="0" style="border-radius:10px; overflow:hidden; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
                    
                    <!-- HEADER -->
                    <tr>
                        <td style="background:#006633; color:white; text-align:center; padding:20px;">
                            <h2 style="margin:0;">UNSM - Sistema de Comunicación</h2>
                        </td>
                    </tr>

                    <!-- BODY -->
                    <tr>
                        <td style="padding:30px; color:#333;">
                            
                            <p style="font-size:16px;">
                                {mensaje_usuario}
                            </p>

                            <br>

                            <div style="background:#f1f5f9; padding:15px; border-radius:8px;">
                                <p style="margin:0; font-size:14px;">
                                    Este es un mensaje enviado desde el sistema institucional.
                                </p>
                            </div>

                        </td>
                    </tr>

                    <!-- FOOTER -->
                    <tr>
                        <td style="background:#f9fafb; text-align:center; padding:15px; font-size:12px; color:#777;">
                            © 2026 UNSM - Todos los derechos reservados
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>
"""

        mensaje.attach(MIMEText(html, "html"))

        # Conexión SMTP
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remitente, password)

        servidor.sendmail(remitente, destinatario, mensaje.as_string())
        servidor.quit()

        return Response({
            "mensaje": "Correo enviado correctamente"
        })

    except Exception as e:
        return Response({
            "error": f"Ocurrió un error: {str(e)}"
        }, status=500)
@api_view(['POST'])
def gmail(request):
    archivo = request.FILES.get('file')

    if not archivo:
        return Response({"error": "No se envió ningún archivo"}, status=400)
    print(f"Archivo recibido: {archivo.name}")
    

    # 1. Cargar y limpiar datos
    df = pd.read_excel(archivo, skiprows=5)
    # Seleccionamos las columnas necesarias basándonos en tu estructura
    dfPrincipal = df[["APELLIDOS Y NOMBRES", "CORREO INSTITUCIONAL",
                    "CONTRASEÑA DE PRIMER SESIÓN", "EMAIL PERSONAL"]]

    # Configuración de cuenta emisora
    remitente = "informatica@unsm.edu.pe"
    password = "jkdn rigo zsel tltj"

    # Función para preparar la imagen (para no repetir código en el bucle)


    def obtener_imagen(ruta, cid, nombre_visible):
        with open(ruta, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", f"<{cid}>")
            img.add_header("Content-Disposition", "inline",
                        filename=nombre_visible)
            return img


    # --- INICIO DEL PROCESO DE ENVÍO ---
    try:
        # Conexión única al servidor para mayor eficiencia
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remitente, password)

        for index, fila in dfPrincipal.iterrows():
            # Asignación de variables según tu solicitud
            nombre_usuario = fila["APELLIDOS Y NOMBRES"]
            correo_inst = fila["CORREO INSTITUCIONAL"]
            clave_temporal = fila["CONTRASEÑA DE PRIMER SESIÓN"]
            destinatario = fila["EMAIL PERSONAL"]  # Se envía al correo personal

            # Validar que el destinatario no esté vacío
            if pd.isna(destinatario):
                print(f"Saltando a {nombre_usuario}: No tiene email personal.")
                continue

            # Crear el contenedor del mensaje
            mensaje = MIMEMultipart("related")
            mensaje["From"] = remitente
            mensaje["To"] = destinatario
            mensaje["Subject"] = "Credenciales de tu Cuenta Institucional de Google - UNSM"

            # Cuerpo HTML con los datos de la fila actual
            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 0;">
                    <img src="cid:cabecera" style="width: 100%; display: block;">
                    <div style="padding: 20px;">
                        <h2 style="color: #006633; text-align: center;">Cuenta Institucional de Google - UNSM</h2>
                        <p>
                            Bienvenido(a): <strong>{nombre_usuario},</strong> 
                            por medio de la presente te hacemos llegar las credenciales de tu cuenta institucional de Google.
                            
                        </p>
                        <br>
                          <p>  <Strong> Si ya iniciaste sesión, omitir o ignorar este mensaje</Strong> </p>
                        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p><strong>Correo Institucional:</strong> {correo_inst}</p>
                            <p><strong>Contraseña:</strong> {clave_temporal}</p>
                        </div>
                        <p style="font-size: 13px;">
                        Se les recuerda que al iniciar sesión deberán actualizar su contraseña cumpliendo las políticas como la 
                        combinación de letras mayúsculas, minúsculas, números y caracteres especiales. En caso tengan 
                        inconvenientes o duda pueden enviarnos a través de <a href="mailto:informatica@unsm.edu.pe">informatica@unsm.edu.pe</a>
                        </p>
                        <br>
                        <p style="font-size: 15px; text-align: center;">
                            <strong>Gestiona de manera adecuada tu correo institucional </strong>
                        </p>
                        <p style="font-size: 14px; text-align: center;">
                            <a href="https://youtube.com/playlist?list=PLH6TUm6qmNq1zN7f4SueRosCQ_U1DUvtd&si=RQZGDOyZ4aJh_Uzd">Ver video</a>
                        </p>

                    </div>
                    <img src="cid:footer" style="width: 100%; display: block;">
                </div>
            </body>
            </html>
            """
            mensaje.attach(MIMEText(html, "html"))

            # Adjuntar imágenes en cada iteración
            ruta_cabecera = os.path.join(settings.MEDIA_ROOT, "gmail", "cabecera.jpeg")
            ruta_footer = os.path.join(settings.MEDIA_ROOT, "gmail", "footer.jpeg")

            mensaje.attach(obtener_imagen(ruta_cabecera, "cabecera", "Credenciales.jpg"))
            mensaje.attach(obtener_imagen(ruta_footer, "footer", "Informacion.jpg"))

            # Enviar
            servidor.sendmail(remitente, destinatario, mensaje.as_string())
            print(f"[{index+1}] Enviado con éxito a: {nombre_usuario} ({destinatario})")

            # Opcional: pausa de 1 segundo para no saturar el servidor de Gmail
            # time.sleep(1)

        print("\n--- ¡Envío masivo finalizado! ---")

    except Exception as e:
        print(f"Error en el proceso: {e}")

    finally:
        servidor.quit()
        
    return Response({
    "mensaje": "Archivo recibido correctamente",
    "nombre": archivo.name
    })
    