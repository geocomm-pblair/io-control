from pydantic import ConfigDict

import iocontrol.pydantic


class BaseModel(iocontrol.pydantic.BaseModel):
    """Pydantic model base class for tenant models."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
