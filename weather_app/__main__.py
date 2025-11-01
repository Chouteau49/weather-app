from .config import load_config
from .logger import setup_logging
from .weather import get_weather
import logging

def main():
    env = load_config()
    setup_logging()
    logging.info(f"Application démarrée en mode {env}")

    city = input("Entrez le nom de la ville : ")
    weather = get_weather(city)
    if weather:
        print(f"Météo à {city} : {weather['temp']}°C, {weather['description']}")
    else:
        print("Impossible de récupérer la météo.")
    logging.info("Application terminée")

if __name__ == "__main__":
    main()