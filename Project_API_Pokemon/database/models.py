# models.py
from sqlalchemy import Column, Integer, String
from database.database import Base

class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    special_attack = Column(Integer, nullable=False)
    special_defense = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    types = Column(String(100))       # Añadido por migración
    abilities = Column(String(100))   # Añadido por migración
    generation = Column(Integer)
    region = Column(String(100))
    image_path = Column(String, nullable=True)  # 👈 nuevo campo