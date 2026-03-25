import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path

from database.models import Pokemon

TOTAL_POKEMON = 1025

# ----------------- CARGAR ENV -----------------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("No se encontró DATABASE_URL en el .env")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def check_pokemon_db():
    db = SessionLocal()
    try:
        total = db.query(Pokemon).count()
        porcentaje = (total / TOTAL_POKEMON) * 100
        print(f"✅ Total Pokémon en DB: {total}/{TOTAL_POKEMON} ({porcentaje:.2f}%)")

        if total < TOTAL_POKEMON:
            faltantes = [
                i for i in range(1, TOTAL_POKEMON + 1)
                if not db.query(Pokemon).filter(Pokemon.id == i).first()
            ]
            print(f"⚠️ IDs faltantes (primeros 20): {faltantes[:20]}")
            # Opcional: exportar a archivo
            with open("faltantes.txt", "w") as f:
                f.write("\n".join(map(str, faltantes)))
            print("📄 Lista completa de IDs faltantes guardada en faltantes.txt")

        # Mostrar algunos registros
        pokemons = db.query(Pokemon).order_by(Pokemon.id).limit(10).all()
        for p in pokemons:
            print(f"ID: {p.id}, Nombre: {p.name}, HP: {p.hp}, Ataque: {p.attack}, Defensa: {p.defense}")

    finally:
        db.close()

if __name__ == "__main__":
    check_pokemon_db()
