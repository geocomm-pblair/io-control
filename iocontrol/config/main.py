from functools import lru_cache
from pathlib import Path

from iocontrol import meta
from iocontrol.config.api import ApiConfig
from iocontrol.config.db import DbConfig
from iocontrol.config.deploy import DeployConfig
from iocontrol.config.logging import LoggingConfig
from iocontrol.config.sqa import SQLAlchemyConfig
from iocontrol.pydantic import BaseSettings
from iocontrol.pydantic import Field


class Config(BaseSettings):
    """Application configuration."""

    home: Path = Field(
        default=f"~/.{meta.this().name}",
        description="the local home directory",
    )
    api: ApiConfig = Field(
        default_factory=ApiConfig, description="API configuration"
    )
    db: DbConfig = Field(
        default_factory=DbConfig, description="Database configuration"
    )
    deploy: DeployConfig = Field(
        default_factory=DeployConfig, description="deployment configuration"
    )
    logging: LoggingConfig = Field(
        default_factory=LoggingConfig,
        description="logging configuration",
    )
    sqa: SQLAlchemyConfig = Field(
        default_factory=SQLAlchemyConfig,
        description="SQL Alchemy configuration",
    )


@lru_cache(maxsize=1)
def config() -> Config:
    """Get the current application configuration."""
    return Config()
