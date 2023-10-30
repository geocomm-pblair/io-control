from typing import Tuple

from pydantic import ConfigDict
from pydantic import Field

from iocontrol.sqa.pages import Page
from iocontrol.tenants.models.base import BaseModel
from iocontrol.tenants.models.cells import ReadCell


class ReadTenant(BaseModel):
    model_config = ConfigDict(frozen=True)

    urn: str = Field(description="identifies the tenant")
    display_name: str = Field(
        alias="displayName", description="the display name"
    )
    cell: ReadCell = Field(description="the cell in which the tenant resides")


class TenantsPage(Page):
    """A page of ``Tenant`` models."""

    tenants: Tuple[ReadTenant, ...] = Field(
        default_factory=tuple, description="the cells"
    )
