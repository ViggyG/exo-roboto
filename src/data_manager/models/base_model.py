import datetime
from typing import Any
from sqlalchemy import Integer, String, Boolean, Numeric, DateTime
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    type_annotation_map = {
        int: Integer,
        str: String,
        bool: Boolean,
        float: Numeric,
        datetime.datetime: DateTime,
    }

    def __init__(self, **kwargs: Any):
        super().__init__()

        for k, value in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, value)
            else:
                print(f"WARNING, model given unrecognized attribute {k}:{value}")
