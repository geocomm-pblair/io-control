from typing import Any
from typing import Dict
from typing import Optional

from pydantic import Field

from iocontrol.pydantic import BaseModel
from iocontrol.tenants.models.clouds import CloudUrn


class Plan(BaseModel):
    """A resource plan."""

    cloud: CloudUrn = Field()
    urn: str = Field(description="identifies the plan type")
    version: str = Field(description="the plan version")
    variables: Optional[Dict[str, Any]] = Field(
        default=None, description="plan variables"
    )
