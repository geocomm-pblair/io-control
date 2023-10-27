from fastapi import Depends
from fastapi import Query
from pydantic import conint
from sqlalchemy.orm import Session

from iocontrol.api import responses
from iocontrol.api.auth.main import security
from iocontrol.api.auth.users import User
from iocontrol.api.tenants.router import router
from iocontrol.sqa.fastapi import session
from iocontrol.tenants.crud import tenants
from iocontrol.tenants.models import TenantModelsPage


@router.get(
    "/",
    name="get-tenants",
    response_model=TenantModelsPage,
    response_model_by_alias=True,
    response_model_exclude_none=True,
    responses=responses.errors,
)
async def get_tenants(
    limit: conint(ge=0, le=10) = Query(
        default=10, description="Limit the results to this number."
    ),
    offset: conint(ge=0) = Query(
        default=0, description="Offset the results by this number."
    ),
    _: User = Depends(security()),
    db: Session = Depends(session),
) -> TenantModelsPage:
    """Get a listing of clouds."""
    return tenants.read(db=db, limit=limit, offset=offset)
