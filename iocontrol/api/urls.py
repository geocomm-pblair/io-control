from typing import Union

from fastapi import Request
from urlpath import URL


def openapi(request: Request, as_url: bool = False) -> Union[str, URL]:
    """
    Get the OGC root URL from a request.

    :param request: the request
    :param as_url: return the root as a ``urlpath`` URL
    :returns: the root URL as a string, or a ``urlpath`` URL
    """
    url = f"{request.base_url}openapi.json"
    return URL(url) if as_url else url
