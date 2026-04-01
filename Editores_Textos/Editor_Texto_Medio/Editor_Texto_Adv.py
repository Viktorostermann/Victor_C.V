import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# -------- CREAR NUEVA PESTAÑA -------- #
def nueva_pestana():
    frame = tk.Frame(notebook)

    editor = tk.Text(
        frame,
        bg="#1e1e1e",
        fg="white",
        insertbackground="white",
        font=("Consolas", 12)
    )
    editor.pack(fill=tk.BOTH, expand=True)

    notebook.add(frame, text="nuevo.py")
    notebook.select(frame)

    return editor

# -------- OBTENER EDITOR ACTUAL -------- #
def obtener_editor():
    tab = notebook.select()
    frame = notebook.nametowidget(tab)
    return frame.winfo_children()[0]

# -------- CERRAR PESTAÑA -------- #
def cerrar_pestana():
    if len(notebook.tabs()) > 1:
        notebook.forget(notebook.select())
    else:
        messagebox.showwarning("Aviso", "No puedes cerrar la última pestaña")

# -------- CLICK DERECHO PARA CERRAR -------- #
def cerrar_pestana_click(event):
    try:
        index = notebook.index(f"@{event.x},{event.y}")
        if len(notebook.tabs()) > 1:
            notebook.forget(index)
    except:
        pass

# -------- EJECUTAR CÓDIGO -------- #
def ejecutar_codigo():
    editor = obtener_editor()
    codigo = editor.get("1.0", tk.END)

    consola.delete("1.0", tk.END)

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
            temp.write(codigo.encode("utf-8"))
            temp_path = temp.name

        resultado = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True
        )

        consola.insert(tk.END, resultado.stdout)
        consola.insert(tk.END, resultado.stderr)

    except Exception as e:
        consola.insert(tk.END, str(e))

# -------- EXPORTAR A PDF -------- #
def exportar_pdf():
    editor = obtener_editor()
    contenido = editor.get("1.0", tk.END)

    archivo = filedialog.asksaveasfilename(defaultextension=".pdf")
    if not archivo:
        return

    doc = SimpleDocTemplate(archivo, pagesize=letter)
    estilos = getSampleStyleSheet()

    texto = Paragraph(contenido.replace("\n", "<br/>"), estilos["Normal"])
    doc.build([texto])

    messagebox.showinfo("PDF", "Archivo exportado correctamente")

# -------- INTERFAZ -------- #
root = tk.Tk()
root.title("Mini IDE Pro")
root.geometry("1000x700")

# -------- TOOLBAR -------- #
toolbar = tk.Frame(root, bg="#2b2b2b")
toolbar.pack(fill=tk.X)

btn_nueva = tk.Button(
    toolbar, text="📄 Nueva",
    command=nueva_pestana,
    font=("Segoe UI", 11, "bold"),
    bg="#3c3f41", fg="white",
    padx=15, pady=5, relief=tk.FLAT
)
btn_nueva.pack(side=tk.LEFT, padx=5, pady=5)

btn_run = tk.Button(
    toolbar, text="▶ Ejecutar",
    command=ejecutar_codigo,
    font=("Segoe UI", 11, "bold"),
    bg="#007acc", fg="white",
    padx=15, pady=5, relief=tk.FLAT
)
btn_run.pack(side=tk.LEFT, padx=5, pady=5)

btn_pdf = tk.Button(
    toolbar, text="📄 Exportar PDF",
    command=exportar_pdf,
    font=("Segoe UI", 11, "bold"),
    bg="#6a9955", fg="white",
    padx=15, pady=5, relief=tk.FLAT
)
btn_pdf.pack(side=tk.LEFT, padx=5, pady=5)

btn_cerrar = tk.Button(
    toolbar, text="❌ Cerrar",
    command=cerrar_pestana,
    font=("Segoe UI", 11, "bold"),
    bg="#c74e39", fg="white",
    padx=15, pady=5, relief=tk.FLAT
)
btn_cerrar.pack(side=tk.LEFT, padx=5, pady=5)

# -------- CONTENEDOR PRINCIPAL -------- #
frame_principal = tk.Frame(root)
frame_principal.pack(fill=tk.BOTH, expand=True)

# -------- NOTEBOOK -------- #
notebook = ttk.Notebook(frame_principal)
notebook.pack(fill=tk.BOTH, expand=True)

notebook.bind("<Button-3>", cerrar_pestana_click)

editor = nueva_pestana()

# -------- CONSOLA -------- #
frame_consola = tk.Frame(root, bg="#1e1e1e")
frame_consola.pack(fill=tk.BOTH)

tk.Label(
    frame_consola,
    text="Consola",
    bg="#1e1e1e",
    fg="white",
    font=("Segoe UI", 10, "bold")
).pack(anchor="w", padx=5)

consola = tk.Text(
    frame_consola,
    height=10,
    bg="black",
    fg="lime",
    insertbackground="white",
    font=("Consolas", 11)
)
consola.pack(fill=tk.BOTH, expand=True)

# -------- MENÚ -------- #
menu = tk.Menu(root)
root.config(menu=menu)

archivo = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Archivo", menu=archivo)

archivo.add_command(label="Nueva pestaña", command=nueva_pestana)
archivo.add_command(label="Exportar a PDF", command=exportar_pdf)

ejecutar_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Ejecutar", menu=ejecutar_menu)

ejecutar_menu.add_command(label="Run", command=ejecutar_codigo)

# -------- LOOP -------- #
root.mainloop()