from typing import Any
from typing import Mapping
from urllib.parse import parse_qs

from fastapi import Request
from starlette.types import Message


async def _set_body(request: Request, body_: bytes):
    """
    Reset the body content of a request.

    :param request: the request
    :param body_: the body
    """

    async def receive() -> Message:
        return {"type": "http.request", "body": body_}

    request._receive = receive


async def _get_body(request: Request) -> bytes:
    """Get the body from a request and reset the content."""
    body_ = await request.body()
    await _set_body(request, body_)
    return body_


async def body(request: Request, reset: bool = False) -> bytes:
    """
    Get the body of a request.

    :param request: the request
    :param reset: resets the body after reading.  This should always be
        ``True`` if called from a middleware context.
    """
    # If we're asked to reset the body contents...
    if reset:
        await _set_body(request, await request.body())
        return await _get_body(request)
    # Otherwise, just read it.
    return await request.body()


async def parse_form(
    request: Request, reset: bool = False
) -> Mapping[str, Any]:
    """
    Parse form parameters from a request body.

    :param request: the request
    :param reset: rests the body contents after reading
    """
    body_ = await body(request=request, reset=reset)
    params = parse_qs(body_)
    return {
        k: v.decode("utf-8") if isinstance(v, bytes) else v
        for k, v in {
            k1.decode("utf-8"): v1[0] if len(v1) == 1 else v1
            for k1, v1 in params.items()
        }.items()
    }


def as_bool(v: Any) -> bool:
    """Get a value as a boolean."""
    if isinstance(v, bool):
        return v
    return str(v).lower() == "true"
