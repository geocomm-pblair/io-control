from functools import lru_cache
from typing import Tuple

from fastapi import Request

from iocontrol.strings import random


@lru_cache(maxsize=1)
def tags() -> Tuple[str, ...]:
    """Get debugging tags."""
    return ("fastapi.py",)


@lru_cache(maxsize=1)
def tracer_length() -> int:
    """Get the length of tracers."""
    return 8


def trace(request: Request) -> str:
    """
    Get the tracer for a request.

    If the request doesn't contain a tracer header, the function creates
    a new one and adds it.

    :param request: the request
    :returns: the tracer
    """
    try:
        return request.state.tracer
    except AttributeError:
        tracer_ = random(length=tracer_length())
        request.state.tracer = tracer_
        return tracer_
