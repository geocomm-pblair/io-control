from pathlib import Path
from typing import Optional
from typing import Tuple

from pydantic import conint
from pydantic import IPvAnyAddress
from pydantic_settings import SettingsConfigDict

from iocontrol.config.api.auth import AuthConfig
from iocontrol.meta import this
from iocontrol.pydantic import BaseSettings
from iocontrol.pydantic import env_prefix
from iocontrol.pydantic import Field


class ApiCORSConfig(BaseSettings):
    """API Cross-Origin Resource Sharing (CORS) configuration"""

    model_config = SettingsConfigDict(env_prefix=env_prefix("api", "cors"))

    allow_origins: Tuple[str, ...] = Field(
        default=("*",),
        description="origins (site URLs) that are allowed to contact the API",
    )
    #: are cookies supported for cross-origin requests?
    allow_credentials: bool = Field(
        default=True, description="allow cookies for cross-origin requests"
    )
    allow_methods: Tuple[str, ...] = Field(
        default=("*",),
        description="allowed HTTP methods",
    )
    allow_headers: Tuple[str, ...] = Field(
        default=("*",),
        description="permitted HTTP headers",
    )


class ApiStaticConfig(BaseSettings):
    """Static file configuration."""

    model_config = SettingsConfigDict(env_prefix=env_prefix("api", "static"))

    path: Optional[Path] = Field(
        default=None, description="path to static files"
    )
    index: str = Field(
        default="index.html", description="the static index file"
    )
    prefixes: Tuple[str, ...] = Field(
        default_factory=tuple,
        description="routes that should be redirected to the static index",
    )


class ApiConfig(BaseSettings):
    """API configuration settings."""

    model_config = SettingsConfigDict(env_prefix=env_prefix("api"))

    app: str = Field(
        default=f"{this().name}.api:app",
        description="the API application entry point",
    )
    auth: AuthConfig = Field(
        default_factory=AuthConfig,
        description="Authentication and authorization configuration",
    )
    bind: IPvAnyAddress = Field(
        default="127.0.0.1",
        description="the interface to which the API service binds",
    )
    cors: ApiCORSConfig = Field(
        default_factory=ApiCORSConfig, description="CORS configuration"
    )
    debug: bool = Field(default=False, description="toggle API debugging")
    port: conint(le=65535) = Field(
        default=8000, description="the post on which the API service listens"
    )
    static: ApiStaticConfig = Field(
        default_factory=ApiStaticConfig,
        description="static file configuration",
    )
