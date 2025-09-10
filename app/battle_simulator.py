import random
import requests
from app.utils import get_type_multiplier

STATUS_EFFECTS = ['paralysis', 'burn', 'poison']

POKEAPI_BASE = "https://pokeapi.co/api/v2"

def fetch_pokemon_stats(name):
    res = requests.get(f"{POKEAPI_BASE}/pokemon/{name}")
    if res.status_code != 200:
        return None
    data = res.json()
    return {
        "name": name,
        "hp": next(s['base_stat'] for s in data['stats'] if s['stat']['name'] == 'hp'),
        "attack": next(s['base_stat'] for s in data['stats'] if s['stat']['name'] == 'attack'),
        "defense": next(s['base_stat'] for s in data['stats'] if s['stat']['name'] == 'defense'),
        "speed": next(s['base_stat'] for s in data['stats'] if s['stat']['name'] == 'speed'),
        "type": data['types'][0]['type']['name']
    }

def simulate_battle(pokemon_1, pokemon_2):
    p1 = fetch_pokemon_stats(pokemon_1)
    p2 = fetch_pokemon_stats(pokemon_2)

    if not p1 or not p2:
        return {"error": "Invalid Pokémon name(s)"}

    log = []
    status = {p1['name']: None, p2['name']: None}

    attacker, defender = (p1, p2) if p1['speed'] >= p2['speed'] else (p2, p1)

    while p1['hp'] > 0 and p2['hp'] > 0:
        for atk, defn in [(attacker, defender), (defender, attacker)]:
            if atk['hp'] <= 0 or defn['hp'] <= 0:
                break

            # Status effect: paralysis can skip turn
            if status[atk['name']] == 'paralysis' and random.random() < 0.25:
                log.append(f"{atk['name']} is paralyzed and can’t move!")
                continue

            # Random move power
            move_power = random.randint(40, 100)
            multiplier = get_type_multiplier(atk['type'], defn['type'])

            # Burn: halve attack
            effective_attack = atk['attack'] // 2 if status[atk['name']] == 'burn' else atk['attack']

            damage = (((2 * effective_attack / defn['defense']) * move_power) / 50 + 2) * multiplier
            damage = int(damage)

            defn['hp'] -= damage
            log.append(f"{atk['name']} used a move and dealt {damage} damage to {defn['name']} ({defn['hp']} HP left)")

            # Poison damage over time
            if status[defn['name']] == 'poison':
                poison_dmg = int(defn['hp'] * 0.05)
                defn['hp'] -= poison_dmg
                log.append(f"{defn['name']} took {poison_dmg} poison damage! ({defn['hp']} HP left)")

            # Inflict status effect randomly once
            if status[defn['name']] is None and random.random() < 0.2:
                inflicted = random.choice(STATUS_EFFECTS)
                status[defn['name']] = inflicted
                log.append(f"{defn['name']} is now affected by {inflicted}!")

        attacker, defender = defender, attacker

    winner = p1['name'] if p2['hp'] <= 0 else p2['name']
    return {"winner": winner, "battle_log": log, "status_effects": status}