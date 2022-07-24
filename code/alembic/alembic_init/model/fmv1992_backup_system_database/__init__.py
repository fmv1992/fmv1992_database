# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
import functools

import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    MetaData,
    String,
    Table,
    text,
    Text,
    UniqueConstraint,
)

Base = declarative_base()
