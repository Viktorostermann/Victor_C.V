import os
import sys
import subprocess
import webbrowser
import tkinter as tk
from tkinter import messagebox
import multiprocessing

def main():
    # Ruta hacia app.py
    script_path = os.path.join(os.path.dirname(__file__), "..", "app", "app.py")
    
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
    main()
