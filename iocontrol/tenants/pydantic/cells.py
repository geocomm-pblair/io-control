from typing import Tuple

from pydantic import ConfigDict
from pydantic import Field

from iocontrol.sqa.pages import Page
from iocontrol.tenants.pydantic.base import BaseModel
from iocontrol.tenants.pydantic.regions import ReadRegion


class ReadCell(BaseModel):
    model_config = ConfigDict(frozen=True)

    urn: str = Field(description="identifies the cell")
    display_name: str = Field(
        alias="displayName", description="the display name"
    )
    region: ReadRegion = Field(
        description="the region in which the cell resides"
    )


class CellsPage(Page):
    """A page of ``Cell`` models."""

    cells: Tuple[ReadCell, ...] = Field(
        default_factory=tuple, description="the cells"
    )
