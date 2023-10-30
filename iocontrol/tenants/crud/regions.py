from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from iocontrol.tenants.models.regions import ReadRegion
from iocontrol.tenants.models.regions import RegionsPage
from iocontrol.tenants.orm import Region


def read(db: Session, offset: int = 0, limit: int = 100) -> RegionsPage:
    """Get a page of clouds."""
    query = db.query(Region, func.count(Region.urn).over().label("total"))
    query.order_by(Region.display_name)
    query.offset(offset).limit(limit)
    results = query.all()
    if len(results) == 0:
        return RegionsPage(offset=offset, limit=limit, total=0)
    return RegionsPage(
        offset=offset,
        limit=limit,
        total=results[0][1],
        regions=tuple(
            ReadRegion.model_validate(result[0]) for result in results
        ),
    )
