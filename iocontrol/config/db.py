from typing import Optional, Literal

from pydantic import conint
from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from iocontrol.pydantic import BaseSettings
from iocontrol.pydantic import env_prefix
from iocontrol.pydantic import Field
from iocontrol import meta


class DbConfig(BaseSettings):
    """Database connection information."""

    model_config = SettingsConfigDict(env_prefix=env_prefix("db"))

    driver: Literal["postgresql+psycopg2"] = Field(
        default="postgresql+psycopg2", description="the database driver"
    )
    host: str = Field(default="localhost", description="the database host")
    port: Optional[conint(gt=0, le=65535)] = Field(
        default=None, description="the database port"
    )
    database: Optional[str] = Field(
        default=meta.this().name, description="the connection database"
    )
    default: Optional[str] = Field(
        default=None, description="the default database"
    )
    user: Optional[str] = Field(default=None, description="the database user")
    password: Optional[SecretStr] = Field(
        default=None,
        description="the database user's password",
    )

    def as_sqa(self, hide_secrets: bool = True) -> str:
        """
        Render a SQLAlchemy connection string.

        :param hide_secrets: hide secrets in the connection string
        :returns: a SQLAlchemy connection string
        """
        parts = [f"{self.driver}://"]
        if self.user:
            if self.password:
                password = (
                    "****"
                    if hide_secrets
                    else self.password.get_secret_value()
                )
            else:
                password = None
            parts.append(
                f"{self.user}:{password}@" if password else f"{self.user}@"
            )
        parts.append(self.host)
        if self.port:
            parts.append(f":{self.port}")
        if self.database:
            parts.append(f"/{self.database}")
        return "".join(parts)
