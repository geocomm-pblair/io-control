from fastapi import Depends
from fastapi import Query
from pydantic import conint
from sqlalchemy.orm import Session

from iocontrol.api import responses
from iocontrol.api.auth.main import security
from iocontrol.api.auth.users import User
from iocontrol.api.tenants.router import router
from iocontrol.sqa.fastapi import session
from iocontrol.tenants.crud import clouds
from iocontrol.tenants.pydantic.clouds import CloudsPage


@router.get(
    "/clouds",
    name="get-clouds",
    response_model=CloudsPage,
    response_model_by_alias=True,
    response_model_exclude_none=True,
    responses=responses.errors,
)
async def get_clouds(
    limit: conint(ge=0, le=10) = Query(
        default=10, description="Limit the results to this number."
    ),
    offset: conint(ge=0) = Query(
        default=0, description="Offset the results by this number."
    ),
    _: User = Depends(security()),
    db: Session = Depends(session),
) -> CloudsPage:
    """Get a listing of clouds."""
    return clouds.read(db=db, limit=limit, offset=offset)
