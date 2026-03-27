import os
import sys
import subprocess
import webbrowser
import tkinter as tk
from tkinter import messagebox
import multiprocessing
import time

def main():
    if os.environ.get("POKEDEX_GUI_STARTED") == "1":
        return
    os.environ["POKEDEX_GUI_STARTED"] = "1"

    # Detecta si está corriendo desde el .exe o desde código fuente
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)

    # Ruta hacia app.py
    script_path = os.path.join(base_path, "app", "app.py")

    # Ruta fija al intérprete de Python real
    python_path = r"C:\Proyectos\Project_Manager\.venv\Scripts\python.exe"

    # Lanza Streamlit usando ese Python
    subprocess.Popen([
        python_path,
        "-m", "streamlit", "run",
        script_path,
        "--server.runOnSave=false",
        "--server.headless=true"
    ], stdout=sys.stdout, stderr=sys.stderr)


    # 🔹 Espera unos segundos para que el servidor arranque
    time.sleep(3)

    url = "http://localhost:8501"

    # Interfaz Tkinter
    root = tk.Tk()
    root.title("Pokédex Personal")
    root.geometry("400x200")

    # Icono Pokéball
    icon_path = os.path.join(base_path, "icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

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
    multiprocessing.freeze_support()
    main()






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
