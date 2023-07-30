import logging
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen, Request

logger = logging.getLogger()


def get(url, **kwargs) -> str:
    return request(url, method="GET", **kwargs)


def post(url, **kwargs) -> str:
    return request(url, method="POST", **kwargs)


def to_url(url, params=None) -> str:
    if isinstance(params, dict):
        return f"{url}?{urlencode(params)}".__str__()
    return url


def request(url, **kwargs) -> str:
    url = to_url(url, kwargs.pop("params"))
    data = kwargs.get("data")
    if isinstance(data, str):
        kwargs["data"] = bytes(data, "utf-8")
    try:
        httprequest = Request(url, **kwargs)
        with urlopen(httprequest) as response:
            return response.read().decode("utf-8")
    except HTTPError as e:
        logger.exception(e)
    except Exception as e:
        logger.exception(e)
    return ""
