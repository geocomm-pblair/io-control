import logging
from functools import lru_cache

CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


@lru_cache(maxsize=1)
def level() -> int:
    """Get the current logging level value."""
    from iocontrol.config import (
        config,
    )  # Local import prevents circular dependency.

    return {
        "debug": DEBUG,
        "info": INFO,
        "warn": WARNING,
        "error": ERROR,
        "critical": CRITICAL,
    }[config().logging.level]
