import tkinter as tk
from tkinter import ttk, messagebox
import random

# 🪟 Ventana principal
root = tk.Tk()
root.title("🚢 Hundir Flota For CO'NQUERBLOCKS")
root.geometry("800x600")

# 🧬 Variables vinculadas
dificultad_var = tk.StringVar(value="Fácil")
tamano_var = tk.StringVar(value="5")

# 🧲 Contenedor central
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# 🧪 Overlay técnico (flotante y desacoplado)
overlay = tk.Frame(root, bg="#222", bd=2, relief="ridge")
overlay.place(relx=0.75, rely=0.05, relwidth=0.22, relheight=0.25)

overlay_title = tk.Label(overlay, text="🧭 Overlay Técnico", bg="#222", fg="white", font=("Arial", 10, "bold"))
overlay_title.pack(pady=5)
overlay_info = tk.Label(overlay, text="", bg="#222", fg="white", justify="left", font=("Arial", 9))
overlay_info.pack()

# 🧾 Labels de estado
estado_label = tk.Label(main_frame, text="")
estado_label.grid(row=4, column=0, columnspan=2, pady=5)
pista_label = tk.Label(main_frame, text="")
pista_label.grid(row=5, column=0, columnspan=2, pady=5)

# 📦 Frame para tablero
tablero_frame = tk.Frame(main_frame)
tablero_frame.grid(row=6, column=0, columnspan=2, pady=10)

# 🎯 Función iniciar/reiniciar
def iniciar_juego():
    global botones
    tablero_frame.configure(bg="#444")
    for widget in tablero_frame.winfo_children():
        widget.destroy()

    dificultad = dificultad_var.get()
    tamano = int(tamano_var.get())
    niveles = {
        "Fácil": {'num_barcos': tamano * tamano // 6, 'intentos_maximos': tamano * 3, 'pista_cada_n_intentos': 3},
        "Medio": {'num_barcos': tamano * tamano // 5, 'intentos_maximos': tamano * 2, 'pista_cada_n_intentos': 5},
        "Difícil": {'num_barcos': tamano * tamano // 4, 'intentos_maximos': tamano,     'pista_cada_n_intentos': 7}
    }
    config = niveles[dificultad]

    tablero = [['~' for _ in range(tamano)] for _ in range(tamano)]
    barcos = 0
    while barcos < config['num_barcos']:
        f, c = random.randint(0, tamano - 1), random.randint(0, tamano - 1)
        if tablero[f][c] == '~':
            tablero[f][c] = 'B'
            barcos += 1

    # 🔎 Overlay info actualizada
    overlay_info.config(text=f"Tamaño: {tamano}x{tamano}\nDificultad: {dificultad}\nBarcos: {config['num_barcos']}\nIntentos máx: {config['intentos_maximos']}")

    intentos = 0
    hundidos = 0
    juego_activo = True
    botones = []

    def dar_pista():
        for f in range(tamano):
            for c in range(tamano):
                if tablero[f][c] == 'B':
                    return f"💡 Barco cerca de fila {f}"
        return "🔍 Sin barcos visibles"

    def fin_juego(mensaje):
        nonlocal juego_activo
        juego_activo = False
        respuesta = messagebox.askquestion("Fin del juego", f"{mensaje}\n¿Jugar otra vez?")
        if respuesta == "yes":
            iniciar_juego()
        else:
            root.quit()

    def click(fila, col):
        nonlocal intentos, hundidos, juego_activo
        if not juego_activo:
            return

        celda = tablero[fila][col]
        boton = botones[fila][col]

        if celda == 'B':
            boton.config(text="💥", bg="red")
            tablero[fila][col] = 'X'
            hundidos += 1
        elif celda == '~':
            boton.config(text="🌊", bg="blue")
            tablero[fila][col] = 'O'
            intentos += 1
            if intentos % config['pista_cada_n_intentos'] == 0:
                pista_label.config(text=dar_pista())
        else:
            return

        estado_label.config(text=f"Intentos: {intentos}/{config['intentos_maximos']} - Hundidos: {hundidos}/{config['num_barcos']}")

        if hundidos == config['num_barcos']:
            estado_label.config(text="🏆 ¡Has ganado!")
            fin_juego("🏆 ¡Has ganado!")
        elif intentos >= config['intentos_maximos']:
            estado_label.config(text="💀 ¡Has perdido!")
            fin_juego("💀 ¡Has perdido!")

    for f in range(tamano):
        fila_botones = []
        for c in range(tamano):
            b = tk.Button(tablero_frame, text="~", width=4, height=2,
                          command=lambda ff=f, cc=c: click(ff, cc))
            b.grid(row=f, column=c, padx=1, pady=1)
            fila_botones.append(b)
        botones.append(fila_botones)

# 🎚️ Configuración inicial
tk.Label(main_frame, text="Seleccione dificultad:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
dificultad_combobox = ttk.Combobox(main_frame, textvariable=dificultad_var)
dificultad_combobox['values'] = ("Fácil", "Medio", "Difícil")
dificultad_combobox.grid(row=0, column=1, sticky="w")
dificultad_combobox.current(0)

tk.Label(main_frame, text="Tamaño del tablero:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Entry(main_frame, textvariable=tamano_var, width=5).grid(row=1, column=1, sticky="w", pady=5)

tk.Button(main_frame, text="🚀 Iniciar Juego", command=iniciar_juego).grid(row=2, column=0, columnspan=2, pady=10)

# ▶️ Ejecutar GUI
root.mainloop()
# 🌊 Fin del programa