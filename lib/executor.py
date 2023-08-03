import logging
import traceback
from concurrent.futures import ThreadPoolExecutor

from lib.constants import TIME_INTERVAL
from lib.plex import get_plex_wl
from lib.servarr import radarr_check_new, sonarr_check_new
from lib.tools import RepeatedTimer

logger = logging.getLogger(__name__)

JOBS = [
    radarr_check_new,
    sonarr_check_new,
]


class Executor:
    def __init__(self):
        self.pool = ThreadPoolExecutor()

    def _runner(self):
        try:
            plex_imdb_ids: dict = get_plex_wl()
            for job in JOBS:
                self.pool.submit(job, plex_imdb_ids)
        except Exception:
            logger.error(traceback.format_exc())
        except KeyboardInterrupt:
            logger.info("Exit by KeyboardInterrupt")
        finally:
            logger.info(f"Sleeping for {TIME_INTERVAL} seconds")

    def run(self):
        logger.info("plexsync started")
        timer = RepeatedTimer(TIME_INTERVAL, self._runner)
        timer.run()

    @staticmethod
    def start():
        Executor().run()
