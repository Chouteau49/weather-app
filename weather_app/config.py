import os
from dotenv import load_dotenv


def load_config() -> str:
    """Charge la configuration selon l'environnement."""
    env = os.getenv("ENV", "dev")
    load_dotenv(f".env.{env}")
    return env
