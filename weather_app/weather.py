import requests
import logging
import os
from typing import Dict, Optional


def get_weather(city: str) -> Optional[Dict[str, str]]:
    """
    Récupère la météo actuelle pour une ville donnée.
    Utilise l'API wttr.in (sans clé API nécessaire).
    Retourne un dict avec 'temp', 'description' ou None en cas d'erreur.
    """
    base_url = os.getenv("API_BASE_URL", "https://wttr.in")
    url = f"{base_url}/{city}?format=j1"
    logging.debug(f"Requête API : {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            current_condition = data["current_condition"][0]
            temp = current_condition["temp_C"]
            description = current_condition["weatherDesc"][0]["value"]
            logging.info(f"Météo récupérée pour {city}")
            return {"temp": temp, "description": description}
        else:
            logging.error(f"Erreur API : {response.status_code}")
            return None
    except requests.RequestException as e:
        logging.error(f"Erreur réseau : {e}")
        return None
