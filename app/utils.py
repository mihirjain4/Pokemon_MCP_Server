import requests

def get_evolution_chain(url):
    res = requests.get(url)
    if res.status_code != 200:
        return {}

    chain = res.json()['chain']
    evolution = []
    while chain:
        evolution.append(chain['species']['name'])
        if chain['evolves_to']:
            chain = chain['evolves_to'][0]
        else:
            break
    return evolution

def get_type_multiplier(attack_type, defense_type):
    chart = {
        'fire': {'grass': 2, 'water': 0.5},
        'water': {'fire': 2, 'grass': 0.5},
        'grass': {'water': 2, 'fire': 0.5},
        'electric': {'water': 2, 'ground': 0},
    }
    return chart.get(attack_type, {}).get(defense_type, 1)