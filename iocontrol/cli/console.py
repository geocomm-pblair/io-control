import json
from typing import List
from typing import Union

import rich
from pydantic import BaseModel
from rich.console import Console

from iocontrol.errors import AppException
from iocontrol.results import Result

#: the standard error console
stderr = Console(stderr=True, style="red")


def pprint(model: Union[BaseModel, List[BaseModel]], *, error: bool = False):
    """
    Pretty print a model object.

    :param model: the model object
    :param error: directs output to the error console
    """
    if isinstance(model, list):
        data = [json.loads(m.json(by_alias=True)) for m in model if m]
    else:
        exclude = (
            {"status_code"}
            if isinstance(model, (Result, AppException))
            else None
        )
        data = json.loads(model.json(by_alias=True, exclude=exclude))
    if error:
        stderr.print_json(data=data)
    rich.print_json(data=data)
