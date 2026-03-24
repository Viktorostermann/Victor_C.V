import pygame
pygame.init()

# 🖥️ Obtener dimensiones de pantalla para escalado defensivo
info_pantalla = pygame.display.Info()
ancho_pantalla = info_pantalla.current_w
alto_pantalla = info_pantalla.current_h

# 💡 Ventana redimensionable basada en la pantalla disponible
VENTANA = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Mi Juego")

# 🧩 Sprite (verificá que la ruta sea válida)
sprite_path = pygame.image.load("C:/Users/vikto/Python_VsCode/battle_tank/sprites/units/Tank_enemy/BackUp_red_tank_siegue_enemy.png")

# 🎮 Función para renderizar en posiciones iniciales
def inicializar_posiciones(x, y):
    VENTANA.fill((0, 0, 0))  # Fondo negro para contraste
    print(f"📐 Tamaño original del sprite: {sprite_path.get_width()}x{sprite_path.get_height()}")

    # 🛡️ Escalado defensivo si el sprite excede el área visible
    sprite_width = min(sprite_path.get_width(), VENTANA.get_width() // 2)
    sprite_height = min(sprite_path.get_height(), VENTANA.get_height() // 2)
    sprite_escalado = pygame.transform.scale(sprite_path, (sprite_width, sprite_height))

    # 🖼️ Renderizado en la posición deseada (con tolerancia)
    x_safe = min(x, VENTANA.get_width() - sprite_width)
    y_safe = min(y, VENTANA.get_height() - sprite_height)
    VENTANA.blit(sprite_escalado, (x_safe, y_safe))

    # ✅ Overlay rojo como control visual
    pygame.draw.rect(VENTANA, (255, 0, 0), (x_safe, y_safe, 50, 50))

    pygame.display.update()

# 🧪 Llamada real a la función (fuera del bloque de definición)
inicializar_posiciones(100, 150)

# 🔁 Bucle principal de la ventana
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

pygame.quit()
