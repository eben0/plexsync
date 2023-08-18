import logging
import traceback
from concurrent.futures import ThreadPoolExecutor

from lib.constants import DEFAULT_INTERVAL, TIME_INTERVAL
from lib.plex import get_plex_wl
from lib.servarr import radarr_check_new, sonarr_check_new
from lib.tools import RepeatedTimer

logger = logging.getLogger(__name__)

JOBS = [
    radarr_check_new,
    sonarr_check_new,
]


class Executor:
    time_interval: float

    def __init__(self):
        self.pool = ThreadPoolExecutor()
        self.time_interval: float = Executor.get_time_interval()

    @staticmethod
    def get_time_interval() -> float:
        try:
            return float(TIME_INTERVAL)
        except ValueError as e:
            logger.error("Defaulting time interval to %s. %s.", DEFAULT_INTERVAL, str(e))
            return DEFAULT_INTERVAL

    def _runner(self):
        try:
            plex_media_ids: dict = get_plex_wl()
            for job in JOBS:
                self.pool.submit(job, plex_media_ids)
        except Exception:
            logger.error(traceback.format_exc())
        except KeyboardInterrupt:
            logger.info("Exit by KeyboardInterrupt")
        finally:
            logger.info(f"Sleeping for {self.time_interval} seconds")

    def run(self):
        logger.info("plexsync started")
        timer = RepeatedTimer(self.time_interval, self._runner)
        timer.run()

    @staticmethod
    def start():
        Executor().run()
