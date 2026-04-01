# Verifica si existen IDs faltantes o Pokémon entre  1 y 1025 
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path

from database.database import SessionLocal
from database.models import Pokemon

TOTAL_POKEMON = 1025

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def check_missing_ids():
    db = SessionLocal()
    try:
        ids = [p.id for p in db.query(Pokemon.id).order_by(Pokemon.id).all()]
        missing = [i for i in range(1, TOTAL_POKEMON+1) if i not in ids]

        print(f"✅ Total Pokémon en DB: {len(ids)}")
        if missing:
            print(f"⚠️ IDs faltantes: {missing}")
        else:
            print("🎉 Todos los IDs del 1 al 1025 están presentes.")
    finally:
        db.close()

if __name__ == "__main__":
    check_missing_ids()
