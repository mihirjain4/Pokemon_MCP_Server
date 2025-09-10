# app.py (Streamlit application - Fixed Version)
import streamlit as st
import requests
import json

# Configuration
API_BASE = "http://127.0.0.1:8000"

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
    .log-entry {
        margin: 5px 0;
        padding: 5px;
        border-radius: 5px;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def get_pokemon_data(name):
    try:
        response = requests.get(f"{API_BASE}/resource/pokemon?name={name}")
        if response.status_code == 200:
            return response.json()
        return {"error": f"HTTP Error: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}

def simulate_battle(pokemon1, pokemon2):
    try:
        # Fixed: Use query parameters instead of form data
        response = requests.post(
            f"{API_BASE}/tool/simulate_battle?pokemon_1={pokemon1}&pokemon_2={pokemon2}"
        )
        if response.status_code == 200:
            return response.json()
        return {"error": f"HTTP Error: {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}

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

# Debug section (can be collapsed)
with st.expander("Debug Info", expanded=False):
    st.write("API Base URL:", API_BASE)
    if st.button("Test API Connection"):
        try:
            test_response = requests.get(f"{API_BASE}/resource/pokemon?name=pikachu")
            st.write("Test Response Status:", test_response.status_code)
            st.write("Test Response Text:", test_response.text)
        except Exception as e:
            st.error(f"Connection test failed: {str(e)}")

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
                    if 'types' in data:
                        types_html = "".join(
                            [f'<span class="type-badge" style="background-color: {type_colors.get(t, "#777777")};">{t.title()}</span>' 
                             for t in data['types']]
                        )
                        st.markdown(f"**Types:** {types_html}", unsafe_allow_html=True)
                    
                    # Display abilities
                    if 'abilities' in data:
                        st.markdown(f"**Abilities:** {', '.join([a.title() for a in data['abilities']])}")
                    
                    # Display stats
                    if 'stats' in data:
                        st.write("**Stats:**")
                        stats_cols = st.columns(3)
                        stats = data['stats']
                        for i, (stat_name, value) in enumerate(stats.items()):
                            stats_cols[i % 3].metric(stat_name.title(), value)
                
                # Display moves and evolution chain in tabs
                if 'moves' in data or 'evolution' in data:
                    tab1, tab2 = st.tabs(["Moves", "Evolution Chain"])
                    
                    with tab1:
                        if 'moves' in data and data['moves']:
                            st.write("**Moves (first 10):**")
                            for move in data['moves'][:10]:
                                st.write(f"- {move.title()}")
                        else:
                            st.write("No moves data available.")
                    
                    with tab2:
                        if 'evolution' in data and data['evolution']:
                            st.write("**Evolution Chain:**")
                            for i, pokemon in enumerate(data['evolution']):
                                st.write(f"{i+1}. {pokemon.title()}")
                        else:
                            st.write("No evolution data available.")
            else:
                error_msg = data.get('error', 'Unknown error') if data else 'No data returned'
                st.error(f"Error fetching Pokémon data: {error_msg}")

else:  # Battle Simulator page
    st.header("Pokémon Battle Simulator")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        pokemon1 = st.text_input("First Pokémon:", "pikachu").lower().strip()
        data1 = None
        if pokemon1:
            data1 = get_pokemon_data(pokemon1)
            if data1 and "error" not in data1:
                try:
                    st.image(f"https://img.pokemondb.net/artwork/{pokemon1}.jpg", 
                             caption=data1.get('name', pokemon1).title(), width=150)
                except:
                    pass
                
                # Display types with colored badges
                if 'types' in data1:
                    types_html = "".join(
                        [f'<span class="type-badge" style="background-color: {type_colors.get(t, "#777777")};">{t.title()}</span>' 
                         for t in data1['types']]
                    )
                    st.markdown(f"**Types:** {types_html}", unsafe_allow_html=True)
                
                if 'stats' in data1:
                    st.metric("HP", data1['stats'].get('hp', 'N/A'))
                    st.metric("Attack", data1['stats'].get('attack', 'N/A'))
                    st.metric("Defense", data1['stats'].get('defense', 'N/A'))
                    st.metric("Speed", data1['stats'].get('speed', 'N/A'))
            else:
                st.warning("Pokémon data not available")
    
    with col2:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>VS</h2>", unsafe_allow_html=True)
    
    with col3:
        pokemon2 = st.text_input("Second Pokémon:", "charmander").lower().strip()
        data2 = None
        if pokemon2:
            data2 = get_pokemon_data(pokemon2)
            if data2 and "error" not in data2:
                try:
                    st.image(f"https://img.pokemondb.net/artwork/{pokemon2}.jpg", 
                             caption=data2.get('name', pokemon2).title(), width=150)
                except:
                    pass
                
                # Display types with colored badges
                if 'types' in data2:
                    types_html = "".join(
                        [f'<span class="type-badge" style="background-color: {type_colors.get(t, "#777777")};">{t.title()}</span>' 
                         for t in data2['types']]
                    )
                    st.markdown(f"**Types:** {types_html}", unsafe_allow_html=True)
                
                if 'stats' in data2:
                    st.metric("HP", data2['stats'].get('hp', 'N/A'))
                    st.metric("Attack", data2['stats'].get('attack', 'N/A'))
                    st.metric("Defense", data2['stats'].get('defense', 'N/A'))
                    st.metric("Speed", data2['stats'].get('speed', 'N/A'))
            else:
                st.warning("Pokémon data not available")
    
    # Handle battle simulation
    if st.button("Battle!", key="battle_button"):
        if not pokemon1 or not pokemon2:
            st.error("Please enter both Pokémon names!")
        else:
            with st.spinner("Simulating battle..."):
                battle_result = simulate_battle(pokemon1, pokemon2)
                
                if battle_result and "error" not in battle_result:
                    # Display winner
                    st.success(f"🎉 Winner: {battle_result.get('winner', 'Unknown').title()}!")
                    
                    # Display battle log
                    st.subheader("Battle Log")
                    if 'battle_log' in battle_result and battle_result['battle_log']:
                        log_html = "<div class='battle-log'>"
                        for log_entry in battle_result['battle_log']:
                            log_html += f"<div class='log-entry'>{log_entry}</div>"
                        log_html += "</div>"
                        st.markdown(log_html, unsafe_allow_html=True)
                    else:
                        st.info("No battle log available.")
                    
                    # Display status effects
                    if 'status_effects' in battle_result and battle_result['status_effects']:
                        st.subheader("Status Effects")
                        for pokemon, status in battle_result['status_effects'].items():
                            if status:
                                st.write(f"{pokemon.title()}: {status.title()}")
                else:
                    error_msg = battle_result.get('error', 'Unknown error') if battle_result else 'No response from server'
                    st.error(f"Error simulating battle: {error_msg}")
                    
                    # Debug information
                    with st.expander("Debug Details"):
                        st.write("Pokémon 1:", pokemon1)
                        st.write("Pokémon 2:", pokemon2)
                        st.write("Full error response:", battle_result)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #777;'>"
    "Pokémon Battle Simulator - Built with Streamlit and FastAPI"
    "</div>",
    unsafe_allow_html=True
)