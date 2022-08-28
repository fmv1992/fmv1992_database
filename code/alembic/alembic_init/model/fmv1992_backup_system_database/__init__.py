# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
import functools
import datetime as dt

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql
from sqlalchemy.ext.declarative import declarative_base

from fmv1992_database import Base, ColumnNonNull


_hash_xxh_example = "f6f9786af9c448d93fe0ab36821a0b17"

SCHEMA = "fmv1992_backup_system"
# ✂ -----------------------------------------------------------------------------
# from sqlalchemy.schema import CreateSchema
# engine.execute(CreateSchema('my_schema'))
# ----------------------------------------------------------------------------- ✂


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

Hash example: `{len(_hash_xxh_example)}` (`fmv1992_database:7ec185b:pyproject.toml:1`).

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
        }

        args_final = args_default + args
        kwargs_final = kwargs_default
        kwargs_final.update(kwargs)
        return ColumnNonNull(*args_final, **kwargs_final)


class IdToBlob(Base):
    """UUID to binary blob relation.

    # Universals

    Old approach:
    `fmv1992_database:7775e0e:code/alembic/alembic_init/model/fmv1992_database_database/__init__.py:65`.

    *   UUID to to binary content.

        *   If `is_compressed == `True`: `binary`'s content does not match the `id`. However the decompressed value does match the `id`.

    """

    __tablename__ = "id_to_binary"
    __table_args__ = {"schema": SCHEMA}

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
    # ???: `vacuumlo`; see ref below.
    #
    # ???: `alembic` does not support large objects`oid`; see <https://www.postgresql.org/docs/14/lo-funcs.html> and <https://stackoverflow.com/a/60569286/5544140>.
    #
    # Problem: <https://www.postgresql.org/docs/current/datatype-oid.html>:
    #
    # > The oid type is currently implemented as an unsigned four-byte integer.
    # Therefore, it is not large enough to provide database-wide uniqueness in
    # large databases, or even in large individual tables.
    #
    # # OID: <sqlalchemy.dialects.postgresql.OID>.
    binary = ColumnNonNull(
        sqlalchemy.dialects.postgresql.OID(),
        comment="""
**On 2022-08-28 I found out that large objects use OIDs, and that [OIDs are limited](https://www.postgresql.org/docs/current/datatype-oid.html):

> The oid type is currently implemented as an unsigned four-byte integer. Therefore, it is not large enough to provide database-wide uniqueness in large databases, or even in large individual tables.

* * *

Sequence of bytes uniquely associated with an `id`.

This is the heart of the `fmv1992_backup_system` schema.

# Relevant extracts of the documentation:

*   "Client applications cannot use these functions while a libpq connection is in pipeline mode.".

*   How to import and export:

    ```
    Oid lo_import(PGconn *conn, const char *filename);
    ```

    ```
    int lo_export(PGconn *conn, Oid lobjId, const char *filename);
    ```

# References:

*   [Chapter 35. Large Objects](https://www.postgresql.org/docs/14/largeobjects.html).

*   [F.20. lo](https://www.postgresql.org/docs/14/lo.html): `lo` stands for "Large Object".
""".strip(),
    )

    sa.schema.CheckConstraint(
        sa.text(f"char_length(id) = {len(_hash_xxh_example)}")
    )


class Backup(Base):
    __tablename__ = "backup"
    __table_args__ = {"schema": SCHEMA}

    id_ = Reuse.get_id(
        sa.schema.ForeignKey("fmv1992_backup_system.id_to_binary.id"),
        primary_key=True,
    )
    datetime_creation = Reuse.get_timestamp(
        comment=f"""
Timestamp associated with the backed up file/binary blob.
""".strip()
    )
    path = ColumnNonNull(
        sa.types.String(),
        primary_key=True,
    )
    is_symlink = ColumnNonNull(sa.types.Boolean())


class AccessRecord(Base):
    __tablename__ = "access_record"
    __table_args__ = {"schema": SCHEMA}

    id_ = Reuse.get_id(
        sa.schema.ForeignKey("fmv1992_backup_system.id_to_binary.id"),
        primary_key=True,
    )
    datetime_access = Reuse.get_timestamp(
        comment=f"""
Timestamp at which a binary file was accessed.
""".strip()
    )
