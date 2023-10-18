import logging
from functools import lru_cache
from typing import Any
from typing import Mapping
from typing import Set
from typing import Tuple

import structlog

from iocontrol.logging import levels


@lru_cache(maxsize=1)
def get_logger():
    """Get the logger."""
    from iocontrol.config import (
        config,
    )  # Local import prevents circular dependency.

    return structlog.get_logger(config().logging.logger)


def args(
    args_: Mapping[str, Any], *, exclude: Set[str] = None
) -> Mapping[str, Any]:
    """
    Clean a set of arguments for logging.

    :param args_: the argument set
    :param exclude: keys to exclude from the argument set
    :returns: the clean set
    """
    exclude_ = {"self"} | (exclude if exclude else {})
    return {k: v for k, v in args_.items() if k not in exclude_}


def debug(
    message: str, *, tags: Tuple[str, ...] = None, logger: str = None, **kwargs
):
    """
    Log a debugging message.

    :param message: the log message
    :param tags: _tags for the logged message
    :param logger: override the logger name
    """
    if levels.level() > logging.DEBUG:
        return
    (structlog.get_logger(logger) if logger else get_logger()).debug(
        message, tags=tags, **kwargs
    )


def info(
    message: str, *, tags: Tuple[str, ...] = None, logger: str = None, **kwargs
):
    """
    Log an info message.

    :param message: the log message
    :param tags: _tags for the logged message
    :param logger: override the logger name
    """
    if levels.level() > logging.INFO:
        return
    (structlog.get_logger(logger) if logger else get_logger()).info(
        message, tags=tags or tuple(), **kwargs
    )


def warn(
    message: str, *, tags: Tuple[str, ...] = None, logger: str = None, **kwargs
):
    """
    Log a warning message.

    :param message: the log message
    :param tags: _tags for the logged message
    :param logger: override the logger name
    """
    if levels.level() > logging.WARNING:
        return
    (structlog.get_logger(logger) if logger else get_logger()).warn(
        message, tags=tags or tuple(), **kwargs
    )


def error(
    message: str, *, tags: Tuple[str, ...] = None, logger: str = None, **kwargs
):
    """
    Log an error message.

    :param message: the log message
    :param tags: _tags for the logged message
    :param logger: override the logger name
    """
    if levels.level() > logging.ERROR:
        return
    (structlog.get_logger(logger) if logger else get_logger()).error(
        message, tags=tags or tuple(), **kwargs
    )


def critical(
    message: str, *, tags: Tuple[str, ...] = None, logger: str = None, **kwargs
):
    """
    Log a critical error message.

    :param message: the log message
    :param tags: _tags for the logged message
    :param logger: override the logger name
    """
    if levels.level() > logging.CRITICAL:
        return
    (structlog.get_logger(logger) if logger else get_logger()).debug(
        message, tags=tags or tuple(), **kwargs
    )


def exception(
    message: str, *, tags: Tuple[str, ...] = None, logger: str = None, **kwargs
):
    """
    Log an exception message from the exception stack.

    :param message: the log message
    :param tags: _tags for the logged message
    :param logger: override the logger name
    """
    if levels.level() > logging.ERROR:
        return
    (structlog.get_logger(logger) if logger else get_logger()).exception(
        message, tags=tags or tuple(), **kwargs
    )
