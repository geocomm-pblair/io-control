from typing import Tuple

from pydantic import ConfigDict
from pydantic import Field

from iocontrol.sqa.pages import Page
from iocontrol.tenants.models.base import BaseModel


class ReadRegion(BaseModel):
    model_config = ConfigDict(frozen=True)

    urn: str = Field(description="uniquely identifies the region")
    display_name: str = Field(
        alias="displayName", description="the display name"
    )
    cloud_urn: str = Field(description="the cloud that hosts the region")
    # cells: Optional[Tuple["ReadCellModel", ...]] = Field(
    #     default=None,
    #     description="These are the cells presently hosted in this region.",
    # )


class RegionsPage(Page):
    """A page of ``Region`` models."""

    regions: Tuple[ReadRegion, ...] = Field(
        default_factory=tuple, description="the regions"
    )
