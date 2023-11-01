from typing import Any
from typing import Tuple

from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic_geojson import PointModel

import iocontrol.pydantic
from iocontrol.sqa.pages import Page
from iocontrol.tenants.models.base import BaseModel
from iocontrol.tenants.models.plans import Plan


class TenantDetails(iocontrol.pydantic.BaseModel):
    """Tenant details."""

    plans: Tuple[Plan, ...] = Field(
        default_factory=tuple, description="resource plans"
    )


class Tenant(BaseModel):
    """A system tenant."""

    model_config = ConfigDict(frozen=True)

    display_name: str = Field(
        alias="displayName", description="the display name"
    )


class CreateTenant(Tenant):
    """A new system tenant."""

    location: PointModel = Field(description="the new tenant's location")


class ReadTenant(Tenant):
    """A system tenant."""

    urn: str = Field(description="identifies the tenant")
    cell_urn: str = Field(
        description="identifies the cell in which the tenant resides"
    )
    doc: TenantDetails = Field(
        default_factory=TenantDetails, description="tenant details"
    )

    @field_validator("doc", mode="before")
    def validate_doc(cls, v: Any) -> Any:
        """Validate network."""
        return v if v is not None else TenantDetails()


class TenantsPage(Page):
    """A page of ``Tenant`` models."""

    tenants: Tuple[ReadTenant, ...] = Field(
        default_factory=tuple, description="the cells"
    )
