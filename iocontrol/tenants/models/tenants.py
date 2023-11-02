from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple

from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator
from pydantic_geojson import PointModel

from iocontrol import strings
from iocontrol.sqa.pages import Page
from iocontrol.tenants.models.base import BaseModel


class Tenant(BaseModel):
    """A system tenant."""

    model_config = ConfigDict(frozen=True)

    urn: str = Field(
        description="identifies the tenant",
        pattern=r"urn:io:tenant:(?P<id>[\w_-]*)",
    )
    display_name: str = Field(
        alias="displayName", description="the display name"
    )


class CreateTenant(Tenant):
    """A new system tenant."""

    urn: Optional[str] = Field(default=None, pattern=r"urn:io:tenant:[\w_-]*")
    location: PointModel = Field(description="the new tenant's location")

    @model_validator(mode="before")
    def validate_urn(cls, data: Any) -> Any:
        """
        Validate the ``urn`` field.

        The function supplies a value based on the display name if no ``urn``
        value is present in the arguments.
        """
        urn = data.get("urn")
        if urn:
            return data
        data_ = dict(data)
        display_name = data.get("displayName", data.get("display_name"))
        data_["urn"] = f"urn:io:tenant:{strings.urn(display_name)}"
        return data_


class ReadTenant(Tenant):
    """A system tenant."""

    cell_urn: str = Field(
        description="identifies the cell in which the tenant resides"
    )
    doc: Optional[Dict[str, Any]] = Field(
        default=None, description="tenant details"
    )


class TenantsPage(Page):
    """A page of ``Tenant`` models."""

    tenants: Tuple[ReadTenant, ...] = Field(
        default_factory=tuple, description="the cells"
    )
