import os
import requests
from dotenv import load_dotenv

# Charger la configuration selon l'environnement
env = os.getenv('ENV', 'dev')
load_dotenv(f".env.{env}")

def get_weather(city):
    """
    Récupère et affiche la météo actuelle pour une ville donnée.
    Utilise l'API wttr.in (sans clé API nécessaire).
    """
    base_url = os.getenv('API_BASE_URL', 'https://wttr.in')
    url = f"{base_url}/{city}?format=j1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        current_condition = data['current_condition'][0]
        temp = current_condition['temp_C']
        description = current_condition['weatherDesc'][0]['value']
        print(f"Météo à {city} : {temp}°C, {description}")
    else:
        print(f"Erreur lors de la récupération des données : {response.status_code}")

if __name__ == "__main__":
    city = input("Entrez le nom de la ville : ")
    get_weather(city)