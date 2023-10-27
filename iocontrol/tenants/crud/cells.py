from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from iocontrol.tenants.models import CellModelsPage
from iocontrol.tenants.models import CellOrm
from iocontrol.tenants.models import ReadCellModel


def read(db: Session, offset: int = 0, limit: int = 100) -> CellModelsPage:
    """Get a page of cells."""
    query = db.query(CellOrm, func.count(CellOrm.urn).over().label("total"))
    query.order_by(CellOrm.display_name)
    query.offset(offset).limit(limit)
    results = query.all()
    if len(results) == 0:
        return CellModelsPage(offset=offset, limit=limit, total=0)
    return CellModelsPage(
        offset=offset,
        limit=limit,
        total=results[0][1],
        cells=tuple(
            ReadCellModel.model_validate(result[0]) for result in results
        ),
    )
