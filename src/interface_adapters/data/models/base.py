# pylint: disable=E0213
from typing import Any

from sqlalchemy.ext.declarative import declarative_base, declared_attr

from utils import algorithms

_Base: Any = declarative_base()


class Model(_Base):
    """Provide a pattern for tablename and common attributes
    such as _created_at and _updated_at"""

    __abstract__ = True
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """Patternize the tablename based on the name of the model class"""
        tablename_camel_case = cls.__name__.replace("Model", "")
        return algorithms.to_snake_case(tablename_camel_case)
