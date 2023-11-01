from enum import Enum
from typing import Any
from typing import Dict
from typing import Optional

from pydantic import Field

from iocontrol.pydantic import BaseModel
from iocontrol.tenants.models.clouds import CloudUrn


class PlanCategory(Enum):
    """Plan categories."""

    cell = "cell"
    tenant = "tenant"


class Plan(BaseModel):
    """A resource plan."""

    urn: str = Field(
        description="identifies the plan type",
        pattern=r"urn:io:plan:(?P<type>cell|tenant):(?P<id>[\w_-]*)",
    )
    cloud: CloudUrn = Field(
        description="identifies the cloud used for the plan"
    )
    version: str = Field(description="the plan version")
    variables: Optional[Dict[str, Any]] = Field(
        default=None, description="plan variables"
    )

    def category(self) -> PlanCategory:
        """Get the plan category from the URN."""
        return PlanCategory[self.urn.split(":")[3]]

    def identifier(self) -> str:
        """Get the plan identifier from the URN."""
        return self.urn.split(":")[4]
