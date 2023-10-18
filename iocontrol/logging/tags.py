from functools import lru_cache
from typing import Tuple

from iocontrol import meta


@lru_cache()
def tags(name: str, *extra) -> Tuple[str, ...]:
    """Convert a module name to a set of logging tags."""
    this = meta.this().name
    tags_ = list(
        set(
            item.lower()
            for item in name.split(".") + list(extra)
            if item != this
        )
    )
    return tuple(sorted(tags_))
