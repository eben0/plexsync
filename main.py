import logging
import traceback
from os import environ
from concurrent.futures import ThreadPoolExecutor
from lib.timer import RepeatTimer

from lib.plex import get_plex_wl
from lib.servarr import radarr_check_new, sonarr_check_new

DEFAULT_INTERVAL: int = 60
TIME_INTERVAL: int = int(environ.get("TIME_INTERVAL", DEFAULT_INTERVAL))

logging.basicConfig(
    format="%(asctime)s [%(levelname)-4s] %(message)s",
    level=environ.get("LOG_LEVEL", "INFO"),
    datefmt="%d-%m-%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)


def sync():
    with ThreadPoolExecutor() as executor:
        try:
            plex_imdb_ids: dict = get_plex_wl()
            executor.submit(radarr_check_new, plex_imdb_ids)
            executor.submit(sonarr_check_new, plex_imdb_ids)
        except:
            logger.error(traceback.format_exc())


logger.info("plexsync started")
timer = RepeatTimer(TIME_INTERVAL, sync)
timer.run()
