import os
import requests
import logging
import colorlog
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime
import pytz
from dotenv import load_dotenv

# Charger la configuration selon l'environnement
env = os.getenv('ENV', 'dev')
load_dotenv(f".env.{env}")

# Créer le dossier logs si nécessaire (pour dev)
if os.getenv('LOG_TO_FILE', 'non').lower() in ['oui', 'yes', 'true']:
    os.makedirs('logs', exist_ok=True)

# Formatter avec timezone Paris
class ParisFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=pytz.timezone('Europe/Paris'))
        return dt.strftime(datefmt or '%Y-%m-%d %H:%M:%S')

# Configurer le logger
logger = logging.getLogger()
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logger.setLevel(getattr(logging, log_level))

# Formatter pour fichiers (sans couleur)
file_formatter = ParisFormatter('%(asctime)s - %(levelname)s - %(message)s')

# Handler pour console avec couleurs
console_handler = colorlog.StreamHandler(sys.stdout)
console_formatter = colorlog.ColoredFormatter(
    '%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Handler pour fichier avec rotation (si activé)
if os.getenv('LOG_TO_FILE', 'non').lower() in ['oui', 'yes', 'true']:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logging.info("Logs vers fichier activés")

logging.info(f"Application démarrée en mode {env}")

def get_weather(city):
    """
    Récupère et affiche la météo actuelle pour une ville donnée.
    Utilise l'API wttr.in (sans clé API nécessaire).
    """
    base_url = os.getenv('API_BASE_URL', 'https://wttr.in')
    url = f"{base_url}/{city}?format=j1"
    logging.debug(f"Requête API : {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            current_condition = data['current_condition'][0]
            temp = current_condition['temp_C']
            description = current_condition['weatherDesc'][0]['value']
            logging.info(f"Météo récupérée pour {city}")
            print(f"Météo à {city} : {temp}°C, {description}")
        else:
            logging.error(f"Erreur API : {response.status_code}")
            print(f"Erreur lors de la récupération des données : {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Erreur réseau : {e}")
        print(f"Erreur réseau : {e}")

if __name__ == "__main__":
    city = input("Entrez le nom de la ville : ")
    get_weather(city)
    logging.info("Application terminée")