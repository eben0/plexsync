import json
from logging import Logger, getLogger

import lib.request as request
from lib.constants import Servarr, Radarr, Sonarr
from lib.tools import synchronized


LABEL_MAP: dict[int, str] = {
    Radarr.TYPE: "Radarr",
    Sonarr.TYPE: "Sonarr",
}

logger: Logger = getLogger(__name__)


def get_config(arr_type: int) -> dict:
    if arr_type == Radarr.TYPE:
        base_url: str = f"{Radarr.URL}{Servarr.BASE_PATH}".__str__()
        return {
            "token": Radarr.TOKEN,
            "list_url": f"{base_url}{Radarr.LIST_PATH}",
            "cmd_url": f"{base_url}{Servarr.CMD_PATH}",
        }
    else:
        base_url: str = f"{Sonarr.URL}{Servarr.BASE_PATH}".__str__()
        return {
            "token": Sonarr.TOKEN,
            "list_url": f"{base_url}{Sonarr.LIST_PATH}",
            "cmd_url": f"{base_url}{Servarr.CMD_PATH}",
        }


def get_arr_imdb_ids(arr_type: int) -> list:
    config: dict = get_config(arr_type)
    res: str = request.get(
        url=config["list_url"], params={"apiKey": config["token"]}
    )
    if not res:
        logger.warning("%s response is empty", config["list_url"])
        return []
    j_res: list = json.loads(res)
    return list(map(lambda x: str(x.get("imdbId")), j_res))


def arr_sync(arr_type: int) -> dict:
    config: dict = get_config(arr_type)
    res: str = request.post(
        url=config["cmd_url"],
        params={"apiKey": config["token"]},
        data='{"name": "ImportListSync"}',
        headers={"Content-Type": "application/json"},
    )
    if not res:
        logger.warning("%s response is empty", config["cmd_url"])
        return {}
    j_res: dict = json.loads(res)
    return dict(j_res)


def check_new(arr_type: int, plex_imdb_ids: dict) -> bool:
    imdb_id: str
    title: str
    plex_type: str = "movie" if arr_type == Radarr.TYPE else "show"
    arr_label: str = LABEL_MAP[arr_type]
    logger.info(f"Checking for new {plex_type}s")
    arr_imdb_ids: list = get_arr_imdb_ids(arr_type)
    logger.debug(
        "Plex %ss watchlist: %s", plex_type, plex_imdb_ids.get(plex_type)
    )
    for imdb_id, title in plex_imdb_ids[plex_type].items():
        if imdb_id not in arr_imdb_ids:
            logger.info(f"New {plex_type} found in Plex watchlist: {title}")
            logger.info(f"Executing {arr_label} ImportListSync command")
            sync_result: dict = arr_sync(arr_type)
            logger.debug("%s sync result: %s", arr_label, sync_result)
            return True
    logger.info(f"{arr_label}: Nothing to sync")
    return False


@synchronized
def radarr_check_new(plex_imdb_ids: dict) -> bool:
    return check_new(Radarr.TYPE, plex_imdb_ids)


@synchronized
def sonarr_check_new(plex_imdb_ids: dict) -> bool:
    return check_new(Sonarr.TYPE, plex_imdb_ids)


# shortcuts
def get_raddar_imdb_ids() -> list:
    return get_arr_imdb_ids(Radarr.TYPE)


def get_sonarr_imdb_ids() -> list:
    return get_arr_imdb_ids(Sonarr.TYPE)


def sync_raddar() -> dict:
    return arr_sync(Radarr.TYPE)


def sync_sonarr() -> dict:
    return arr_sync(Sonarr.TYPE)
