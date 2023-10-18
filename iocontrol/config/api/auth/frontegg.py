import os
from typing import Optional

from pydantic import HttpUrl
from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from iocontrol.meta import this
from iocontrol.pydantic import BaseSettings
from iocontrol.pydantic import env_prefix
from iocontrol.pydantic import Field

# Note to the Future:  The Frontegg API uses environment variables that
# we can't override with the API calls.  So, let's synchronize their
# environment variables with our before we proceed.
try:
    os.environ["FRONTEGG_API_GATEWAY_URL"] = os.environ[
        f"{this().name}__api__auth__frontegg__api__gateway_url"
    ]
except KeyError:
    pass


class FronteggClientConfig(BaseSettings):
    """Frontegg security configuration."""

    model_config = SettingsConfigDict(
        env_prefix=env_prefix("api", "auth", "frontegg", "client")
    )

    base_url: Optional[HttpUrl] = Field(
        default=None,
        description="the Frontegg API base URL",
    )
    client_id: Optional[str] = Field(
        default=None, description="the Frontegg client identifier"
    )

    def configured(self) -> bool:
        """Determine if Frontegg has been configured."""
        return all({self.client_id is not None, self.base_url is not None})


class FronteggApiConfig(BaseSettings):
    """Frontegg API configuration."""

    model_config = SettingsConfigDict(
        env_prefix=env_prefix("api", "auth", "frontegg", "api")
    )

    gateway_url: HttpUrl = Field(
        default="https://api.frontegg.com",
        description="the Frontegg gateway URL",
    )

    api_key: Optional[SecretStr] = Field(
        default=None,
        description="the Frontegg API key",
    )

    def configured(self) -> bool:
        """Determine if Frontegg has been configured."""
        return self.api_key is not None


class FronteggConfig(BaseSettings):
    """Frontegg security configuration."""

    api: FronteggApiConfig = Field(
        default_factory=FronteggApiConfig,
        description="Frontegg API configuration",
    )
    client: FronteggClientConfig = Field(
        default_factory=FronteggClientConfig,
        description="Frontegg client configuration",
    )
