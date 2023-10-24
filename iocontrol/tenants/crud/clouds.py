from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from iocontrol.tenants.models import CloudModelsPage
from iocontrol.tenants.models import CloudOrm
from iocontrol.tenants.models import ReadCloudModel


def read(
    db: Session, offset: int = 0, limit: int = 100
) -> CloudModelsPage:
    """Get a page of clouds."""
    # https://stackoverflow.com/questions/64371048/get-total-record-count-for-sqlalchemy-query-result-which-uses-paginationlimit
    query = db.query(CloudOrm, func.count(CloudOrm.id).over().label("total"))
    query.order_by(CloudOrm.id)
    query.offset(offset).limit(limit)
    results = query.all()
    if len(results) == 0:
        return CloudModelsPage(offset=offset, limit=limit, total=0)
    return CloudModelsPage(
        offset=offset,
        limit=limit,
        total=results[0][1],
        clouds=tuple(
            ReadCloudModel.model_validate(result[0]) for result in results
        ),
    )
