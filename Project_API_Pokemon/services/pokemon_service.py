import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from database.database import SessionLocal
from database.models import Pokemon

BASE_URL = "https://pokeapi.co/api/v2/pokemon"
TOTAL_POKEMON = 1025

# Ruta absoluta hacia assets/pokemon_images
ASSETS_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "assets", "pokemon_images")
)

# ... resto de tu código idéntico ...



def download_pokemon_sprite(pokemon_id, sprite_url):
    os.makedirs(ASSETS_DIR, exist_ok=True)
    local_path = os.path.join(ASSETS_DIR, f"{pokemon_id}.png")

    try:
        response = requests.get(sprite_url, timeout=10)
        response.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(response.content)
        # ⚠️ Guardar en DB la ruta relativa
        return f"assets/pokemon_images/{pokemon_id}.png"
    except Exception as e:
        print(f"❌ Error descargando sprite de Pokémon {pokemon_id}: {e}")
        return None



def preload_pokemon_range(start_id: int, end_id: int, max_workers: int = 10):
    """Precarga un rango de Pokémon desde la API, guarda en DB y descarga sprites faltantes."""
    db = SessionLocal()
    try:
        # Traer todos los Pokémon en el rango
        existing = db.query(Pokemon).filter(Pokemon.id.between(start_id, end_id)).all()

        # IDs que faltan en DB
        existing_ids = {p.id for p in existing}
        ids_missing_in_db = [i for i in range(start_id, end_id + 1) if i not in existing_ids]

        # IDs que ya están en DB pero sin sprite local
        ids_missing_sprite = [p.id for p in existing if not p.image_path]

        # Unión de ambos casos
        ids_to_fetch = ids_missing_in_db + ids_missing_sprite

        if not ids_to_fetch:
            print(f"✅ Todos los Pokémon {start_id}-{end_id} ya tienen sprite en DB")
            return

        def fetch_pokemon(p_id: int):
            try:
                response = requests.get(f"{BASE_URL}/{p_id}", timeout=5)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"❌ Error con Pokémon {p_id}: {e}")
                return None

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for future in as_completed([executor.submit(fetch_pokemon, pid) for pid in ids_to_fetch]):
                data = future.result()
                if not data:
                    continue

                stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
                types = ",".join([t["type"]["name"] for t in data["types"]])
                abilities = ",".join([a["ability"]["name"] for a in data["abilities"]])

                # Descargar sprite y guardar en assets
                sprite_url = data["sprites"]["front_default"]
                image_path = None
                if sprite_url:
                    image_path = download_pokemon_sprite(data["id"], sprite_url)

                # Si ya existe en DB, actualizar; si no, insertar
                pokemon = db.query(Pokemon).get(data["id"])
                if pokemon:
                    pokemon.image_path = image_path or pokemon.image_path
                else:
                    pokemon = Pokemon(
                        id=data["id"],
                        name=data["name"],
                        height=data["height"],
                        weight=data["weight"],
                        hp=stats.get("hp", 0),
                        attack=stats.get("attack", 0),
                        defense=stats.get("defense", 0),
                        special_attack=stats.get("special-attack", 0),
                        special_defense=stats.get("special-defense", 0),
                        speed=stats.get("speed", 0),
                        types=types,
                        abilities=abilities,
                        generation=None,
                        region=None,
                        image_path=image_path
                    )
                    db.add(pokemon)

                print(f"✅ Guardado {data['id']} - {data['name']} con sprite en {image_path}")

        db.commit()
        print(f"Batch {start_id}-{end_id} completado. Total en DB: {db.query(Pokemon).count()}")

    finally:
        db.close()


def get_pokemon_data(db, pokemon_id: int):
    """Obtiene el objeto Pokémon desde la DB usando una sesión existente."""
    return db.query(Pokemon).get(pokemon_id)


if __name__ == "__main__":
    # Precarga de todos los Pokémon oficiales con sprites
    preload_pokemon_range(1, TOTAL_POKEMON, max_workers=5)
