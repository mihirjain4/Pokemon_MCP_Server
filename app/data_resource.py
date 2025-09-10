import requests
from app.utils import get_evolution_chain

POKEAPI_BASE = "https://pokeapi.co/api/v2"

def get_pokemon_data(name):
    pokemon_url = f"{POKEAPI_BASE}/pokemon/{name}"
    species_url = f"{POKEAPI_BASE}/pokemon-species/{name}"

    poke_res = requests.get(pokemon_url)
    species_res = requests.get(species_url)

    if poke_res.status_code != 200 or species_res.status_code != 200:
        return {"error": "Pokemon not found"}

    poke_data = poke_res.json()
    species_data = species_res.json()

    types = [t['type']['name'] for t in poke_data['types']]
    abilities = [a['ability']['name'] for a in poke_data['abilities']]
    stats = {s['stat']['name']: s['base_stat'] for s in poke_data['stats']}
    moves = [m['move']['name'] for m in poke_data['moves']]

    evolution_chain_url = species_data['evolution_chain']['url']
    evolution_chain = get_evolution_chain(evolution_chain_url)

    return {
        "name": poke_data['name'],
        "types": types,
        "abilities": abilities,
        "stats": stats,
        "moves": moves[:10],
        "evolution": evolution_chain
    }