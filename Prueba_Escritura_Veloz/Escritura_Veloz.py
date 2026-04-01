
'''Desarrollo de Programa con interfaz grafica para Probar la velocidad de escritura en el teclado,
para determinar cuan rapido escribe una oracion de manera precisa. Que registre el avance en el teclado 
y el tiempo que tarda en escribirla correctamente.'''

import time
import random
from tkinter import *
from tkinter import ttk

frases = [
    "python es poderoso",
    "la practica hace al maestro",
    "escribe rapido y sin errores"
]

# Variables globales
inicio_tiempo = 0
frase_actual = ""

# NUEVAS métricas
conteo_borrados = 0
tiempo_pausa = 0
ultimo_tecleo = 0

def iniciar():
    global inicio_tiempo, frase_actual, conteo_borrados, tiempo_pausa, ultimo_tecleo
    frase_actual = random.choice(frases)
    etiqueta_frase.config(text=frase_actual)
    inicio_tiempo = time.time()
    campo1.delete("1.0", END)

    conteo_borrados = 0
    tiempo_pausa = 0
    ultimo_tecleo = 0

    btn_iniciar.config(state=DISABLED)
    btn_finalizar.config(state=NORMAL)
    campo1.focus_set()

def finalizar():
    global conteo_borrados, tiempo_pausa

    fin = time.time()
    texto_usuario = campo1.get("1.0", END).strip()

    for row in tabla.get_children():
        tabla.delete(row)

    if texto_usuario == frase_actual:
        tiempo_total = round(fin - inicio_tiempo, 2)
        resultado.config(text=f"Tiempo: {tiempo_total} segundos")

        tabla.insert("", "end", values=("Tiempo total", tiempo_total))
        tabla.insert("", "end", values=("Correcciones", conteo_borrados))
        tabla.insert("", "end", values=("Tiempo en pausas", round(tiempo_pausa, 2)))

        tiempo_efectivo = tiempo_total - tiempo_pausa
        tabla.insert("", "end", values=("Tiempo efectivo", round(tiempo_efectivo, 2)))
    else:
        resultado.config(text="Error en la escritura")

    btn_iniciar.config(state=NORMAL)
    btn_finalizar.config(state=DISABLED)
    btn_iniciar.focus_set()

# 🔥 LIMPIAR TODO
def limpiar():
    global conteo_borrados, tiempo_pausa, ultimo_tecleo, inicio_tiempo, frase_actual

    campo1.delete("1.0", END)
    etiqueta_frase.config(text="")
    resultado.config(text="")

    for row in tabla.get_children():
        tabla.delete(row)

    conteo_borrados = 0
    tiempo_pausa = 0
    ultimo_tecleo = 0
    inicio_tiempo = 0
    frase_actual = ""

    btn_iniciar.config(state=NORMAL) # 
    btn_finalizar.config(state=NORMAL) # 🔥 cambiar a DISABLED
    btn_iniciar.focus_set()

def detectar_teclas(event):
    global conteo_borrados, ultimo_tecleo, tiempo_pausa

    ahora = time.time()

    if ultimo_tecleo != 0:
        pausa = ahora - ultimo_tecleo
        if pausa > 1.5:
            tiempo_pausa += pausa

    ultimo_tecleo = ahora

    if event.keysym == "BackSpace":
        conteo_borrados += 1

# 🔥 CONTROL DE TAB (clave)
def cambiar_foco(event):
    btn_finalizar.focus_set()
    return "break"

def main():
    global campo1, etiqueta_frase, resultado, tabla, btn_iniciar, btn_finalizar

    root = Tk()
    root.title("Test de Escritura")
    root.geometry("600x500")

    # -------- Layout adaptable -------- #
    frame_superior = Frame(root)
    frame_superior.pack(fill=X, padx=10, pady=5)

    frame_medio = Frame(root)
    frame_medio.pack(fill=BOTH, expand=True, padx=10)

    frame_botones = Frame(root)
    frame_botones.pack(pady=5)

    frame_inferior = Frame(root)
    frame_inferior.pack(fill=BOTH, expand=True, padx=10, pady=5)

    # -------- Parte superior -------- #
    Label(frame_superior, text="Presiona iniciar").pack()

    etiqueta_frase = Label(frame_superior, text="", font=("Arial", 12))
    etiqueta_frase.pack()

    # -------- Campo de texto -------- #
    campo1 = Text(frame_medio, height=5)
    campo1.pack(fill=BOTH, expand=True)

    campo1.bind("<Key>", detectar_teclas)
    campo1.bind("<Tab>", cambiar_foco)  # 🔥 clave

    # -------- Botones -------- #
    btn_iniciar = Button(frame_botones, text="Iniciar", command=iniciar)
    btn_iniciar.pack(side=LEFT, padx=10)

    btn_finalizar = Button(frame_botones, text="Finalizar", command=finalizar, state=NORMAL) # 🔥 cambiar a DISABLED
    btn_finalizar.pack(side=LEFT, padx=10)

    btn_limpiar = Button(frame_botones, text="Limpiar", command=limpiar)
    btn_limpiar.pack(side=LEFT, padx=10)

    btn_iniciar.bind('<Return>', lambda event: iniciar())
    btn_finalizar.bind('<Return>', lambda event: finalizar())

    btn_iniciar.focus_set()

    # -------- Tabla -------- #
    tabla = ttk.Treeview(frame_inferior, columns=("dato", "valor"), show="headings")
    tabla.heading("dato", text="Métrica")
    tabla.heading("valor", text="Valor")

    tabla.column("dato", anchor="w", width=250)
    tabla.column("valor", anchor="center", width=120)

    tabla.pack(fill=BOTH, expand=True)

    # -------- Resultado -------- #
    resultado = Label(root, text="")
    resultado.pack(pady=5)

    root.mainloop()

main()