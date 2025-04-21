from scraper import buscar_ofertas
from utils.email_alert import enviar_alerta_email
import pandas as pd
import os
import logging
import traceback
from datetime import datetime
import sys

# Configura tu correo
EMAIL_RECEPTOR = "alu0101340814@ull.edu.es"

# Crear carpetas necesarias
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

# Configurar logging
logging.basicConfig(filename="logs/log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    try:
        ofertas = buscar_ofertas()

        if ofertas:
            # Añadir fecha y hora a cada oferta
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for oferta in ofertas:
                oferta["Fecha"] = timestamp

            # Guardar CSV
            df = pd.DataFrame(ofertas)
            df.to_csv("data/resultados.csv", index=False)

            # Enviar alerta por correo
            enviar_alerta_email(len(ofertas), EMAIL_RECEPTOR)

            logging.info(f"{len(ofertas)} ofertas encontradas y guardadas en {timestamp}.")
        else:
            logging.info("No se encontraron ofertas.")
            enviar_alerta_email(0, EMAIL_RECEPTOR)
    except Exception:
        logging.error("Error en la ejecución:\n" + traceback.format_exc())
    finally:
        sys.exit()

if __name__ == "__main__":
    main()
