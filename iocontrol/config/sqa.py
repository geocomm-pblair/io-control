from typing import Optional, Literal, Tuple

from pydantic import conint
from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from iocontrol.pydantic import BaseSettings
from iocontrol.pydantic import env_prefix
from iocontrol.pydantic import Field


class SQLAlchemyConfig(BaseSettings):
    """SQLAlchemy connection information."""

    model_config = SettingsConfigDict(env_prefix=env_prefix("sql"))

    models: Tuple[str] = Field(
        default=("{{this}}.tenants.models",), description="model libraries"
    )

    echo: bool = Field(
        default=False,
        description="Echo SQL emitted by connections to standard out.",
    )
