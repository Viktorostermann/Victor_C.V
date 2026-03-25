from services.pokemon_service import preload_pokemon_range

# Probar precarga de los primeros 10 Pokémon
preload_pokemon_range(1, 1025, max_workers=5)
