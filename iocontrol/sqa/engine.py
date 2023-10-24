import importlib
from functools import lru_cache
from typing import cast
from typing import Tuple

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from iocontrol import logging
from iocontrol.config import config
from iocontrol.logging.tags import tags
from iocontrol.meta import this
from iocontrol.sqa.models import Base
from iocontrol.strings import render


@lru_cache(maxsize=1)
def engine() -> sqlalchemy.Engine:
    """Get the SQLAlchemy engine."""
    # Import all the modules that define models.
    for module in config().sqa.models:
        mod = importlib.import_module(render(module, this=this().name))
        logging.info(
            f'Imported model module "{mod.__name__}" from "{mod.__file__}".',
            db=config().db.model_dump(),
            sqa=config().sqa.model_dump(),
            module_name=mod.__name__,
            module_file=mod.__file__,
            tags=tags(__name__),
        )
    logging.info(
        f"Creating SQLAlchemy engine for {config().db.as_sqa(hide_secrets=True)}",
        db=config().db.model_dump(),
        sqa=config().sqa.model_dump(),
        tags=tags(__name__),
    )
    # Create the engine.
    engine_ = create_engine(
        url=config().db.as_sqa(hide_secrets=False), echo=config().sqa.echo
    )
    # Build the models.
    Base.metadata.create_all(engine_)
    return engine_


@lru_cache(maxsize=1)
def session_local() -> sessionmaker[Session]:
    """Get the current SQLAlchemy session maker."""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine())
