from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from iocontrol.tenants.models import ReadTenantModel
from iocontrol.tenants.models import TenantModelsPage
from iocontrol.tenants.models import TenantOrm


def read(db: Session, offset: int = 0, limit: int = 100) -> TenantModelsPage:
    """Get a page of cells."""
    query = db.query(
        TenantOrm, func.count(TenantOrm.urn).over().label("total")
    )
    query.order_by(TenantOrm.display_name)
    query.offset(offset).limit(limit)
    results = query.all()
    if len(results) == 0:
        return TenantModelsPage(offset=offset, limit=limit, total=0)
    return TenantModelsPage(
        offset=offset,
        limit=limit,
        total=results[0][1],
        tenants=tuple(
            ReadTenantModel.model_validate(result[0]) for result in results
        ),
    )
