from fastapi import Depends
from fastapi import Path
from sqlalchemy.orm import Session

from iocontrol.api import responses
from iocontrol.api.auth.main import security
from iocontrol.api.auth.users import User
from iocontrol.api.tenants.router import router
from iocontrol.sqa.fastapi import session
from iocontrol.tenants.provisioning.base import Provisioner
from iocontrol.tenants.provisioning.base import ProvisioningTask
from iocontrol.tenants.provisioning.fastapi import provisioner


@router.get(
    "/provisioning/tasks/{uid}",
    name="get-provisioning-task",
    response_model=ProvisioningTask,
    response_model_by_alias=True,
    response_model_exclude_none=True,
    responses=responses.errors,
)
async def get_provisioning_task(
    uid: str = Path(description="the provisioning task identifier"),
    _: User = Depends(security()),
    db: Session = Depends(session),
    provisioner_: Provisioner = Depends(provisioner),
) -> ProvisioningTask:
    """Get a listing of clouds."""
    return await provisioner_.task(uid=uid, db=db)
