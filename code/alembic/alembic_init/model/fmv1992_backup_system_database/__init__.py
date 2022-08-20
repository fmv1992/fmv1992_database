# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
import functools
import datetime as dt

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

# https://docs.sqlalchemy.org/en/14/core/type_basics.html

ColumnNonNull = functools.partial(sa.Column, nullable=False)
sa.Column = ColumnNonNull

Base = declarative_base()

_hash_xxh_example = "f6f9786af9c448d93fe0ab36821a0b17"


class Reuse(object):
    @staticmethod
    def get_id(*args, **kwargs):
        args_default = (sa.types.String(len(_hash_xxh_example)),)
        kwargs_default = {
            "name": "id",
            "primary_key": True,
            "comment": f"""
Unique ID of every primary blob.

I decided to use `xxHash` for its collision resistance and speed.

Hash example: `{len(_hash_xxh_example)}` (`fmv1992_backup_system:7ec185b:pyproject.toml:1`).

# Related links:

1.  <https://github.com/Cyan4973/xxHash>.
""".strip(),
        }

        args_final = args_default + args
        kwargs_final = kwargs_default
        kwargs_final.update(kwargs)
        return ColumnNonNull(*args_final, **kwargs_final)

    @staticmethod
    def get_timestamp(*args, **kwargs):
        args_default = (sa.types.DateTime(timezone=dt.timezone.utc),)
        kwargs_default = {
            "name": "timestamp",
            "primary_key": True,
            "comment": f"""
Timestamp associated with the backed up file/binary blob.
""".strip(),
        }

        args_final = args_default + args
        kwargs_final = kwargs_default
        kwargs_final.update(kwargs)
        return ColumnNonNull(*args_final, **kwargs_final)


class IdToBlob(Base):
    """UUID to binary blob relation.

    # Universals

    Old approach:
    `fmv1992_backup_system:7775e0e:code/alembic/alembic_init/model/fmv1992_backup_system_database/__init__.py:65`.

    *   UUID to to binary content.

        *   If `is_compressed == `True`: `binary`'s content does not match the `id`. However the decompressed value does match the `id`.

    """

    __tablename__ = "id_to_binary"
    __table_args__ = {"schema": "fmv1992_backup_system"}

    id_ = Reuse.get_id()
    is_compressed = ColumnNonNull(
        sa.types.Boolean(),
        comment="""
Tells whether the `binary` column is compressed or not.

If it is not compressed then `id = hash(binary)`. If it is compressed then `id = hash(uncompressed(binary))`.
""".strip(),
    )
    comment = ColumnNonNull(
        sa.types.String(),
        comment="""
Comment associated with the binary.
""".strip(),
        server_default=sa.text("''"),
    )
    binary = ColumnNonNull(sa.types.LargeBinary())

    sa.schema.CheckConstraint(
        sa.text(f"char_length(id) = {len(_hash_xxh_example)}")
    )


class Backups(Base):
    __tablename__ = "backups"
    __table_args__ = {"schema": "fmv1992_backup_system"}

    id_ = Reuse.get_id(
        sa.schema.ForeignKey("fmv1992_backup_system.id_to_binary.id"),
        primary_key=True,
    )
    datetime_creation = Reuse.get_timestamp()
    path = ColumnNonNull(
        sa.types.String(),
        primary_key=True,
    )


class AccessRecord(Base):
    __tablename__ = "access_record"
    __table_args__ = {"schema": "fmv1992_backup_system"}

    id_ = Reuse.get_id(
        sa.schema.ForeignKey("fmv1992_backup_system.id_to_binary.id"),
        primary_key=True,
    )
    datetime_access = Reuse.get_timestamp()
