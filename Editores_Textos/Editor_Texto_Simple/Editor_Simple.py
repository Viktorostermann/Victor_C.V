import tkinter as tk
from tkinter import filedialog

# -------- CONFIGURACIÓN -------- #
palabras_clave = ["def", "class", "import", "from", "return", "if", "else", "elif", "for", "while"]

# -------- FUNCIONES -------- #

def nuevo():
    editor.delete("1.0", tk.END)

def abrir():
    archivo = filedialog.askopenfilename(filetypes=[("Python", "*.py"), ("Texto", "*.txt")])
    if archivo:
        with open(archivo, "r", encoding="utf-8") as f:
            editor.delete("1.0", tk.END)
            editor.insert("1.0", f.read())

def guardar():
    archivo = filedialog.asksaveasfilename(defaultextension=".py")
    if archivo:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(editor.get("1.0", tk.END))

# -------- RESALTADO DE SINTAXIS -------- #

def colorear(event=None):
    contenido = editor.get("1.0", tk.END)

    for tag in ["keyword", "string", "comment"]:
        editor.tag_remove(tag, "1.0", tk.END)

    # Palabras clave
    for palabra in palabras_clave:
        idx = "1.0"
        while True:
            idx = editor.search(palabra, idx, stopindex=tk.END)
            if not idx:
                break
            fin = f"{idx}+{len(palabra)}c"
            editor.tag_add("keyword", idx, fin)
            idx = fin

    # Strings
    idx = "1.0"
    while True:
        idx = editor.search('"', idx, stopindex=tk.END)
        if not idx:
            break
        fin = editor.search('"', f"{idx}+1c", stopindex=tk.END)
        if not fin:
            break
        editor.tag_add("string", idx, f"{fin}+1c")
        idx = f"{fin}+1c"

    # Comentarios
    idx = "1.0"
    while True:
        idx = editor.search("#", idx, stopindex=tk.END)
        if not idx:
            break
        fin = editor.search("\n", idx, stopindex=tk.END)
        editor.tag_add("comment", idx, fin)
        idx = fin

# -------- NUMERACIÓN DE LÍNEAS -------- #

def actualizar_lineas(event=None):
    lineas.delete("1.0", tk.END)
    total = editor.index("end-1c").split(".")[0]
    numeros = "\n".join(str(i) for i in range(1, int(total) + 1))
    lineas.insert("1.0", numeros)

# -------- AUTOINDENT -------- #

def auto_indent(event):
    linea = editor.get("insert linestart", "insert")
    espacios = len(linea) - len(linea.lstrip())
    editor.insert("insert", "\n" + " " * espacios)
    return "break"

# -------- AUTOCOMPLETADO -------- #

def autocompletar(event):
    palabra = editor.get("insert-3c", "insert")
    if palabra == "pri":
        editor.insert("insert", "nt()")
    return None

# -------- INTERFAZ -------- #

root = tk.Tk()
root.title("Mini VS Code")
root.geometry("900x600")
root.configure(bg="#1e1e1e")

# Frame principal
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Líneas
lineas = tk.Text(frame, width=4, bg="#2b2b2b", fg="gray", state="disabled")
lineas.pack(side=tk.LEFT, fill=tk.Y)

# Editor
editor = tk.Text(
    frame,
    bg="#1e1e1e",
    fg="white",
    insertbackground="white",
    font=("Consolas", 12),
    undo=True
)
editor.pack(fill=tk.BOTH, expand=True)

# Scroll
scroll = tk.Scrollbar(editor)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
editor.config(yscrollcommand=scroll.set)
scroll.config(command=editor.yview)

# -------- TAGS DE COLOR -------- #
editor.tag_config("keyword", foreground="#569cd6")
editor.tag_config("string", foreground="#ce9178")
editor.tag_config("comment", foreground="#6a9955")

# -------- EVENTOS -------- #
editor.bind("<KeyRelease>", lambda e: [colorear(), actualizar_lineas()])
editor.bind("<Return>", auto_indent)
editor.bind("<KeyRelease>", autocompletar)

# -------- MENÚ -------- #
menu = tk.Menu(root)
root.config(menu=menu)

archivo = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Archivo", menu=archivo)

archivo.add_command(label="Nuevo", command=nuevo)
archivo.add_command(label="Abrir", command=abrir)
archivo.add_command(label="Guardar", command=guardar)

# -------- INICIO -------- #
actualizar_lineas()
root.mainloop()