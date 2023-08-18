from logging import Logger, getLogger
import lib.request as request
import xml.etree.ElementTree as ET

from lib.constants import Plex, ID_TYPE

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
        "X-Plex-Token": Plex.TOKEN,
    }

    res: str = request.get(url=Plex.WL_URL, params=params)
    if not res:
        logger.warning(f"{Plex.WL_URL} response is empty")
        return collection
    root: ET.XML = ET.fromstring(res)
    for child in root.findall(".//*[@title]"):
        title: str = child.attrib.get("title").strip()
        rating_key: str = child.attrib.get("ratingKey").strip()

        metadata_url: str = str(f"{Plex.MD_URL}/{rating_key}")
        metadata_res: str = request.get(url=metadata_url, params=params)
        if not metadata_res:
            logger.warning(f"{metadata_url} response is empty")
            continue
        metadata_root: ET.XML = ET.fromstring(metadata_res)
        guids: list[ET.Element] = metadata_root.find(".//*").findall(".//Guid[@id]")
        id_prefix = f"{ID_TYPE}://"

        for guid in guids:
            guid_id: str = guid.get("id").strip()
            if guid_id.startswith(id_prefix):
                media_id: str = guid_id.replace(id_prefix, "")
                collection[child.attrib.get("type")][media_id] = title
                break

    return collection
