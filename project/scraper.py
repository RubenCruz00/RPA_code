from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import SEARCH_KEYWORD, NUM_RESULTS

def buscar_ofertas():
    keyword = SEARCH_KEYWORD.replace(" ", "+")
    url = f"https://www.tecnoempleo.com/ofertas-trabajo/?te={keyword}&pr=#buscador-ofertas"

    opciones = webdriver.ChromeOptions()
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    opciones.add_experimental_option("detach", False)  # Cierra siempre

    driver = webdriver.Chrome(options=opciones)

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.p-3.border.rounded.mb-3.bg-white")))

        cards = driver.find_elements(By.CSS_SELECTOR, "div.p-3.border.rounded.mb-3.bg-white")

        ofertas = []
        for card in cards[:NUM_RESULTS]:
            try:
                titulo = card.find_element(By.CSS_SELECTOR, "h3.fs-5 a").text.strip()
                enlace = card.find_element(By.CSS_SELECTOR, "h3.fs-5 a").get_attribute("href")
                empresa = card.find_element(By.CSS_SELECTOR, "a.text-primary.link-muted").text.strip()
                ofertas.append({
                    "Título": titulo,
                    "Empresa": empresa,
                    "Enlace": enlace
                })
            except Exception as e:
                print(f"⚠️ Error en una tarjeta: {e}")
                continue
        return ofertas

    except Exception as e:
        print(f"Error general: {e}")
        return []

    finally:
        driver.quit()
