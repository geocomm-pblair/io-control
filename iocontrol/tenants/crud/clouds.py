from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from iocontrol.tenants.models.clouds import CloudsPage
from iocontrol.tenants.models.clouds import ReadCloud
from iocontrol.tenants.orm import Cloud


def read(db: Session, offset: int = 0, limit: int = 100) -> CloudsPage:
    """Get a page of clouds."""
    query = db.query(Cloud, func.count(Cloud.urn).over().label("total"))
    query.order_by(Cloud.display_name)
    query.offset(offset).limit(limit)
    results = query.all()
    if len(results) == 0:
        return CloudsPage(offset=offset, limit=limit, total=0)
    return CloudsPage(
        offset=offset,
        limit=limit,
        total=results[0][1],
        clouds=tuple(
            ReadCloud.model_validate(result[0]) for result in results
        ),
    )
