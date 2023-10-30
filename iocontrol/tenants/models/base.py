from typing import Any
from typing import Dict
from typing import Optional

from pydantic import ConfigDict
from pydantic import Field

import iocontrol.pydantic


class BaseModel(iocontrol.pydantic.BaseModel):
    """Pydantic model base class for tenant models."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    doc: Optional[Dict[str, Any]] = Field(
        default=None, description="an entity document"
    )
