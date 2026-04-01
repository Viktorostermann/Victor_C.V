import os
import sys
import webbrowser
import tkinter as tk
from tkinter import simpledialog, messagebox
import multiprocessing
import time
import socket
import urllib.request
import subprocess


def get_free_ports(ports):
    """Devuelve una lista de puertos libres de una lista dada."""
    free = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                free.append(port)
    return free

def elegir_puerto():
    # 🔹 Incluye 8080 además de 8051–8053
    ports_to_check = [8051, 8052, 8053, 8080]
    available = get_free_ports(ports_to_check)

    if not available:
        messagebox.showerror("Error", "❌ No hay puertos libres en la lista.")
        return None, None

    # Preguntar al usuario cuál usar
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    chosen_port = simpledialog.askinteger(
        "Seleccionar puerto",
        f"Puertos disponibles: {available}\n\nElige uno:",
        initialvalue=available[0]
    )
    root.destroy()

    if chosen_port not in available:
        chosen_port = available[0]

    url = f"http://localhost:{chosen_port}"
    messagebox.showinfo("Pokédex Personal", f"✅ Se usará el puerto {chosen_port}\nURL: {url}")
    return chosen_port, url

# Ejemplo de uso
puerto, url = elegir_puerto()
if puerto:
    print(f"Servidor se levantará en {url}")


''' 
# 🔹 Esta versión antigua ya no se usa
def get_free_port(start=8501, max_attempts=20):
    """Busca un puerto libre empezando en 'start'."""
    for port in range(start, start + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
    return None
'''

def lanzar_streamlit(script_path, puerto):
    """Lanza Streamlit en el puerto indicado."""
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", script_path, "--server.port", str(puerto)])

def esperar_servidor(url, intentos=15):
    """Espera hasta que el servidor responda antes de abrir navegador."""
    for _ in range(intentos):
        try:
            with urllib.request.urlopen(url):
                return True
        except:
            time.sleep(1)
    return False

def main():
    if os.environ.get("POKEDEX_GUI_STARTED") == "1":
        return
    os.environ["POKEDEX_GUI_STARTED"] = "1"

    # Ruta dinámica al app.py dentro de la carpeta instalada
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)
    script_path = os.path.join(base_path, "app", "app.py")

    # 🔹 Usar la función elegir_puerto()
    puerto, url = elegir_puerto()
    if not puerto:
        return

    # 🔹 Lanza Streamlit en un proceso separado
    multiprocessing.Process(target=lanzar_streamlit, args=(script_path, puerto)).start()

    # 🔹 Espera activa antes de abrir navegador
    if esperar_servidor(url):
        webbrowser.open_new(url)
    else:
        messagebox.showerror("Pokédex Personal", "❌ El servidor no respondió. Revisa el log.")

    # ------------------ GUI Tkinter ----------------- #
    root = tk.Tk()
    root.title("Pokédex Personal")
    root.geometry("400x200")

    label = tk.Label(root, text=f"✅ Servidor iniciado en:\n{url}\n\nElige una opción:", font=("Arial", 12))
    label.pack(pady=20)

    def abrir():
        webbrowser.open_new(url)

    def copiar():
        root.clipboard_clear()
        root.clipboard_append(url)
        root.update()
        messagebox.showinfo("Pokédex Personal", "📋 La URL se copió al portapapeles.")

    def salir():
        root.destroy()

    tk.Button(root, text="Abrir Pokédex", command=abrir,
          width=20, bg="lightgreen", activebackground="green", activeforeground="white").pack(pady=5)

    tk.Button(root, text="Copiar URL", command=copiar,
            width=20, bg="lightblue", activebackground="blue", activeforeground="white").pack(pady=5)

    tk.Button(root, text="Salir", command=salir,
            width=20, bg="lightcoral", activebackground="red", activeforeground="white").pack(pady=5)

    root.mainloop()


# --------------------------------- Launcher actual (2026-03-29) --------------------------------- #
'''import os
import sys
import subprocess
import webbrowser
import tkinter as tk
from tkinter import messagebox
import multiprocessing
import time
import socket
import traceback

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    # 🔥 Subimos un nivel desde launcher/
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def wait_for_server(host="localhost", port=8501, timeout=60):
    """Espera hasta que el servidor Streamlit esté disponible."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=2):
                return True
        except OSError:
            time.sleep(1)
    return False

def main():
    if os.environ.get("POKEDEX_GUI_STARTED") == "1":
        return
    os.environ["POKEDEX_GUI_STARTED"] = "1"

    base_path = get_base_path()
    script_path = os.path.join(base_path, "app", "app.py")

    try:
        # 🔹 Lanzar Streamlit
        subprocess.Popen([sys.executable, "-m", "streamlit", "run", script_path])

        # 🔹 Esperar hasta 60 segundos
        if not wait_for_server(timeout=60):
            raise RuntimeError("Streamlit server no respondió en el tiempo esperado")

        url = "http://localhost:8501"
        webbrowser.open(url)

        # 🔹 GUI
        root = tk.Tk()
        root.title("Pokédex Personal")
        root.geometry("400x200")

        icon_path = os.path.join(base_path, "icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)

        label = tk.Label(
            root,
            text=f"✅ Servidor iniciado en:\n{url}\n\nElige una opción:",
            font=("Arial", 12)
        )
        label.pack(pady=20)

        def abrir():
            webbrowser.open_new(url)

        def copiar():
            root.clipboard_clear()
            root.clipboard_append(url)
            root.update()
            messagebox.showinfo("Pokédex Personal", "📋 URL copiada")

        def salir():
            root.destroy()

        tk.Button(root, text="Abrir Pokédex", command=abrir, width=20, bg="lightgreen").pack(pady=5)
        tk.Button(root, text="Copiar URL", command=copiar, width=20, bg="lightblue").pack(pady=5)
        tk.Button(root, text="Salir", command=salir, width=20, bg="lightcoral").pack(pady=5)

        root.mainloop()

    except Exception as e:
        traceback.print_exc()
        input("Presiona Enter para salir...")
        messagebox.showerror("Error", f"Streamlit no inició correctamente:\n{e}")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()'''

# --------------------------------- Launcher anterior al actual (2026-03-28) --------------------------------- #

# Launcher anterior al actual (2023-01-07)
'''import os
import sys
import subprocess
import webbrowser
import tkinter as tk
from tkinter import messagebox
import multiprocessing

def main():
    # Evita múltiples ventanas: solo crea la interfaz si no existe la bandera
    if os.environ.get("POKEDEX_GUI_STARTED") == "1":
        return
    os.environ["POKEDEX_GUI_STARTED"] = "1"

    # Detecta si está corriendo desde el .exe (PyInstaller) o desde código fuente
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)   # cuando corres el .exe
    else:
        base_path = os.path.dirname(__file__)         # cuando corres en desarrollo

    # Ruta hacia app.py
    script_path = os.path.join(base_path, "app", "app.py")

    # Lanza Streamlit en segundo plano sin abrir navegador automáticamente
    subprocess.Popen([
        sys.executable,
        "-m", "streamlit", "run",
        script_path,
        "--server.runOnSave=false",
        "--server.headless=true"
    ])

    # URL de la Pokédex
    url = "http://localhost:8501"

    # Interfaz Tkinter
    root = tk.Tk()
    root.title("Pokédex Personal")
    root.geometry("400x200")

    label = tk.Label(root, text=f"✅ Servidor iniciado en:\n{url}\n\nElige una opción:", font=("Arial", 12))
    label.pack(pady=20)

    def abrir():
        webbrowser.open_new(url)

    def copiar():
        root.clipboard_clear()
        root.clipboard_append(url)
        root.update()
        messagebox.showinfo("Pokédex Personal", "📋 La URL se copió al portapapeles.")

    def salir():
        root.destroy()

    tk.Button(root, text="Abrir Pokédex", command=abrir, width=20, bg="lightgreen").pack(pady=5)
    tk.Button(root, text="Copiar URL", command=copiar, width=20, bg="lightblue").pack(pady=5)
    tk.Button(root, text="Salir", command=salir, width=20, bg="lightcoral").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    multiprocessing.freeze_support()  # <- evita múltiples ventanas al compilar con PyInstaller
    main()'''
