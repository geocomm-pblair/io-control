from ipaddress import IPv4Network
from typing import Any

from pydantic import Field
from pydantic import field_validator

from iocontrol.tenants.pydantic.base import BaseModel


class ReadIpV4BlockModel(BaseModel):
    urn: str = Field(description="uniquely identifies the block")
    network: IPv4Network = Field(description="the network block")

    @field_validator("network")
    def validate_network(cls, v: Any) -> Any:
        """Validate network."""
        return IPv4Network(str(v)) if v else v
