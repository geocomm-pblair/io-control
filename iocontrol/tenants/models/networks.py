import ipaddress
from typing import Any

from pydantic import Field
from pydantic import field_validator

from iocontrol.tenants.models.base import BaseModel


class IPv4Network(BaseModel):
    urn: str = Field(description="uniquely identifies the block")
    network: ipaddress.IPv4Network = Field(description="the network block")

    @field_validator("network")
    def validate_network(cls, v: Any) -> Any:
        """Validate network."""
        return ipaddress.IPv4Network(str(v)) if v else v
