# Api_PokeAPI

Mini aplicación creada con Streamlit que muestra los Pokémon de la primera generación utilizando la PokéAPI.

## Características

- Muestra nombre e imagen del Pokémon
- Navegación con botones Anterior y Siguiente
- Datos obtenidos desde la PokéAPI

## Instalación

Clonar el repositorio:

git clone https://github.com/usuario/Api_PokeAPI.git

Entrar al proyecto:

cd Api_PokeAPI

Instalar dependencias:

pip install -r requirements.txt:

fastapi==0.110.0
uvicorn[standard]==0.29.0
SQLAlchemy==2.0.25
alembic==1.13.1
python-dotenv==1.0.1
matplotlib==3.8.3
pandas==2.2.1
numpy==1.26.4
python-dateutil==2.9.0.post0
six==1.17.0
tzdata==2025.3

## Ejecutar la aplicación

streamlit run app.py

## Tecnologías utilizadas

- Python
- Streamlit
- PokéAPI

NOTAS: La aplicación se puede ejecutar en cualquier dispositivo que tenga Python instalado.

## Autor
Victor Miletic

## Licencia
Este proyecto está bajo la Licencia MIT.

## Recomendaciones para proyectos de desarrollo mayores separar siempre :
UI (app.py)
API / lógica (pokemon_api.py)
dependencias
documentación

# Ejecucion scripts:

$env:PYTHONPATH="C:\Proyectos\Python\FastAPI\Project_API_Pokemon" python -m database.check_db
