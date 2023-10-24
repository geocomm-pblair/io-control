from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

#: base class for all SQLAlchemy models
Base = declarative_base()
