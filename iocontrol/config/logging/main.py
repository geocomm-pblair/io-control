from importlib import import_module
from typing import Literal
from typing import Optional

import structlog
from pydantic_settings import SettingsConfigDict

from iocontrol import logging
from iocontrol.meta import this
from iocontrol.pydantic import BaseSettings
from iocontrol.pydantic import env_prefix
from iocontrol.pydantic import Field

# logging profiles
Profiles = Literal["12fa", "cli", "default"]  # TODO: Use enums

# logging levels
Levels = Literal[
    "debug", "info", "warn", "error", "critical"
]  # TODO: Use enums


class LoggingConfig(BaseSettings):
    """Logging configuration."""

    model_config = SettingsConfigDict(env_prefix=env_prefix("logging"))

    level: Levels = Field(default="error", description="the logging level")
    logger: Optional[str] = Field(
        default=this().name, description="the application logger's name"
    )
    profile: Profiles = Field(
        default="default", description="the logger profile"
    )
    prettier: bool = Field(default=True, description="prettier logging output")


def configure(profile: str = None):
    """
    Configure logging.

    :param profile: the logging configuration
    """
    from iocontrol.config.main import config

    config_ = config()
    profile_ = profile or config_.logging.profile

    reconfiguring = structlog.is_configured()

    parent = ".".join(__name__.split(".")[:-1])
    package = f"{parent}.profiles"
    mod = import_module(name=f".{profile_}", package=package)
    mod.configure(config_.logging)
    verb = "Re-configured" if reconfiguring else "Configured"
    logging.debug(
        f'{verb} logging for the "{profile_}" profile.',
        profile=profile_,
        reconfigured=reconfiguring,
        tags=("logging",),
    )
