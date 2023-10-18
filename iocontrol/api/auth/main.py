from functools import lru_cache
from typing import List

from iocontrol.api.auth import providers
from iocontrol.api.auth.providers.base import SecurityProvider
from iocontrol.config import config
from iocontrol.pydantic import pycls


@lru_cache(maxsize=1)
def provider() -> SecurityProvider:
    """Get the current security provider."""
    which = config().api.auth.provider
    class_ = pycls(
        f"{providers.__name__}.{which}."
        f"{which.capitalize()}{SecurityProvider.__name__}"
    )
    provider_ = class_()
    provider_.init()
    return provider_


def security(
    permissions: List[str] = None,
    auto_error: bool = True,
    roles: List[str] = None,
):
    """
    Secure endpoints.

    :param permissions: required permissions
    :param auto_error: raise exceptions on security failure
    :param roles: required roles
    """
    return provider().security(
        permissions=permissions, auto_error=auto_error, roles=roles
    )
