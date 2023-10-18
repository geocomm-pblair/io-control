import logging.config
from typing import cast
from typing import Literal

import structlog

from iocontrol.config.logging.main import LoggingConfig
from iocontrol.logging.handlers import StructlogJsonStreamHandler


def configure(
    config: LoggingConfig,
    level: Literal["debug", "info", "warn", "error", "critical"] = None,
):
    """
    12-Factor App (12fa) logging configuration.

    :param config: the logging config
    :param level: override the logging level
    """
    # What's the configured logging level?
    logging_level = (level or config.level).upper()
    handler = (
        f"{StructlogJsonStreamHandler.__module__}."
        f"{StructlogJsonStreamHandler.__name__}"
    )
    # If we're working with a 12-factor app config, configure `structlog`
    # accordingly
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "structlog_json": {
                    "format": "%(name)s %(levelname)s %(asctime)s %(message)s"
                }
            },
            "handlers": {
                "structlog_json": {
                    "class": handler,
                    "level": logging_level,
                    "formatter": "structlog_json",
                    "stream": "ext://sys.stdout",
                }
            },
            "loggers": {
                "root": {
                    "handlers": ["structlog_json"],
                    "level": logging_level,
                    "propagate": False,
                },
                "mangum": {
                    "handlers": ["structlog_json"],
                    "level": logging_level,
                    "propagate": False,
                },
                "uvicorn": {
                    "handlers": ["structlog_json"],
                    "level": logging_level,
                    "propagate": False,
                },
            },
        }
    )
    structlog.configure(
        processors=[
            # If log level is too low, abort pipeline and throw away the
            # log entry.
            structlog.stdlib.filter_by_level,
            # Add the name of the logger to the event dict.
            structlog.stdlib.add_logger_name,
            # Add the log level to the event dict.
            structlog.stdlib.add_log_level,
            # Perform %-style formatting.
            structlog.stdlib.PositionalArgumentsFormatter(),
            # Add a timestamp in ISO 8601 format.
            structlog.processors.TimeStamper(fmt="iso"),
            # If the "stack_info" key in the event dict is true, remove it
            # and render the current stack trace in the "stack" key.
            structlog.processors.StackInfoRenderer(),
            # If the "exc_info" key in the event dict is either true or
            # a sys.exc_info() tuple, remove "exc_info" and render the
            # exception with a traceback in the "exception" key.
            structlog.processors.format_exc_info,
            # If some value is in bytes, decode it to a unicode str.
            structlog.processors.UnicodeDecoder(),
            # Render the final event dict as JSON.
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        # `logger_factory` is used to create wrapped loggers that are used
        # for OUTPUT. This one returns a `logging.Logger`. The final value
        # (a JSON string) from the final processor (`JSONRenderer`) will
        # be passed to the method of the same name as that you've called
        # on the bound logger.
        logger_factory=structlog.stdlib.LoggerFactory(),
        # `wrapper_class` is the bound logger that you get back from
        # `get_logger()`. This one imitates the API of `logging.Logger`.
        wrapper_class=cast(
            structlog.typing.BindableLogger, structlog.stdlib.BoundLogger
        ),
        # Effectively freeze configuration after creating the first bound
        # logger.
        cache_logger_on_first_use=True,
    )
