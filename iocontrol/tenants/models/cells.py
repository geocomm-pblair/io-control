from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple

from pydantic import ConfigDict
from pydantic import Field

from iocontrol.sqa.pages import Page
from iocontrol.tenants.models.base import BaseModel


class Cell(BaseModel):
    """A cell."""

    model_config = ConfigDict(frozen=True)

    display_name: str = Field(
        alias="displayName", description="the display name"
    )
    region_urn: str = Field(
        description="identifies the region in which the cell resides"
    )


class ReadCell(Cell):
    """A cell."""

    urn: str = Field(description="identifies the cell")

    doc: Optional[Dict[str, Any]] = Field(
        default=None, description="tenant details"
    )


class CellsPage(Page):
    """A page of ``Cell`` models."""

    cells: Tuple[ReadCell, ...] = Field(
        default_factory=tuple, description="the cells"
    )
