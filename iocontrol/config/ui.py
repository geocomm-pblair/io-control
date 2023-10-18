from functools import lru_cache

from iocontrol.config.api.auth.frontegg import FronteggClientConfig
from iocontrol.pydantic import BaseModel
from iocontrol.pydantic import Field


class UiAuthConfig(BaseModel):
    """User interface (UI) authentication configuration."""

    frontegg: FronteggClientConfig = Field(
        default_factory=FronteggClientConfig,
        description="Frontegg configuration.",
    )


class UiConfig(BaseModel):
    """User interface (UI) configuration."""

    auth: UiAuthConfig = Field(
        default_factory=UiAuthConfig,
        description="UI authentication and authorization configuration.",
    )


@lru_cache(maxsize=1)
def config() -> UiConfig:
    """Get the current user interface (UI) configuration."""
    return UiConfig()
