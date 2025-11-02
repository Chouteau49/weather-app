from .config import load_config
from .logger import setup_logging
from .weather import get_weather
import logging
import sys


def main_cli() -> None:
    env = load_config()
    setup_logging()
    logging.info(f"Application démarrée en mode {env}")

    city = input("Entrez le nom de la ville : ")
    weather = get_weather(city)
    if weather:
        logging.info(f"Météo à {city} : {weather['temp']}°C, {weather['description']}")
    else:
        logging.error("Impossible de récupérer la météo.")
    logging.info("Application terminée")


def main_api() -> None:
    from .api import app
    import uvicorn
    env = load_config()
    setup_logging()
    logging.info(f"API démarrée en mode {env}")
    uvicorn.run(app, host="0.0.0.0", port=8000)


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        main_api()
    else:
        main_cli()


if __name__ == "__main__":
    main()
