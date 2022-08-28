"""Common definitions for my schemas.
"""
import functools

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
import sqlalchemy as sa

ColumnNonNull = functools.partial(sa.Column, nullable=False)
sa.Column = ColumnNonNull


Base = declarative_base(metadata=MetaData(schema="public"))
