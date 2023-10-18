from enum import Enum

from pydantic_settings import SettingsConfigDict

from iocontrol.pydantic import BaseSettings
from iocontrol.pydantic import env_prefix
from iocontrol.pydantic import Field


class DeployLevel(str, Enum):
    """
    The deployment level.

    Values can be converted to their relative integer values by casting to
    ``int``.

    DEVELOPMENT = 0
    TESTING     = 1
    STAGING:    = 2
    PRODUCTION  = 4
    """

    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

    def __int__(self):
        """Convert the value to its respective ``int`` value."""
        return {
            self.DEVELOPMENT: 0,
            self.TESTING: 1,
            self.STAGING: 2,
            self.PRODUCTION: 4,
        }[self]


class DeployPlatform(Enum):
    """The deployment platform."""

    K8S = "k8s"
    LAMBDA = "lambda"
    LOCAL = "local"


class DeployConfig(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(env_prefix=env_prefix("deploy"))

    platform: DeployPlatform = Field(
        default=DeployPlatform.LOCAL, description="the deployment platform"
    )

    level: DeployLevel = Field(
        default=DeployLevel.PRODUCTION, description="the deployment level"
    )
