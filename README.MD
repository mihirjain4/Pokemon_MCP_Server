# 🧠 Pokémon Battle Simulation – MCP Server

This project implements a complete Pokémon battle simulation system that provides:


1. **Pokémon Data Resource** — exposes comprehensive Pokémon data from PokeAPI
2. **Battle Simulation Tool** — allows users to simulate battles between any two Pokémon with realistic mechanics

---

## 📚 What is MCP?

MCP (Model Context Protocol) is an open protocol that standardizes how applications provide context to LLMs. More info: [modelcontextprotocol.io](https://modelcontextprotocol.io/introduction)

This project implements an MCP-compatible server using FastAPI, allowing LLMs to interact with Pokémon data and simulate turn-based battles through structured APIs.

---

## 🚀 Features

### ✅ Pokémon Data Resource
- Connects to public Pokémon datasets using [PokeAPI](https://pokeapi.co)
- Provides information such as:
  - Base Stats: HP, Attack, Defense, Sp. Attack, Sp. Defense, Speed
  - Pokémon Types
  - Abilities
  - Available Moves and their Effects
  - Evolution Data
- Exposes endpoints following MCP resource design to make this accessible to LLMs

### ✅ Battle Simulation Tool
- Accepts any two Pokémon names
- Simulates a turn-based battle based on:
  - Type effectiveness (e.g. Water > Fire)
  - Base stats and move power
  - Speed for turn order
  - Random damage variation
  - Status effects (e.g. Burn, Paralysis, Poison)
- Returns detailed battle logs and winner

### ✅ FastAPI Backend
- RESTful API: Clean, well-structured endpoints

- PokeAPI Integration: Real-time data fetching from official Pokémon database

- Data Processing: Efficient handling and transformation of Pokémon data
### ✅Streamlit Frontend 
- Interactive UI: User-friendly interface for data exploration and battles

- Visual Display: Pokémon images with type badges and stat metrics

- Real-time Simulation: Live battle visualization with animated logs

- Responsive Design: Mobile and desktop compatible interface
---

## 📁 Project Structure

pokemon-battle-simulator/
│
├── app/                       # FastAPI Backend
│   ├── __init__.py
│   ├── main.py               # FastAPI application and endpoints
│   ├── app.py                # Streamlit Frontend Application
│   ├── data_resource.py      # Pokémon data fetching from PokeAPI
│   ├── battle_simulator.py   # Battle simulation logic
│   └── utils.py             # Helper functions (type multipliers, evolution chains)
│
├── requirements.txt          # Python dependencies
└── README.md
---

## ⚙️ Installation & Setup

### 🐍 Prerequisites
- Python 3.8 or later
- pip
- Internet connection (for PokeAPI access)

### ✅ Step-by-Step

1. **Create a virtual environment**

bash
Copy code
python -m venv venv
source venv/bin/activate      # On Unix/macOS
venv\Scripts\activate         # On Windows

2. **Install dependencies**

bash
pip install -r requirements.txt

3. **Run the FastAPI backend server (Terminal 1)**

bash
uvicorn app.main:app --reload --port 8000

4. **Run the Streamlit frontend (Terminal 2)**

bash
streamlit run app.py --server.port 8501

### 🌐 Access Points
- Backend API: http://127.0.0.1:8000
- API Documentation: http://127.0.0.1:8000/docs
- Web Interface: http://localhost:8501

You should now see:

nginx
Uvicorn running on http://127.0.0.1:8000


🔍 API Usage
🧪 Test from Swagger UI
Visit:

http://127.0.0.1:8000/docs


📌 Endpoints
1. Get Pokémon Info
Endpoint: /resource/pokemon?name={name}

Method: GET

Example:

bash
GET GET http://127.0.0.1:8000/resource/pokemon?name=pikachu
Response:

json
{
  "name": "pikachu",
  "types": ["electric"],
  "stats": {
    "hp": 35,
    "attack": 55,
    "defense": 40,
    "special-attack": 50,
    "special-defense": 50,
    "speed": 90
  },
  "abilities": ["static", "lightning-rod"],
  "moves": ["thunder-shock", "quick-attack", "thunderbolt"],
  "evolution": ["pichu", "pikachu", "raichu"]
}
2. Simulate Battle
Endpoint: /tool/simulate_battle?pokemon_1={name}&pokemon_2={name}

Method: POST

Example:
bash
POST http://127.0.0.1:8000/tool/simulate_battle?pokemon_1=pikachu&pokemon_2=squirtle

Body:

{
  "battle_log": [
    "pikachu used a move and dealt 15 damage to squirtle (70 HP left)",
    "squirtle used a move and dealt 12 damage to pikachu (58 HP left)"
  ],
  "winner": "squirtle",
  "status_effects": {
    "pikachu": null,
    "squirtle": null
  }
}


## 🤖 MCP Compliance
This project follows the MCP protocol by:

Structuring API responses in JSON for LLM consumption

Using standardized resource (GET) and tool (POST) interfaces

Simulating interactive tools accessible via LLM prompts

## 📄 How an LLM Would Query This Resource
Example (natural language prompt to an LLM):

"Use the Pokémon Data Resource to fetch stats for Pikachu."

LLM converts to:

http
GET /resource/pokemon?name=pikachu
"Simulate a battle between Charmander and Bulbasaur using the Battle Simulation Tool."

LLM converts to:

http
POST /tool/simulate_battle?pokemon_1=charmander&pokemon_2=bulbasaur
{
  "pokemon1": "charmander",
  "pokemon2": "bulbasaur"
}

## 🧪 Testing via Postman
You can also test APIs manually with Postman:

Pokémon Info
Method: GET

URL: http://127.0.0.1:8000/pokemon/bulbasaur

Battle Simulation
Method: POST

URL: http://127.0.0.1:8000/simulate_battle

Body (raw JSON):

json
{
  "pokemon1": "bulbasaur",
  "pokemon2": "charmander"
}

## 🎮 Web Interface Usage

1. Open http://localhost:8501

2. Use sidebar to navigate between:

  - Pokémon Data: Explore detailed Pokémon information

  - Battle Simulator: Run interactive battle simulations

## 🐛 Troubleshooting

Common Issues:

- Ensure ports 8000/8501 are available
- Check internet connection for PokeAPI access
- Verify all dependencies are installed

## 📝 License

Educational use only. Pokémon is a trademark of Nintendo/Creatures Inc./GAME FREAK Inc.

## 🤝 Contributing

This project demonstrates modern web development with:

- FastAPI backend development
- Streamlit frontend creation
- External API integration
- Real-time battle simulation

Feel free to submit issues or enhancement requests!