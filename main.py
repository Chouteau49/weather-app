import requests

def get_weather(city):
    """
    Récupère et affiche la météo actuelle pour une ville donnée.
    Utilise l'API wttr.in (sans clé API nécessaire).
    """
    url = f"https://wttr.in/{city}?format=j1"
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