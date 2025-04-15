import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import pyautogui
import time
import os

def obtener_titulares_vivienda():
    url = "https://elpais.com/noticias/vivienda/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = soup.find_all('h2')
    titulares = []
    for noticia in noticias:
        texto = noticia.get_text(strip=True)
        if 'vivienda' in texto.lower():
            titulares.append(texto)
        if len(titulares) >= 5:
            break
    return titulares

def abrir_word_y_pegar_titulares(titulares):
    # Abrir Word desde Spotlight
    pyautogui.hotkey('command', 'space')
    time.sleep(1)
    pyautogui.write('Word')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(5)

    # Pegar titulares
    for t in titulares:
        pyautogui.write(t)
        pyautogui.press('enter')
        time.sleep(0.2)

    # Guardar documento en escritorio
    pyautogui.hotkey('command', 'shift', 's')
    time.sleep(2)
    pyautogui.write('Noticias_Vivienda.docx')
    time.sleep(1)
    pyautogui.hotkey('command', 'shift', 'g')
    time.sleep(1)
    pyautogui.write('~/Desktop')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')

def abrir_word_solo():
    pyautogui.hotkey('command', 'space')
    time.sleep(1)
    pyautogui.write('Word')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(5)

def main():
    def ejecutar_opcion(opcion):
        ventana.destroy()
        if opcion == "noticias":
            titulares = obtener_titulares_vivienda()
            abrir_word_y_pegar_titulares(titulares)
        elif opcion == "word":
            abrir_word_solo()
        messagebox.showinfo("Finalizado", "Listo")

    # Interfaz
    ventana = tk.Tk()
    ventana.title("¿Qué deseas hacer?")
    ventana.geometry("300x120")

    etiqueta = tk.Label(ventana, text="¿Qué quieres hacer?")
    etiqueta.pack(pady=10)

    boton1 = tk.Button(ventana, text="Ver noticias sobre vivienda", command=lambda: ejecutar_opcion("noticias"))
    boton1.pack(pady=5)

    boton2 = tk.Button(ventana, text="Abrir Word", command=lambda: ejecutar_opcion("word"))
    boton2.pack(pady=5)

    ventana.mainloop()

if __name__ == "__main__":
    main()
