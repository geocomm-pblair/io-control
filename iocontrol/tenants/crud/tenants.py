from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from iocontrol.tenants.models.tenants import ReadTenant
from iocontrol.tenants.models.tenants import TenantsPage
from iocontrol.tenants.orm import Tenant


def read(db: Session, offset: int = 0, limit: int = 100) -> TenantsPage:
    """Get a page of cells."""
    query = db.query(Tenant, func.count(Tenant.urn).over().label("total"))
    query.order_by(Tenant.display_name)
    query.offset(offset).limit(limit)
    results = query.all()
    if len(results) == 0:
        return TenantsPage(offset=offset, limit=limit, total=0)
    return TenantsPage(
        offset=offset,
        limit=limit,
        total=results[0][1],
        tenants=tuple(
            ReadTenant.model_validate(result[0]) for result in results
        ),
    )
