from .config import load_config
from .logger import setup_logging
from .weather import get_weather
import logging

def main():
    env = load_config()
    setup_logging()
    logging.info(f"Application démarrée en mode {env}")

    city = input("Entrez le nom de la ville : ")
    get_weather(city)
    logging.info("Application terminée")

if __name__ == "__main__":
    main()