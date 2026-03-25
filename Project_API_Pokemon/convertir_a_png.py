from PIL import Image
import os

# Ruta absoluta basada en el script
base_path = os.path.dirname(__file__)
img_path = os.path.join(base_path, "assets", "Pokedex.png")

# Abrir y convertir
img = Image.open(img_path)
img.save(os.path.join(base_path, "icon.ico"))

print("Icono creado correctamente")