from fastapi import Body
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
from iocontrol.tenants.crud.tenants import TenantProvisioningTask
from iocontrol.tenants.models.tenants import CreateTenant
from iocontrol.tenants.models.tenants import TenantsPage
from iocontrol.tenants.provisioning.base import Provisioner
from iocontrol.tenants.provisioning.base import ProvisioningTask
from iocontrol.tenants.provisioning.fastapi import provisioner


@router.get(
    "/",
    name="get-tenants",
    response_model=TenantsPage,
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
) -> TenantsPage:
    """Get a listing of clouds."""
    return tenants.read(db=db, limit=limit, offset=offset)


@router.post(
    "/",
    name="create-tenant",
    response_model=TenantProvisioningTask,
    response_model_by_alias=True,
    response_model_exclude_none=True,
    responses=responses.errors,
)
async def create_tenant(
    tenant: CreateTenant = Body(description="tenant details"),
    _: User = Depends(security()),
    db: Session = Depends(session),
    provisioner_: Provisioner = Depends(provisioner),
) -> ProvisioningTask:
    return provisioner_.run(task=TenantProvisioningTask(detail=tenant), db=db)
