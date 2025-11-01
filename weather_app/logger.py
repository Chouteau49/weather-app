import logging
import colorlog
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime
import pytz
from pathlib import Path


class ParisFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=pytz.timezone("Europe/Paris"))
        return dt.strftime(datefmt or "%Y-%m-%d %H:%M:%S")


def setup_logging() -> None:
    """Configure les logs."""
    import os

    logger = logging.getLogger()
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level))

    # Formatter pour fichiers
    file_formatter = ParisFormatter("%(asctime)s - %(levelname)s - %(message)s")

    # Handler console avec couleurs
    console_handler = colorlog.StreamHandler(sys.stdout)
    console_formatter = colorlog.ColoredFormatter(
        "%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Handler fichier si activé
    if os.getenv("LOG_TO_FILE", "non").lower() in ["oui", "yes", "true"]:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        file_handler = RotatingFileHandler(
            log_dir / "app.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        logging.info("Logs vers fichier activés")
