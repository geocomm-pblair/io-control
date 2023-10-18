from pathlib import Path
from typing import Optional

from iocontrol.pydantic import BaseSettings
from iocontrol.pydantic import Field


class MockSecurityConfig(BaseSettings):
    """Mock authentication and authorization configuration."""

    root: Optional[Path] = Field(
        default=None, description="the home repository for mock users"
    )

    user: Optional[str] = Field(
        default=None,
        description="identifies the user profile",
    )
