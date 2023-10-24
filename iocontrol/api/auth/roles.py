from functools import lru_cache
from typing import List


@lru_cache(maxsize=1)
def consumers() -> List[str]:
    return [
        "Editor",
        "TenantAdmin",
        "UserAdmin",
        "Commenter",
        "Consumer",
        "Trusted",
    ]
