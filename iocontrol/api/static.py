from functools import lru_cache
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from iocontrol.config import config


@lru_cache(maxsize=1)
def path() -> Optional[Path]:
    """Get the path to static files."""
    config_ = config()
    # If the path to static files has been configured manually, we'll use it.
    if config_.api.static.path:
        return config_.api.static.path.expanduser().resolve()
    return Path(__file__).parent / "static"


def configure(app: FastAPI):
    """
    Configure static files.

    :param app: the FastAPI application
    """
    # Mount the static files to the application.
    app.mount(
        "/",
        StaticFiles(directory=str(path().expanduser().resolve()), html=True),
        name="static",
    )
