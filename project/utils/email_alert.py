import smtplib
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email import encoders
import os

def enviar_alerta_email(num_ofertas, receptor):
    remitente = "rubencruzglez@gmail.com"
    contraseña = "vega cxtw iwid tnpr"

    asunto = f"Bot de empleo – {num_ofertas} ofertas encontradas"
    cuerpo = (
        f"Se han encontrado {num_ofertas} ofertas nuevas.\n\n"
        f"Adjunto el archivo 'resultados.csv' con los detalles."
    )

    # Creamos un nuevo objeto de mensaje de correo
    mensaje = EmailMessage()

    # Establecemos el remitente del correo
    mensaje["From"] = remitente

    # Establecemos el destinatario (a quién se va a enviar el correo)
    mensaje["To"] = receptor

    # Establecemos el asunto del correo
    mensaje["Subject"] = asunto

    # Establecemos el cuerpo del mensaje (texto plano con codificación UTF-8)
    mensaje.set_content(cuerpo, charset="utf-8")

    # Definimos la ruta al archivo de resultados
    ruta_csv = "data/resultados.csv"

    # Comprobamos si el archivo existe antes de intentar adjuntarlo
    if os.path.exists(ruta_csv):
        # Abrimos el archivo en modo lectura binaria
        with open(ruta_csv, "rb") as f:
            # Creamos una parte MIME con tipo 'application/octet-stream' (archivo genérico)
            parte = MIMEBase("application", "octet-stream")

            # Cargamos el contenido binario del archivo en la parte
            parte.set_payload(f.read())

            # Codificamos el archivo en base64 para asegurar compatibilidad
            encoders.encode_base64(parte)

            # Añadimos una cabecera con el nombre del archivo adjunto
            parte.add_header(
                "Content-Disposition",     # Tipo de contenido: adjunto
                "attachment",              # Indicamos que es un adjunto
                filename="ofertas.csv"     # Nombre con el que aparecerá en el correo
            )

        # Convertimos el mensaje en multipart/mixed para permitir adjuntos
        mensaje.make_mixed()

        # Añadimos el archivo adjunto al mensaje
        mensaje.attach(parte)

    try:
        # Abrimos una conexión segura con el servidor de Gmail (puerto 465)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            # Iniciamos sesión con las credenciales del remitente
            smtp.login(remitente, contraseña)

            # Enviamos el mensaje con el adjunto incluido
            smtp.send_message(mensaje)

            # Confirmamos en consola que el correo se ha enviado
            print("Correo con adjunto enviado correctamente.")

    # Captura cualquier error que pueda ocurrir durante el envío
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
