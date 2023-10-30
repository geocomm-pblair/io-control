import importlib
import sys
from functools import lru_cache
from typing import Any
from typing import Mapping
from typing import Optional
from typing import Type

import pydantic
import pydantic_settings
from pydantic import ConfigDict
from pydantic import Extra
from pydantic import Field
from pydantic_settings import SettingsConfigDict

from iocontrol.meta import this


@lru_cache(maxsize=1)
def env_separator() -> str:
    return "__"


@lru_cache(maxsize=1)
def env_prefix(*nested: str) -> str:
    """
    Get the metadata prefix.

    :param nested: nested namespaces
    """
    prefix = this().name.replace("-", "_")
    separator = env_separator()
    return (
        f"{prefix}{separator}{f'{separator}'.join(nested)}{separator}"
        if nested
        else f"{prefix}{separator}"
    )


@lru_cache(maxsize=2048)
def alias(field: str) -> str:
    """
    Generate an alias for a field name.

    :param field: the field name
    :returns: the alias
    """
    a = "".join(word.capitalize() for word in field.split("_"))
    return f"{a[0].lower()}{''.join(a[1:])}"


def get_value(d: Mapping[str, Any], field: str, alias_: str = None) -> Any:
    """
    Get a value from a mapping (dict) by looking for a field name or alias.

    The function first checks for the field name, then the alias.

    :param d: the mapping (dict)
    :param field: the field name
    :param alias_: the alias (if the caller does not provide a value, the
        alias is calculated using the ``alias`` function
    :returns: the value (or ``None``)
    """
    if not d:
        return None
    return d.get(field, d.get(alias_ if alias_ else alias(field)))


def pyfqn(obj) -> str:
    """
    Get the fully-qualified name (FQN) of an object's type.

    :param obj: the object
    :return: the fully-qualified type name
    """
    _cls = obj if isinstance(obj, type) else type(obj)
    return f"{_cls.__module__}.{_cls.__name__}"


def pycls(fqn: str) -> Optional[Type]:
    """
    Get the class to which a fully-qualified name (FQN) refers.

    :param fqn: the fully-qualified name of the class
    :return: the class described by the fully-qualified name (FQN)
    :raises ModuleNotFoundError: if the module is not found
    """
    # Nothing gets nothing.
    if not fqn:
        return None
    # Split up the fqn (fully-qualified name) at the dots.
    tokens = fqn.split(".")
    # Put the module name back together.
    modname = ".".join(tokens[:-1])
    # Let's get the module in which
    try:
        mod = sys.modules[modname]
    except KeyError:
        mod = importlib.import_module(modname)
    # The name of the class is the last token.  Retrieve it from the module.
    _cls = getattr(mod, tokens[-1])
    # That's our answer.
    return _cls


json_encoders = {
    # Add custom JSON encoders here.
    set: lambda s: tuple(s),
    Type: pyfqn,
    type: pyfqn,
}  #: custom JSON encoders


class BaseModel(pydantic.BaseModel):
    """Extended models Basemodel."""

    model_config = ConfigDict(
        alias_generator=alias,
        json_encoders=json_encoders,
        populate_by_name=True,
        str_strip_whitespace=True,
        use_enum_values=True,
    )


class BaseSettings(pydantic_settings.BaseSettings):
    """Extended models Basemodel."""

    model_config = SettingsConfigDict(
        populate_by_name=False,
        env_prefix=env_prefix(),
        str_strip_whitespace=True,
        frozen=True,
        json_encoders=json_encoders,
        use_enum_values=True,
    )


__all__ = [
    "alias",
    "env_prefix",
    "BaseModel",
    "BaseSettings",
    "Extra",
    "Field",
    "get_value",
    "json_encoders",
]
