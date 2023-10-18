import logging.config
from typing import Literal

import structlog

from iocontrol.config.logging.main import LoggingConfig


def configure(
    config: LoggingConfig,
    level: Literal["debug", "info", "warn", "error", "critical"] = None,
):
    """
    Default logging configuration.

    :param config: the logging config
    :param level: override the logging level
    """
    # Resolve the logging level.
    level_ = (level or config.level).upper()
    # How shall we format timestamps?
    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
    pre_chain = [
        # Add the log level and a timestamp to the event_dict if the log
        # entry is not from structlog.
        structlog.stdlib.add_log_level,
        timestamper,
    ]
    # Perform standard logging configuration.
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "colored": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.dev.ConsoleRenderer(colors=True),
                    "foreign_pre_chain": pre_chain,
                },
            },
            "handlers": {
                "default": {
                    "level": level_,
                    "class": "logging.StreamHandler",
                    "formatter": "colored",
                }
            },
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": level_,
                    "propagate": True,
                },
            },
        }
    )
    # What structlog processors are we using?
    processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]
    # If the configuration doesn't call for "prettier" output, include the
    # standard exception formatter (which isn't a glossy as the `rich`
    # formatter, but is a bit more compact).
    if not config.prettier:
        processors.append(
            structlog.processors.format_exc_info,
        )
    # OK, let's do this.
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        # wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
