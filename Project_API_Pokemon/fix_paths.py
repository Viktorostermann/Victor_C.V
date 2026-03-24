from database.database import SessionLocal
from database.models import Pokemon
import os

def fix_sprite_paths():
    db = SessionLocal()
    try:
        pokemons = db.query(Pokemon).all()
        for p in pokemons:
            if p.image_path:
                # Si la ruta es absoluta, la convertimos a relativa
                filename = os.path.basename(p.image_path)
                new_path = f"assets/pokemon_images/{filename}"
                if p.image_path != new_path:
                    print(f"🔧 Corrigiendo {p.id}: {p.image_path} -> {new_path}")
                    p.image_path = new_path
        db.commit()
        print("✅ Todas las rutas de sprites fueron corregidas a relativas.")
    finally:
        db.close()

if __name__ == "__main__":
    fix_sprite_paths()
