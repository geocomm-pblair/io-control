import json
from datetime import datetime
from functools import lru_cache
from typing import Any

from sqlalchemy.orm import Session

from iocontrol import strings
from iocontrol.errors import NotFoundException
from iocontrol.pydantic import pycls
from iocontrol.pydantic import pyfqn
from iocontrol.sqa.errors import DataInconsistencyException
from iocontrol.tenants import orm
from iocontrol.tenants.provisioning.base import Provisioner
from iocontrol.tenants.provisioning.base import ProvisioningTask


class MockProvisioner(Provisioner):
    @classmethod
    @lru_cache(maxsize=1)
    def type(cls) -> str:
        """Get the identifier for the provisioner type."""
        return "mock"

    async def run(
        self, task: ProvisioningTask, db: Session
    ) -> ProvisioningTask:
        """
        Execute a provisioning plan.

        :param task: the plan
        :param db: a database session
        :returns: an update provisioning task
        """
        task_ = type(task)(
            **{
                **task.model_dump(),
                **dict(
                    uid=task.uid or strings.random(12), meta=task.meta or {}
                ),
            }
        )
        task_.meta["$doctype"] = pyfqn(task_)
        orm_task = orm.ProvisioningTask(
            uid=task_.uid,
            provisioner=self.type(),
            created=datetime.utcnow(),
            doc=json.loads(task_.model_dump_json()),
        )
        db.add(orm_task)
        db.commit()
        # Now pretend we outsourced the work.
        doc = dict(orm_task.doc)
        doc["state"] = "success"
        # TODO: Create the actual tenant.

        orm_task.doc = doc
        db.commit()
        # Remove the metadata from the object we return.
        return task_.model_validate({**task_.model_dump(), **dict(meta=None)})

    async def task(self, uid: str, db: Session) -> ProvisioningTask:
        """
        Get the state of a provisioning task.

        :param uid: the task identifier
        :param db: a database session
        :returns: the provisioning task definition
        """
        query = db.query(orm.ProvisioningTask).filter_by(
            uid=uid, provisioner=self.type()
        )
        orm_task = query.first()
        if not orm_task:
            raise NotFoundException(
                f'Task "{uid}" was not found by the '
                f'"{self.type()}" provisioner.'
            )
        doc = dict(orm_task.doc)
        doctype = doc.get("meta", {}).get("$doctype")
        doccls: Any = pycls(doctype)
        task = doccls.model_validate(doc)
        # Perform consistency checks between the document and the ORM fields.
        if not uid == task.uid:
            raise DataInconsistencyException(
                f'The task document identifier ("{task.uid}") does not match '
                f'the row identifier ("{uid}").'
            )
        return task
