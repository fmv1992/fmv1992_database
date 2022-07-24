# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
import functools

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

# https://docs.sqlalchemy.org/en/14/core/type_basics.html

ColumnNonNull = functools.partial(sa.Column, nullable=False)
sa.Column = ColumnNonNull

Base = declarative_base()

_hash_xxh_example = "f6f9786af9c448d93fe0ab36821a0b17"


class IdToBlob(Base):
    __tablename__ = "id_to_binary"

    id_ = ColumnNonNull(
        sa.types.String(len(_hash_xxh_example)),
        name="id",
        primary_key=True,
        comment=f"""
Unique ID of every primary blob.

I decided to use `xxHash` for its collision resistance and speed.

Hash example: `{len(_hash_xxh_example)}` (`fmv1992_backup_system:7ec185b:pyproject.toml:1`).

# Related links:

1.  <https://github.com/Cyan4973/xxHash>.
""".strip(),
    )
    binary = ColumnNonNull(sa.types.LargeBinary())

    sa.schema.CheckConstraint(
        sa.text(f"char_length(id) = {len(_hash_xxh_example)}")
    )
