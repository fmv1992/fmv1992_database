"""Create the `IdToBlob` table.

Revision ID: edf0bc6f1951
Revises: 7e64e2a8f778
Create Date: 2022-08-21 20:26:54.856338

"""
from alembic import op
import sqlalchemy as sa
import datetime
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "edf0bc6f1951"
down_revision = "7e64e2a8f778"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "id_to_binary",
        sa.Column(
            "id",
            sa.String(length=32),
            nullable=False,
            comment="Unique ID of every primary blob.\n\nI decided to use `xxHash` for its collision resistance and speed.\n\nHash example: `32` (`fmv1992_database:7ec185b:pyproject.toml:1`).\n\n# Related links:\n\n1.  <https://github.com/Cyan4973/xxHash>.",
        ),
        sa.Column(
            "is_compressed",
            sa.Boolean(),
            nullable=False,
            comment="Tells whether the `binary` column is compressed or not.\n\nIf it is not compressed then `id = hash(binary)`. If it is compressed then `id = hash(uncompressed(binary))`.",
        ),
        sa.Column(
            "comment",
            sa.String(),
            server_default=sa.text("''"),
            nullable=False,
            comment="Comment associated with the binary.",
        ),
        sa.Column(
            "binary",
            postgresql.OID(),
            nullable=False,
            comment='Sequence of bytes uniquely associated with an `id`.\n\nThis is the heart of the `fmv1992_backup_system` schema.\n\n# Relevant extracts of the documentation:\n\n*   "Client applications cannot use these functions while a libpq connection is in pipeline mode.".\n\n*   How to import and export:\n\n    ```\n    Oid lo_import(PGconn *conn, const char *filename);\n    ```\n\n    ```\n    int lo_export(PGconn *conn, Oid lobjId, const char *filename);\n    ```\n\n# References:\n\n*   [Chapter 35. Large Objects](https://www.postgresql.org/docs/14/largeobjects.html).\n\n*   [F.20. lo](https://www.postgresql.org/docs/14/lo.html): `lo` stands for "Large Object".',
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="",
    )
    op.create_table(
        "access_record",
        sa.Column(
            "id",
            sa.String(length=32),
            nullable=False,
            comment="Unique ID of every primary blob.\n\nI decided to use `xxHash` for its collision resistance and speed.\n\nHash example: `32` (`fmv1992_database:7ec185b:pyproject.toml:1`).\n\n# Related links:\n\n1.  <https://github.com/Cyan4973/xxHash>.",
        ),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=datetime.timezone.utc),
            nullable=False,
            comment="Timestamp associated with the backed up file/binary blob.",
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["fmv1992_backup_system.id_to_binary.id"],
        ),
        sa.PrimaryKeyConstraint("id", "timestamp"),
        schema="fmv1992_backup_system",
    )
    op.create_table(
        "backups",
        sa.Column(
            "id",
            sa.String(length=32),
            nullable=False,
            comment="Unique ID of every primary blob.\n\nI decided to use `xxHash` for its collision resistance and speed.\n\nHash example: `32` (`fmv1992_database:7ec185b:pyproject.toml:1`).\n\n# Related links:\n\n1.  <https://github.com/Cyan4973/xxHash>.",
        ),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=datetime.timezone.utc),
            nullable=False,
            comment="Timestamp associated with the backed up file/binary blob.",
        ),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("is_symlink", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["fmv1992_backup_system.id_to_binary.id"],
        ),
        sa.PrimaryKeyConstraint("id", "timestamp", "path"),
        schema="fmv1992_backup_system",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("backups", schema="fmv1992_backup_system")
    op.drop_table("access_record", schema="fmv1992_backup_system")
    op.drop_table("id_to_binary", schema="fmv1992_backup_system")
    # ### end Alembic commands ###
