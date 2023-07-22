from logging import Logger, getLogger
from os import environ
import lib.request as request
import xml.etree.ElementTree as ET

PLEX_TOKEN: str = environ.get("PLEX_TOKEN")
PLEX_DISCOVER_URL: str = "https://discover.provider.plex.tv"
PLEX_WL_URL: str = (
    f"{PLEX_DISCOVER_URL}/library/sections/watchlist/all".__str__()
)
PLEX_MD_URL: str = f"{PLEX_DISCOVER_URL}/library/metadata".__str__()
ID_PFX: str = "imdb://"

logger: Logger = getLogger(__name__)


def get_plex_wl() -> dict:
    logger.info("Getting Plex watchlist")
    collection: dict[str, dict] = {
        "movie": {},
        "show": {},
    }

    params: dict = {
        "includeFields": "key,ratingKey,title,type,year,publicPagesURL",
        "includeElements": "Guid",
        "sort": "watchlistedAt:desc",
        # "type": TYPE,
        "X-Plex-Token": PLEX_TOKEN,
    }

    res: str = request.get(url=PLEX_WL_URL, params=params)
    root: ET.XML = ET.fromstring(res)
    for child in root.findall(".//*[@title]"):
        title: str = child.attrib.get("title").strip()
        rating_key: str = child.attrib.get("ratingKey").strip()

        metadata_url: str = str(f"{PLEX_MD_URL}/{rating_key}")
        metadata_res: str = request.get(url=metadata_url, params=params)
        metadata_root: ET.XML = ET.fromstring(metadata_res)
        guids: list[ET.Element] = metadata_root.find(".//*").findall(
            ".//Guid[@id]"
        )

        for guid in guids:
            guid_id: str = guid.get("id").strip()
            if guid_id.startswith(ID_PFX):
                imdb_id: str = guid_id.replace(ID_PFX, "")
                collection[child.attrib.get("type")][imdb_id] = title
                break

    return collection
