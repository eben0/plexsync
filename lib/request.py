from urllib.parse import urlencode
from urllib.request import urlopen, Request


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
    httprequest = Request(url, **kwargs)
    with urlopen(httprequest) as response:
        return response.read().decode("utf-8")
