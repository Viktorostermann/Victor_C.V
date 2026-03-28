import time
import random
from tkinter import *
from tkinter import ttk

frases = [
    "python es poderoso",
    "la practica hace al maestro",
    "escribe rapido y sin errores"
]

# Variables
frase_actual = ""
inicio_tiempo = 0
escribiendo = False
errores = 0

def nueva_frase():
    global frase_actual, inicio_tiempo, escribiendo, errores

    frase_actual = random.choice(frases)
    texto_objetivo.config(state=NORMAL)
    texto_objetivo.delete("1.0", END)
    texto_objetivo.insert("1.0", frase_actual)
    texto_objetivo.config(state=DISABLED)

    campo.delete("1.0", END)

    inicio_tiempo = 0
    escribiendo = False
    errores = 0

    resultado.config(text="")
    wpm_label.config(text="WPM: 0")

def al_escribir(event):
    global inicio_tiempo, escribiendo, errores

    texto_usuario = campo.get("1.0", END).strip()

    # iniciar automáticamente
    if not escribiendo and len(texto_usuario) == 1:
        inicio_tiempo = time.time()
        escribiendo = True

    # comparar texto
    texto_objetivo.config(state=NORMAL)
    texto_objetivo.delete("1.0", END)

    errores = 0

    for i, char in enumerate(frase_actual):
        if i < len(texto_usuario):
            if texto_usuario[i] == char:
                texto_objetivo.insert(END, char, "correcto")
            else:
                texto_objetivo.insert(END, char, "error")
                errores += 1
        else:
            texto_objetivo.insert(END, char)

    texto_objetivo.config(state=DISABLED)

    # calcular WPM
    if escribiendo:
        tiempo = time.time() - inicio_tiempo
        palabras = len(texto_usuario.split())
        wpm = int((palabras / tiempo) * 60) if tiempo > 0 else 0
        wpm_label.config(text=f"WPM: {wpm}")

    # finalizar automáticamente
    if texto_usuario == frase_actual:
        fin = time.time()
        total = round(fin - inicio_tiempo, 2)

        resultado.config(
            text=f"Tiempo: {total}s | WPM: {wpm} | Errores: {errores}"
        )

def main():
    global campo, texto_objetivo, resultado, wpm_label

    root = Tk()
    root.title("Mini MonkeyType")
    root.geometry("700x400")

    # Texto objetivo (con colores)
    texto_objetivo = Text(root, height=3, font=("Arial", 14))
    texto_objetivo.pack(fill=X, padx=10, pady=10)

    texto_objetivo.tag_config("correcto", foreground="green")
    texto_objetivo.tag_config("error", foreground="red")

    # Campo de escritura
    campo = Text(root, height=3, font=("Arial", 14))
    campo.pack(fill=X, padx=10)
    campo.bind("<KeyRelease>", al_escribir)

    # WPM en vivo
    wpm_label = Label(root, text="WPM: 0", font=("Arial", 12))
    wpm_label.pack(pady=5)

    # Resultado final
    resultado = Label(root, text="", font=("Arial", 12))
    resultado.pack(pady=10)

    # Botón nueva frase
    Button(root, text="Nueva frase", command=nueva_frase).pack()

    nueva_frase()
    campo.focus_set()

    root.mainloop()

main()