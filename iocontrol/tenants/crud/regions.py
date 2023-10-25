from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from iocontrol.tenants.models import ReadRegionModel
from iocontrol.tenants.models import RegionModelsPage
from iocontrol.tenants.models import RegionOrm


def read(
    db: Session, offset: int = 0, limit: int = 100
) -> RegionModelsPage:
    """Get a page of clouds."""
    query = db.query(RegionOrm, func.count(RegionOrm.id).over().label("total"))
    query.order_by(RegionOrm.name)
    query.offset(offset).limit(limit)
    results = query.all()
    if len(results) == 0:
        return RegionModelsPage(offset=offset, limit=limit, total=0)
    return RegionModelsPage(
        offset=offset,
        limit=limit,
        total=results[0][1],
        regions=tuple(
            ReadRegionModel.model_validate(result[0]) for result in results
        ),
    )
