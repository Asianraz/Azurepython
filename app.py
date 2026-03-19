import os
import random
from typing import Any, Dict, Optional

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon"


def fetch_pokemon(identifier: str) -> Optional[Dict[str, Any]]:
    """Fetch and normalize Pokemon data from PokeAPI."""
    try:
        response = requests.get(f"{POKEAPI_BASE_URL}/{identifier.lower()}", timeout=8)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return None

    image = (
        data.get("sprites", {})
        .get("other", {})
        .get("official-artwork", {})
        .get("front_default")
        or data.get("sprites", {}).get("front_default")
    )

    return {
        "name": data.get("name", "unknown").title(),
        "id": data.get("id", "-"),
        "height": data.get("height", "-"),
        "weight": data.get("weight", "-"),
        "types": [t.get("type", {}).get("name", "unknown").title() for t in data.get("types", [])],
        "abilities": [a.get("ability", {}).get("name", "unknown").title() for a in data.get("abilities", [])],
        "image": image,
    }


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("name", "pikachu").strip()
    pokemon = fetch_pokemon(query)
    error = None

    if pokemon is None:
        error = f"Could not find Pokemon '{query}'. Try another name (e.g., charizard)."

    return render_template("index.html", pokemon=pokemon, query=query, error=error)


@app.route("/random", methods=["GET"])
def random_pokemon():
    random_id = str(random.randint(1, 151))
    pokemon = fetch_pokemon(random_id)
    return render_template("index.html", pokemon=pokemon, query="", error=None)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
