#pokeapi_client.py
import requests

BASE_URL = "https://pokeapi.co/api/v2/pokemon"


def get_pokemon_from_api(pokemon_id, retries=3):
    url = f"{BASE_URL}/{pokemon_id}"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Intento {attempt+1} fallido para Pokémon #{pokemon_id}: {e}")
    return None