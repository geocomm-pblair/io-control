from typing import Tuple

from pydantic import ConfigDict
from pydantic import Field

from iocontrol.sqa.pages import Page
from iocontrol.tenants.models.base import BaseModel


class ReadCloud(BaseModel):
    model_config = ConfigDict(frozen=True)

    urn: str = Field(description="identifies the cloud")
    display_name: str = Field(
        alias="displayName", description="the display name"
    )


class CloudsPage(Page):
    """A page of ``Cloud`` models."""

    clouds: Tuple[ReadCloud, ...] = Field(
        default_factory=tuple, description="the clouds"
    )
