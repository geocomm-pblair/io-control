from fastapi import Depends
from iocontrol.api import responses
from iocontrol.api.auth.main import security
from iocontrol.api.auth.users import User
from iocontrol.fastapi import APIRouter

router = APIRouter(
    tags=["auth"],
    dependencies=[],
)


@router.get(
    "/whoami",
    name="whoami",
    response_model=User,
    response_model_by_alias=True,
    responses=responses.errors,
)
async def whoami(
    user: User = Depends(security()),
) -> User:
    """Get the current configuration."""
    return user
