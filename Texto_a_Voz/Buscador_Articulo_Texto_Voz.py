# Proyecto 1: Buscador de Artículos y Conversión a Voz
# Descripción: Este proyecto permite a los usuarios buscar artículos en línea y convertirlos a formato de voz de audio reproducible en formato mp3. 
# Se puede hacer uso de bibliotecas existentes como  nltk (kit de herramientas de lenguaje natural), 
# newspaper3k, y gtts o utilizar la API de OpenAI. 
# El proyecto incluye una interfaz de usuario simple para ingresar términos de búsqueda y escuchar los resultados.

# Requerimientos:
# 1. Interfaz de Usuario: Crear una interfaz de usuario simple utilizando Tkinter o Streamlit para que los usuarios puedan ingresar términos de búsqueda.
# 2. Búsqueda de Artículos: Implementar una función que utilice la biblioteca newspaper3k para buscar artículos relacionados con los términos de búsqueda ingresados por el usuario.
# 3. Conversión a Voz: Utilizar gtts o la API de OpenAI para convertir el texto del artículo encontrado en un archivo de audio mp3.
# 4. Reproducción de Audio: Implementar una función para reproducir el archivo de audio mp3 generado.
# 5. Manejo de Errores: Asegurarse de manejar errores como la falta de resultados de búsqueda o problemas con la conversión a voz de manera adecuada, proporcionando retroalimentación al usuario.
# 6. Documentación: Incluir documentación clara sobre cómo usar la aplicación, así como comentarios en el código para explicar las funciones y la lógica implementada.
# 7. Pruebas: Realizar pruebas para asegurar que todas las funcionalidades estén funcionando correctamente, incluyendo casos de borde como términos de búsqueda sin resultados o artículos con contenido no convertible a voz.
# 8. Debe aplicarse los principios de responsabilidad SOLID para asegurar que el código sea modular, mantenible y fácil de entender.
# 9. Desarrollo inicialmente para SO Windows 11.

import sys, threading, queue, os
import sys
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import tkinter as tk
from tkinter import messagebox, Listbox
from tkinter import PhotoImage

from newspaper import Article
import newspaper

from gtts import gTTS
from langdetect import detect
import pygame

import requests
from bs4 import BeautifulSoup
from newspaper import build

import re
import time

# ----------------------------------------------------------------------------------------------------------------

# ⚙️ CONFIGURACIÓN GLOBAL DE NEWSPAPER
config_newspaper = newspaper.Config()
config_newspaper.request_timeout = 15  # ⏱️ Aumenta el tiempo de espera para conexiones lentas
config_newspaper.memoize_articles = False  # Evita cacheo innecesario

# ----------------------------------------------------------------------------------------------------------------

 # 📁 Detectar entorno compilado o fuente
RAIZ = Path(__file__).resolve().parent
BASE_DIR = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else RAIZ

# ----------------------------------------------------------------------------------------------------------------
# 📁 Rutas oficiales
RUTA_REPORTES = BASE_DIR / "Reportes"
RUTA_LOGS_GUI = RUTA_REPORTES / "Logs_GUI"
RUTA_HTML_POS = RUTA_REPORTES / "Reporte_HTML" / "Positivos"
RUTA_HTML_NEG = RUTA_REPORTES / "Reporte_HTML" / "Negativos"
RUTA_TXT_POS  = RUTA_REPORTES / "Reporte_TXT" / "Positivos"
RUTA_TXT_NEG  = RUTA_REPORTES / "Reporte_TXT" / "Negativos"
RUTA_AUDIOS   = RUTA_REPORTES / "Audios_URLS"
for ruta in [RUTA_LOGS_GUI, RUTA_HTML_POS, RUTA_HTML_NEG, RUTA_TXT_POS, RUTA_TXT_NEG, RUTA_AUDIOS]:
    ruta.mkdir(parents=True, exist_ok=True)
    
# ----------------------------------------------------------------------------------------------------------------

# 🎧 Inicializar pygame mixer
pygame.mixer.init()
# 🧱 Variables de estado
audio_path = None
audio_playing = False
audio_paused = False
cola_gui = queue.Queue()

# ----------------------------------------------------------------------------------------------------------------

# 🖼️ GUI principal
root = tk.Tk()
root.title("Verificador de Artículos")
root.configure(bg="black")
root.geometry("1000x700")
root.minsize(width=900, height=600)
root.resizable(True, True)

# ----------------------------------------------------------------------------------------------------------------

# 🔗 Entrada de URL
tk.Label(root, text="🔗 Ingrese una URL para verificar:", fg="white", bg="black", font=("Arial", 12)).pack(pady=10)
url_entry = tk.Entry(root, width=100)
url_entry.pack(pady=5)

# ----------------------------------------------------------------------------------------------------------------

# 🎛️ Botones inferiores (fuera de los paneles, siempre visibles)
boton_frame = tk.Frame(root, bg="black")
boton_frame.pack(side="bottom", fill="x", pady=10)

boton_interno = tk.Frame(boton_frame, bg="black")
boton_interno.pack(anchor="center")

btn_procesar   = tk.Button(boton_interno, text="🔍 Procesar URL", bg="#222", fg="white", font=("Arial", 10))
btn_reproducir = tk.Button(boton_interno, text="🔊 Reproducir Audio", bg="#222", fg="white", font=("Arial", 10))
btn_pausar     = tk.Button(boton_interno, text="⏸️ Pausar",       bg="#222", fg="white", font=("Arial", 10))
btn_reanudar   = tk.Button(boton_interno, text="▶ Reanudar",      bg="#222", fg="white", font=("Arial", 10))
btn_detener    = tk.Button(boton_interno, text="⏹️ Detener",      bg="#222", fg="white", font=("Arial", 10))

btn_procesar.grid(row=0, column=0, padx=10, pady=5)
btn_reproducir.grid(row=0, column=1, padx=10, pady=5)
btn_pausar.grid(row=0, column=2, padx=10, pady=5)
btn_reanudar.grid(row=0, column=3, padx=10, pady=5)
btn_detener.grid(row=0, column=4, padx=10, pady=5)


# ----------------------------------------------------------------------------------------------------------------

# 🧩 PanedWindow horizontal Superior 
horizontal_pane = tk.PanedWindow(root, orient="horizontal", sashwidth=6, bg="black", bd=0, sashrelief="raised")
horizontal_pane.pack(fill="both", expand=True, padx=10, pady=(10, 0))
tk.Label(horizontal_pane, text="🗂️ Texto ubicado", fg="white", bg="#1a1a1a", font=("Arial", 11)).pack(pady=10)

# ----------------------------------------------------------------------------------------------------------------

# 📌 Panel izquierdo
panel_izquierdo = tk.Frame(horizontal_pane, bg="#1a1a1a", width=250)
horizontal_pane.add(panel_izquierdo, stretch="always")
tk.Label(panel_izquierdo, text="🗂️ Historial de Consultas", fg="white", bg="#1a1a1a", font=("Arial", 11)).pack(pady=10)
historial_urls = Listbox(panel_izquierdo, bg="#222", fg="white", font=("Courier", 10), height=20)
historial_urls.pack(fill="both", expand=True, padx=10)

# ----------------------------------------------------------------------------------------------------------------

# 📌 Panel horizontal inferior
vertical_pane = tk.PanedWindow(horizontal_pane, orient="vertical", sashwidth=6, bg="black", bd=0, sashrelief="raised")
horizontal_pane.add(vertical_pane, stretch="always")

# ----------------------------------------------------------------------------------------------------------------

# 📄 Texto del artículo
text_frame = tk.Frame(vertical_pane, bg="black")
scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")
text_display = tk.Text(text_frame, wrap="word", yscrollcommand=scrollbar.set, bg="#111", fg="#eee", insertbackground="white",
                       relief="flat", bd=0, highlightthickness=2, highlightbackground="#444", highlightcolor="#3399ff",
                       font=("Courier", 10), state="disabled")
text_display.pack(fill="both", expand=True)
scrollbar.config(command=text_display.yview)
vertical_pane.add(text_frame, stretch="always")

# ----------------------------------------------------------------------------------------------------------------

# 📊 Reporte/log comienza aqui 
reporte_frame = tk.Frame(vertical_pane, bg="black")
reporte_scroll = tk.Scrollbar(reporte_frame)
reporte_scroll.pack(side="right", fill="y")
reporte_display = tk.Text(reporte_frame, wrap="word", yscrollcommand=reporte_scroll.set, bg="black", fg="white",
                          font=("Courier", 10), height=10)
reporte_display.pack(fill="both", expand=True)
reporte_scroll.config(command=reporte_display.yview)
vertical_pane.add(reporte_frame, stretch="always")
# 📊 Reporte/log termina aqui

# ----------------------------------------------------------------------------------------------------------------

# 🧠 Utilidades comienza aqui 
def generar_nombre_reporte(prefijo, url):
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    dominio = urlparse(url).netloc.replace(".", "_") or "sin_dominio"
    return f"{prefijo}_{dominio}_{fecha}"

# ----------------------------------------------------------------------------------------------------------------

def guardar_html(nombre_base, contenido, extension, carpeta: Path):
    ruta = carpeta / f"{nombre_base}{extension}"
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
    except Exception as e:
        print(f"[ERROR] No se pudo guardar HTML: {e}")
    return ruta

# ----------------------------------------------------------------------------------------------------------------

def guardar_log_evento_gui(evento: str):
    nombre_base = f"log_gui_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    contenido = f"""<html><head><meta charset="utf-8"><title>Log GUI</title></head>
<body style="background-color:#111;color:#eee;font-family:Courier;padding:20px;">
<pre>{evento}</pre>
<hr><div style="color:#aaa;font-size:12px;">
🕒 Evento registrado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
📁 Guardado en: {RUTA_LOGS_GUI}<br>
🔧 Script: {Path(__file__).name}
</div></body></html>"""
    guardar_html(nombre_base, contenido, ".html", RUTA_LOGS_GUI)

# ----------------------------------------------------------------------------------------------------------------

def agregar_url_historial(url, estado):
    color = "green" if estado == "ok" else "red"
    historial_urls.insert("end", url)
    historial_urls.itemconfig("end", {'fg': color})

# ----------------------------------------------------------------------------------------------------------------

def registrar_consulta_en_log(url, estado):
    nombre_archivo = RUTA_LOGS_GUI / "historial_consultas.html"
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = "#00cc00" if estado == "ok" else "#cc0000"
    icono = "✅" if estado == "ok" else "❌"
    entrada = f"""<div style="margin-bottom:8px;">
  <span style="color:{color}; font-weight:bold;">{icono}</span>
  <span style="color:{color};">{url}</span>
  <span style="color:#aaa;">🕒 {fecha_hora}</span>
</div>"""
    if not nombre_archivo.exists():
        contenido_inicial = f"""<html><head><meta charset="utf-8"><title>Historial de Consultas</title></head>
<body style="background-color:#111;color:#eee;font-family:Courier;padding:20px;">
<h2>📜 Historial de URLs consultadas</h2>
{entrada}</body></html>"""
        nombre_archivo.write_text(contenido_inicial, encoding="utf-8")
    else:
        contenido = nombre_archivo.read_text(encoding="utf-8")
        contenido = contenido.replace("</body></html>", entrada + "\n</body></html>")
        nombre_archivo.write_text(contenido, encoding="utf-8")

# 🧠 Utilidades Termina aqui

# ----------------------------------------------------------------------------------------------------------------

# 🔁 Cola y reproducción (no bloqueante) Comienza aqui.
def pump_queue():
    try:
        while True:
            tipo, payload = cola_gui.get_nowait()
            if tipo == "texto":
                text_display.config(state="normal")
                text_display.delete("1.0", "end")
                text_display.insert("end", payload)
                text_display.config(state="disabled")
            elif tipo == "log":
                reporte_display.insert("end", payload + "\n")
                reporte_display.see("end")
            elif tipo == "audio":
                if payload and Path(payload).exists():
                    start_playback(payload)
                else:
                    cola_gui.put(("log", f"\n[ERROR] Ruta de audio inválida o no existe: {payload}\n"))
    except queue.Empty:
        pass
    root.after(50, pump_queue)

'''def start_playback(mp3_path):
    global audio_playing, audio_paused, audio_path
    audio_path = mp3_path
    audio_paused = False
    if not Path(mp3_path).exists():
        cola_gui.put(("log", f"\n🔍 [ERROR] El archivo de audio no fue creado: {mp3_path}\n"))
        return
    try:
        pygame.mixer.music.load(mp3_path)
        pygame.mixer.music.play()
        audio_playing = True
        check_busy()
    except Exception as e:
        cola_gui.put(("log", f"\n🔍 [ERROR] al reproducir audio: {e}\n"))

cola_gui.put(("log", f"\n✅ Reproducción finalizada.\n"))'''

def start_playback(mp3_path):
    global audio_playing, audio_paused, audio_path
    audio_path = mp3_path
    audio_paused = False

    mp3_file = Path(mp3_path)
    if not mp3_file.exists():
        cola_gui.put(("log", f"\n🔍 [ERROR] El archivo de audio no fue creado: {mp3_path}\n"))
        return

    try:
        pygame.mixer.music.load(str(mp3_file.resolve()))
        pygame.mixer.music.play()
        audio_playing = True

        # Hilo que espera a que termine la reproducción
        def _monitor_playback():
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            cola_gui.put(("log", "\n✅ Reproducción finalizada.\n"))
            # marcamos que ya no está reproduciéndose
            global audio_playing
            audio_playing = False

        threading.Thread(target=_monitor_playback, daemon=True).start()

    except Exception as e:
        cola_gui.put(("log", f"\n🔍 [ERROR] al reproducir audio: {e}\n"))


def check_busy():
    global audio_playing
    if audio_paused:
        root.after(200, check_busy)
        return
    if pygame.mixer.music.get_busy():
        root.after(200, check_busy)
    else:
        audio_playing = False
        cola_gui.put(("log", f"\n✅ Reproducción finalizada.\n"))

def pausar_audio():
    global audio_paused
    if audio_playing and not audio_paused:
        try:
            pygame.mixer.music.pause()
            audio_paused = True
            cola_gui.put(("log", "⏸️ Pausado"))
        except Exception as e:
            cola_gui.put(("log", f"[ERROR] al pausar: {e}"))

def reanudar_audio():
    global audio_paused, audio_playing
    if audio_paused:
        try:
            pygame.mixer.music.unpause()
            audio_paused = False
            audio_playing = True
            cola_gui.put(("log", "▶ Reanudado"))
            check_busy()
        except Exception as e:
            cola_gui.put(("log", f"[ERROR] al reanudar: {e}"))

def detener_audio():
    global audio_playing, audio_paused
    try:
        pygame.mixer.music.stop()
    finally:
        audio_playing = False
        audio_paused = False
        cola_gui.put(("log", "⏹️ Detenido"))

ultima_url_procesada = None  # ← asegúrate de tener esto definido al inicio del script

def reproducir_audio_actual():
    global ultima_ruta_audio
    if not ultima_ruta_audio:
        cola_gui.put(("log", "\n[ERROR] No hay audio para reproducir. Procesa una URL primero.\n"))
        return

    if not Path(ultima_ruta_audio).exists():
        cola_gui.put(("log", f"\n[ERROR] El audio no existe: {ultima_ruta_audio}\n"))
        return

    start_playback(str(ultima_ruta_audio))

# 🔁 Cola y reproducción (no bloqueante) Termina aqui

# ----------------------------------------------------------------------------------------------------------------

# ✅ Validacion de la URL Comienza aqui #
def url_valida(url):
    try:
        r = requests.get(url, timeout=10)
        return r.status_code == 200 and "html" in r.headers.get("Content-Type", "")
    except Exception:
        return False

PATRON_ARTICULO = re.compile(
    r"(/a/[^/]+_\d+/?$)|(_\d+/?$)", re.IGNORECASE
)
# Ejemplos válidos:
# https://historia.nationalgeographic.com.es/a/fascinante-historia-descubrimiento-tumba-joyas-princesa-iran_17326
# https://historia.nationalgeographic.com.es/a/ciudades-antiguas-mas-interesantes-fantasia-lugares-historia_14641
# ...y otros que terminan en _12345

def es_seccion(url: str) -> bool:
    # Si matchea patrón de artículo, NO es sección
    if PATRON_ARTICULO.search(url):
        return False
    # Si termina en slash o no tiene patrón de artículo, tratamos como sección
    return url.endswith("/")

# ----------------------------------------------------------------------------------------------------------------
def explorar_articulos_con_newspaper(seccion_url):
    try:
        sitio = build(seccion_url, memoize_articles=False)
        urls = [normalizar_url(art.url) for art in sitio.articles if PATRON_ARTICULO.search(art.url or "")]
        # quita duplicados
        vistos, filtrados = set(), []
        for u in urls:
            if u not in vistos:
                vistos.add(u)
                filtrados.append(u)
        return filtrados
    except Exception as e:
        cola_gui.put(("log", f"\n🔍 [ERROR] al explorar sección con newspaper: {e}\n"))
        return []


def explorar_articulos_con_bs4(seccion_url):
    try:
        html = requests.get(seccion_url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        enlaces = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            # normaliza a URL absoluta
            if href.startswith("/"):
                href = f"{urlparse(seccion_url).scheme}://{urlparse(seccion_url).netloc}{href}"
            # filtra solo artículos
            if PATRON_ARTICULO.search(href):
                enlaces.append(normalizar_url(href))
        # elimina duplicados preservando orden
        vistos, filtrados = set(), []
        for h in enlaces:
            if h not in vistos:
                vistos.add(h)
                filtrados.append(h)
        return filtrados
    except Exception as e:
        cola_gui.put(("log", f"\n🔍 [ERROR] al explorar sección con BeautifulSoup: {e}\n"))
        return []

# ✅ Validacion de la URL Termina aqui #

# ----------------------------------------------------------------------------------------------------------------

# 🧵 Procesamiento en hilos

IDIOMAS_SOPORTADOS = {"es", "en", "pt", "fr", "de", "it"}
def procesar_url_en_hilo(url: str):
    def worker():
        if not url_valida(url):
            cola_gui.put(("log", f"\n🔍 [ERROR] La URL no es válida o no existe: {url}\n"))
            agregar_url_historial(url, "error")
            registrar_consulta_en_log(url, "error")
            return

        if es_seccion(url):
            cola_gui.put(("log", f"\n📂 Detectada sección: {url}\n"))

            urls_detectadas = explorar_articulos_con_newspaper(url)
            if not urls_detectadas:
                urls_detectadas = explorar_articulos_con_bs4(url)

            if not urls_detectadas:
                cola_gui.put(("log", f"\n🔍 [ERROR] No se encontraron artículos en la sección: {url}\n"))
                agregar_url_historial(url, "error")
                registrar_consulta_en_log(url, "error")
                return

            cola_gui.put(("log", f"\n🔗 Artículos encontrados en sección: {len(urls_detectadas)}\n"))
            for u in urls_detectadas[:5]:
                cola_gui.put(("log", f"→ {u}\n"))
            return

        try:
            cola_gui.put(("log", f"\n🔍 Procesando: {url}\n"))
            art = Article(url, config=config_newspaper)
            art.download()
            art.parse()
            texto = (art.text or "").strip()
            cola_gui.put(("log", f"[DEBUG] Longitud del texto extraído: {len(texto)}\n"))

            if not texto:
                raise ValueError("No se pudo extraer texto del artículo.")
            cola_gui.put(("texto", texto))

            try:
                lang = detect(texto)
            except Exception:
                lang = "es"
            if lang not in IDIOMAS_SOPORTADOS:
                cola_gui.put(("log", f"🌐 Idioma '{lang}' no soportado por gTTS. Usando 'es'.\n"))
                lang = "es"

            nombre = generar_nombre_reporte("articulo", url)
            mp3_path = RUTA_AUDIOS / f"{nombre}.mp3"

            try:
                gTTS(text=texto, lang=lang).save(str(mp3_path))
            except Exception as e:
                cola_gui.put(("log", f"\n[ERROR] al generar audio: {e}\n"))
                return
        
            if not mp3_path.exists():
                cola_gui.put(("log", f"\n[ERROR] El archivo de audio no fue creado: {mp3_path}\n"))
                return

# ------------------------------------------------------------------------------------------------------------------------------------------
            # 🔽 Codigo nuevo para reproducir audio Fecha modificacion 2025-09-08
            
            cola_gui.put(("log", f"▶️ Reproduciendo audio...\n"))
            cola_gui.put(("log", f"🔗 Archivo de audio: {mp3_path}\n"))
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(str(mp3_path))
                pygame.mixer.music.play()
                cola_gui.put(("log", f"▶️ Reproducción iniciada correctamente.\n"))
            except Exception as e:
                cola_gui.put(("log", f"\n[ERROR] El audio no pudo reproducirse, fallo en el archivo origen: {e}\n"))
                cola_gui.put(("log", f"💡 Verifica que el dispositivo de audio esté disponible y que el archivo no esté corrupto.\n"))
                cola_gui.put(("log", f"\n[ERROR] El audio no pudo reproducirse, fallo en el archivo origen: {e}\n"))
# ------------------------------------------------------------------------------------------------------------------------------------------

            global ultima_url_procesada, ultima_ruta_audio
            ultima_url_procesada = url
            ultima_ruta_audio = mp3_path

            cola_gui.put(("audio", str(mp3_path)))
            cola_gui.put(("log", f"🔊 Audio generado: {mp3_path}\n"))

            agregar_url_historial(url, "ok")
            registrar_consulta_en_log(url, "ok")

        except Exception as e:
            cola_gui.put(("log", f"\n[ERROR] {e}\n"))
            agregar_url_historial(url, "error")
            registrar_consulta_en_log(url, "error")


    threading.Thread(target=worker, daemon=True).start()

def on_historial_doble_click(event):
    sel = historial_urls.curselection()
    if sel:
        url = historial_urls.get(sel[0])
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)
        on_procesar()

historial_urls.bind("<Double-Button-1>", on_historial_doble_click)

# 🎛️ Handlers de botones
def normalizar_url(url: str) -> str:
    # Limpia espacios, fragmentos y barra final
    url = url.strip()
    url = url.split("#", 1)[0]
    return url.rstrip("/")

def on_procesar():
    url = normalizar_url(url_entry.get())
    if not url:
        messagebox.showwarning("URL vacía", "Por favor, ingresa una URL.")
        return
    if audio_playing and not audio_paused:
        detener_audio()
    procesar_url_en_hilo(url)


btn_procesar.config(command=on_procesar)
btn_reproducir.config(command=reproducir_audio_actual)
btn_pausar.config(command=pausar_audio)
btn_reanudar.config(command=reanudar_audio)
btn_detener.config(command=detener_audio)

# 🧹 Cierre limpio
def on_close():
    try:
        detener_audio()
        pygame.mixer.quit()
    except Exception:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.after(50, pump_queue)

while not cola_gui.empty():
    cola_gui.get()

root.mainloop()

''' 
1 - Artículo sobre APIs de texto a voz en Unite.AI:  
https://www.unite.ai/es/Las-mejores-API-de-conversi%C3%B3n-de-texto-a-voz/

2- Guía de los mejores sitios TTS en Mango Animate: 
https://mangoanimate.com/blog/es/sitios-web-de-texto-a-voz/

3- Ranking de generadores de voz IA en Cyberlink: 
https://es.cyberlink.com/blog/edicion-de-audio/3049/convertir-texto-a-voz

4- Wikipedia: Historia de la inteligencia artificial: 
https://es.wikipedia.org/wiki/Historia_de_la_inteligencia_artificial

5- BBC Mundo: ¿Qué es la inteligencia artificial?:
https://www.bbc.com/mundo/noticias-51218742

6- El País: Cómo la IA está transformando el trabajo:
https://elpais.com/tecnologia/2023-11-15/como-la-inteligencia-artificial-esta-transformando-el-trabajo.html

7- Xataka: Guía de modelos de lenguaje:
https://www.xataka.com/inteligencia-artificial/que-son-modelos-lenguaje-como-funcionan-por-que-son-clave-inteligencia-artificial

8- MIT Technology Review en español:
https://www.technologyreview.es/

9- Medium: Productividad con inteligencia artificial:
https://medium.com/@danielgomez/productividad-con-inteligencia-artificial-2025-estrategias-clave-para-equipos-h%C3%ADbridos-4f3e9a2b9e2a

10- National Geographic: Cómo funciona el cerebro humano:
https://www.nationalgeographic.com.es/ciencia/como-funciona-cerebro-humano_19234

'''