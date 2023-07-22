import time
import logging
from os import environ

from lib.plex import get_plex_wl
from lib.servarr import radarr_check_new, sonarr_check_new

TIME_INTERVAL: int = int(environ.get("TIME_INTERVAL", 60))

logging.basicConfig(
    format="%(asctime)s [%(levelname)-4s] %(message)s",
    level=environ.get("LOG_LEVEL", "INFO"),
    datefmt="%d-%m-%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)


def sync():
    plex_imdb_ids: dict = get_plex_wl()
    radarr_check_new(plex_imdb_ids)
    sonarr_check_new(plex_imdb_ids)


while True:
    sync()
    time.sleep(TIME_INTERVAL)
