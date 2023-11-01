from abc import ABC
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

from pydantic import Field

from iocontrol.pydantic import BaseModel


class JsonSchemaObject(BaseModel, ABC):
    """Base class for JSON schema objects."""

    title: Optional[str] = Field(default=None, description="a title")
    type: Literal["string", "integer", "number", "object"] = Field(
        description="the field type"
    )


class JsonSchemaProperty(JsonSchemaObject):
    """A JSON schema property definition."""

    description: Optional[str] = Field(
        default=None, description="a description of the property"
    )
    format: Optional[str] = Field(default=None, description="the value format")


class JsonSchema(JsonSchemaObject):
    """A JSON schema."""

    properties: Dict[str, JsonSchemaProperty] = Field(
        default_factory=dict, description="schema properties"
    )
    required: List[str] = Field(
        default_factory=list, description="required properties"
    )
