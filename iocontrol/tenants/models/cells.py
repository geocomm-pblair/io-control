from typing import Any
from typing import Tuple

from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator

import iocontrol.pydantic
from iocontrol.sqa.pages import Page
from iocontrol.tenants.models.base import BaseModel
from iocontrol.tenants.models.plans import Plan
from iocontrol.tenants.models.regions import ReadRegion


class CellDetails(iocontrol.pydantic.BaseModel):
    """Tenant details."""

    plans: Tuple[Plan, ...] = Field(
        default_factory=tuple, description="resource plans"
    )


class Cell(BaseModel):
    """A cell."""

    model_config = ConfigDict(frozen=True)

    display_name: str = Field(
        alias="displayName", description="the display name"
    )
    region: ReadRegion = Field(
        description="the region in which the cell resides"
    )
    doc: CellDetails = Field(
        default_factory=CellDetails, description="tenant details"
    )

    @field_validator("doc", mode="before")
    def validate_doc(cls, v: Any) -> Any:
        """Validate network."""
        return v if v is not None else CellDetails()


class ReadCell(Cell):
    """A cell."""

    urn: str = Field(description="identifies the cell")


class CellsPage(Page):
    """A page of ``Cell`` models."""

    cells: Tuple[ReadCell, ...] = Field(
        default_factory=tuple, description="the cells"
    )
