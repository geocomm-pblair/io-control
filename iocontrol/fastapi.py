from typing import Any
from typing import Callable

from fastapi import APIRouter as FastAPIRouter
from fastapi.types import DecoratedCallable


class APIRouter(FastAPIRouter):
    """
    A FastAPI router.

    This router overrides the `api_route` method to allow callers to specify
    routes with our without trailing slashes.
    """

    def api_route(
        self, path: str, *, include_in_schema: bool = True, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        if path.endswith("/"):
            path = path[:-1]

        alternate_path = path + "/"
        super().api_route(alternate_path, include_in_schema=False, **kwargs)
        return super().api_route(
            path, include_in_schema=include_in_schema, **kwargs
        )
