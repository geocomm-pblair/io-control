from typing import Any
from typing import Dict
from typing import Literal
from typing import Optional

from pydantic_settings import SettingsConfigDict

from iocontrol.config.api.auth.frontegg import FronteggConfig
from iocontrol.config.api.auth.mock import MockSecurityConfig
from iocontrol.pydantic import BaseSettings
from iocontrol.pydantic import env_prefix
from iocontrol.pydantic import Field


class AuthConfig(BaseSettings):
    """Authentication and authorization configuration."""

    model_config = SettingsConfigDict(env_prefix=env_prefix("api", "auth"))

    enabled: bool = Field(default=True, description="authorization is enabled")

    provider: Literal["frontegg", "mock"] = Field(
        default="frontegg",
        description="authentication and authorization provider",
    )

    options: Dict[str, Any] = Field(
        default_factory=dict,
        description="authentication and authorization options",
    )

    mock: Optional[MockSecurityConfig] = Field(
        default_factory=MockSecurityConfig,
        description="mock authentication configuration",
    )

    frontegg: Optional[FronteggConfig] = Field(
        default_factory=FronteggConfig,
        description="Frontegg configuration",
    )
