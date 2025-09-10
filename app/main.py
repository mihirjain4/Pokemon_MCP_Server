from fastapi import FastAPI, Query
from app.data_resource import get_pokemon_data
from app.battle_simulator import simulate_battle

app = FastAPI()

@app.get("/resource/pokemon")
def fetch_pokemon_data(name: str = Query(...)):
    return get_pokemon_data(name.lower())

@app.post("/tool/simulate_battle")
def battle(pokemon_1: str, pokemon_2: str):
    return simulate_battle(pokemon_1.lower(), pokemon_2.lower())