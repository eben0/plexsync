from os import environ

__DEFAULT_INTERVAL__: float = 60.0
TIME_INTERVAL: float = float(environ.get("TIME_INTERVAL", __DEFAULT_INTERVAL__))


class Plex:
    TOKEN: str = environ.get("PLEX_TOKEN")
    DISCOVER_URL: str = "https://discover.provider.plex.tv"
    WL_URL: str = f"{DISCOVER_URL}/library/sections/watchlist/all".__str__()
    MD_URL: str = f"{DISCOVER_URL}/library/metadata".__str__()
    ID_PFX: str = "imdb://"


class Servarr:
    BASE_PATH: str = "/api/v3"
    CMD_PATH: str = "/command"


class Radarr:
    TYPE: int = 1
    TOKEN: str = environ.get("RADARR_TOKEN")
    URL: str = environ.get("RADARR_URL", "http://localhost:7878")
    LIST_PATH: str = "/movie"


class Sonarr:
    TYPE: int = 2
    TOKEN: str = environ.get("SONARR_TOKEN")
    URL: str = environ.get("SONARR_URL", "http://localhost:8989")
    LIST_PATH: str = "/series"
