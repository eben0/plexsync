import json
from logging import Logger, getLogger
from os import environ

import lib.request as request

BASE_PATH: str = "/api/v3"
CMD_PATH: str = "/command"

TYPE_RADARR: int = 1
TYPE_SONARR: int = 2

RADARR_TOKEN: str = environ.get("RADARR_TOKEN")
RADARR_HOST: str = environ.get("RADARR_HOST", "localhost:7878")
RADARR_LIST_PATH: str = "/movie"

SONARR_TOKEN: str = environ.get("SONARR_TOKEN")
SONARR_HOST: str = environ.get("SONARR_HOST", "localhost:8989")
SONARR_LIST_PATH: str = "/series"

LABEL_MAP: dict[int, str] = {
    TYPE_RADARR: "Radarr",
    TYPE_SONARR: "Sonarr",
}

logger: Logger = getLogger(__name__)


def get_config(arr_type: int) -> dict:
    if arr_type == TYPE_RADARR:
        base_url: str = f"http://{RADARR_HOST}{BASE_PATH}".__str__()
        return {
            "token": RADARR_TOKEN,
            "list_url": f"{base_url}{RADARR_LIST_PATH}",
            "cmd_url": f"{base_url}{CMD_PATH}",
        }
    else:
        base_url: str = f"http://{SONARR_HOST}{BASE_PATH}".__str__()
        return {
            "token": SONARR_TOKEN,
            "list_url": f"{base_url}{SONARR_LIST_PATH}",
            "cmd_url": f"{base_url}{CMD_PATH}",
        }


def get_arr_imdb_ids(arr_type: int) -> list:
    config: dict = get_config(arr_type)
    res: str = request.get(
        url=config["list_url"], params={"apiKey": config["token"]}
    )
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
    j_res: dict = json.loads(res)
    return dict(j_res)


def check_new(arr_type: int, plex_imdb_ids: dict) -> bool:
    imdb_id: str
    title: str
    plex_type: str = "movie" if arr_type == TYPE_RADARR else "show"
    arr_label: str = LABEL_MAP[arr_type]
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


def radarr_check_new(plex_imdb_ids: dict) -> bool:
    return check_new(TYPE_RADARR, plex_imdb_ids)


def sonarr_check_new(plex_imdb_ids: dict) -> bool:
    return check_new(TYPE_SONARR, plex_imdb_ids)


# shortcuts
def get_raddar_imdb_ids() -> list:
    return get_arr_imdb_ids(TYPE_RADARR)


def get_sonarr_imdb_ids() -> list:
    return get_arr_imdb_ids(TYPE_SONARR)


def sync_raddar() -> dict:
    return arr_sync(TYPE_RADARR)


def sync_sonarr() -> dict:
    return arr_sync(TYPE_SONARR)
