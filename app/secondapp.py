# app.py (Standalone Streamlit application)
import streamlit as st
import requests
import random
import json
from typing import Dict, List, Optional

# Configuration
st.set_page_config(
    page_title="Pokémon Battle Simulator",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FFCC00;
        text-align: center;
        text-shadow: 2px 2px 4px #0075BE;
        margin-bottom: 2rem;
    }
    .pokemon-card {
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .battle-log {
        height: 400px;
        overflow-y: auto;
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .type-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 15px;
        margin: 5px 5px 5px 0;
        color: white;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #FFCC00, #FF0000);
    }
</style>
""", unsafe_allow_html=True)

# Backend functions (copied from your original code)
STATUS_EFFECTS = ['paralysis', 'burn', 'poison']
POKEAPI_BASE = "https://pokeapi.co/api/v2"

def fetch_pokemon_stats(name):
    try:
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
    except:
        return None

def get_evolution_chain(url):
    try:
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
    except:
        return []

def get_type_multiplier(attack_type, defense_type):
    chart = {
        'fire': {'grass': 2, 'water': 0.5, 'fire': 0.5},
        'water': {'fire': 2, 'grass': 0.5, 'water': 0.5},
        'grass': {'water': 2, 'fire': 0.5, 'grass': 0.5},
        'electric': {'water': 2, 'flying': 2, 'grass': 0.5, 'ground': 0},
        'normal': {'rock': 0.5, 'ghost': 0},
        'fighting': {'normal': 2, 'rock': 2, 'ice': 2, 'dark': 2, 'steel': 2, 
                     'flying': 0.5, 'poison': 0.5, 'bug': 0.5, 'psychic': 0.5, 'ghost': 0},
        'flying': {'grass': 2, 'fighting': 2, 'bug': 2, 'electric': 0.5, 'rock': 0.5, 'steel': 0.5},
        'poison': {'grass': 2, 'fairy': 2, 'poison': 0.5, 'ground': 0.5, 'rock': 0.5, 'ghost': 0.5},
        'ground': {'fire': 2, 'electric': 2, 'poison': 2, 'rock': 2, 'steel': 2, 
                   'grass': 0.5, 'bug': 0.5, 'flying': 0},
        'rock': {'fire': 2, 'ice': 2, 'flying': 2, 'bug': 2, 'fighting': 0.5, 'ground': 0.5, 'steel': 0.5},
        'bug': {'grass': 2, 'psychic': 2, 'dark': 2, 'fire': 0.5, 'fighting': 0.5, 'poison': 0.5, 
                'flying': 0.5, 'ghost': 0.5, 'steel': 0.5},
        'ghost': {'ghost': 2, 'psychic': 2, 'normal': 0, 'dark': 0.5},
        'steel': {'ice': 2, 'rock': 2, 'fairy': 2, 'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'steel': 0.5},
        'psychic': {'fighting': 2, 'poison': 2, 'dark': 0, 'steel': 0.5, 'psychic': 0.5},
        'ice': {'grass': 2, 'ground': 2, 'flying': 2, 'dragon': 2, 'fire': 0.5, 'water': 0.5, 'ice': 0.5, 'steel': 0.5},
        'dragon': {'dragon': 2, 'steel': 0.5, 'fairy': 0},
        'dark': {'psychic': 2, 'ghost': 2, 'fighting': 0.5, 'dark': 0.5, 'fairy': 0.5},
        'fairy': {'fighting': 2, 'dragon': 2, 'dark': 2, 'fire': 0.5, 'poison': 0.5, 'steel': 0.5}
    }
    return chart.get(attack_type, {}).get(defense_type, 1)

def get_pokemon_data(name):
    try:
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
    except:
        return {"error": "Failed to fetch Pokémon data"}

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
                log.append(f"{atk['name']} is paralyzed and can't move!")
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

# Type color mapping
type_colors = {
    "normal": "#A8A878",
    "fire": "#F08030",
    "water": "#6890F0",
    "electric": "#F8D030",
    "grass": "#78C850",
    "ice": "#98D8D8",
    "fighting": "#C03028",
    "poison": "#A040A0",
    "ground": "#E0C068",
    "flying": "#A890F0",
    "psychic": "#F85888",
    "bug": "#A8B820",
    "rock": "#B8A038",
    "ghost": "#705898",
    "dragon": "#7038F8",
    "dark": "#705848",
    "steel": "#B8B8D0",
    "fairy": "#EE99AC"
}

# App layout
st.markdown('<h1 class="main-header">Pokémon Battle Simulator</h1>', unsafe_allow_html=True)

# Sidebar for navigation
page = st.sidebar.selectbox("Navigation", ["Pokémon Data", "Battle Simulator"])

if page == "Pokémon Data":
    st.header("Pokémon Data Explorer")
    
    pokemon_name = st.text_input("Enter Pokémon name:", "pikachu").lower().strip()
    
    if st.button("Get Pokémon Data"):
        with st.spinner("Fetching Pokémon data..."):
            data = get_pokemon_data(pokemon_name)
            
            if data and "error" not in data:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Display Pokémon image
                    try:
                        st.image(f"https://img.pokemondb.net/artwork/{pokemon_name}.jpg", 
                                 caption=data['name'].title(), width=200)
                    except:
                        st.info("Image not available")
                
                with col2:
                    st.subheader(data['name'].title())
                    
                    # Display types with colored badges
                    types_html = "".join(
                        [f'<span class="type-badge" style="background-color: {type_colors.get(t, "#777777")};">{t.title()}</span>' 
                         for t in data['types']]
                    )
                    st.markdown(f"**Types:** {types_html}", unsafe_allow_html=True)
                    
                    # Display abilities
                    st.markdown(f"**Abilities:** {', '.join([a.title() for a in data['abilities']])}")
                    
                    # Display stats
                    st.write("**Stats:**")
                    stats_cols = st.columns(3)
                    stats = data['stats']
                    for i, (stat_name, value) in enumerate(stats.items()):
                        stats_cols[i % 3].metric(stat_name.title(), value)
                
                # Display moves and evolution chain in tabs
                tab1, tab2 = st.tabs(["Moves", "Evolution Chain"])
                
                with tab1:
                    st.write("**Moves (first 10):**")
                    for move in data['moves']:
                        st.write(f"- {move.title()}")
                
                with tab2:
                    if data['evolution']:
                        st.write("**Evolution Chain:**")
                        for i, pokemon in enumerate(data['evolution']):
                            st.write(f"{i+1}. {pokemon.title()}")
                    else:
                        st.write("This Pokémon does not evolve.")
            else:
                st.error("Pokémon not found. Please check the name and try again.")

else:  # Battle Simulator page
    st.header("Pokémon Battle Simulator")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        pokemon1 = st.text_input("First Pokémon:", "pikachu").lower().strip()
        if pokemon1:
            data1 = get_pokemon_data(pokemon1)
            if data1 and "error" not in data1:
                try:
                    st.image(f"https://img.pokemondb.net/artwork/{pokemon1}.jpg", 
                             caption=data1['name'].title(), width=150)
                except:
                    pass
                
                # Display types with colored badges
                types_html = "".join(
                    [f'<span class="type-badge" style="background-color: {type_colors.get(t, "#777777")};">{t.title()}</span>' 
                     for t in data1['types']]
                )
                st.markdown(f"**Types:** {types_html}", unsafe_allow_html=True)
                
                st.metric("HP", data1['stats']['hp'])
                st.metric("Attack", data1['stats']['attack'])
                st.metric("Defense", data1['stats']['defense'])
                st.metric("Speed", data1['stats']['speed'])
            else:
                st.warning("Pokémon not found")
    
    with col2:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>VS</h2>", unsafe_allow_html=True)
    
    with col3:
        pokemon2 = st.text_input("Second Pokémon:", "charmander").lower().strip()
        if pokemon2:
            data2 = get_pokemon_data(pokemon2)
            if data2 and "error" not in data2:
                try:
                    st.image(f"https://img.pokemondb.net/artwork/{pokemon2}.jpg", 
                             caption=data2['name'].title(), width=150)
                except:
                    pass
                
                # Display types with colored badges
                types_html = "".join(
                    [f'<span class="type-badge" style="background-color: {type_colors.get(t, "#777777")};">{t.title()}</span>' 
                     for t in data2['types']]
                )
                st.markdown(f"**Types:** {types_html}", unsafe_allow_html=True)
                
                st.metric("HP", data2['stats']['hp'])
                st.metric("Attack", data2['stats']['attack'])
                st.metric("Defense", data2['stats']['defense'])
                st.metric("Speed", data2['stats']['speed'])
            else:
                st.warning("Pokémon not found")
    
    # Handle battle simulation
    if st.button("Battle!", key="battle_button"):
        if not pokemon1 or not pokemon2:
            st.error("Please enter both Pokémon names!")
        else:
            with st.spinner("Simulating battle..."):
                battle_result = simulate_battle(pokemon1, pokemon2)
                
                if battle_result and "error" not in battle_result:
                    # Display winner
                    st.success(f"🎉 Winner: {battle_result['winner'].title()}!")
                    
                    # Display battle log
                    st.subheader("Battle Log")
                    log_html = "<div class='battle-log'>"
                    for log_entry in battle_result['battle_log']:
                        log_html += f"<p>{log_entry}</p>"
                    log_html += "</div>"
                    st.markdown(log_html, unsafe_allow_html=True)
                    
                    # Display status effects
                    if battle_result['status_effects']:
                        st.subheader("Status Effects")
                        for pokemon, status in battle_result['status_effects'].items():
                            if status:
                                st.write(f"{pokemon.title()}: {status.title()}")
                else:
                    st.error("Error simulating battle. Please check the Pokémon names and try again.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #777;'>"
    "Pokémon Battle Simulator - Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)