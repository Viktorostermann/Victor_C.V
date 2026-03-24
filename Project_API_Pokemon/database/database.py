import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from pathlib import Path

# ----------------- CARGAR ENV -----------------
env_path = Path(__file__).parent / ".env"   # tu .env está en /database/.env
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("No se encontró DATABASE_URL en el .env")

# ----------------- CONEXIÓN -----------------
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ----------------- CREAR TABLAS SI NO EXISTEN -----------------
from database import models
Base.metadata.create_all(bind=engine)
