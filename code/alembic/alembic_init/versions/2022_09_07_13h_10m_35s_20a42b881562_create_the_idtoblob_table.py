"""Create the `IdToBlob` table.

Revision ID: 20a42b881562
Revises: cfaee594661a
Create Date: 2022-09-07 13:10:35.535052

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = "20a42b881562"
down_revision = "cfaee594661a"
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
        sa.PrimaryKeyConstraint("id"),
        schema="fmv1992_backup_system",
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
            comment="Timestamp at which a binary file was accessed.",
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["fmv1992_backup_system.id_to_binary.id"],
        ),
        sa.PrimaryKeyConstraint("id", "timestamp"),
        schema="fmv1992_backup_system",
    )
    op.create_table(
        "backup",
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
    op.create_table(
        "id_to_blob_auxiliary_table",
        sa.Column(
            "id",
            sa.String(length=32),
            nullable=False,
            comment="Unique ID of every primary blob.\n\nI decided to use `xxHash` for its collision resistance and speed.\n\nHash example: `32` (`fmv1992_database:7ec185b:pyproject.toml:1`).\n\n# Related links:\n\n1.  <https://github.com/Cyan4973/xxHash>.",
        ),
        sa.Column(
            "part",
            sa.Integer(),
            nullable=False,
            comment="Part number starting from zero.",
        ),
        sa.Column(
            "binary",
            sa.LargeBinary(),
            nullable=False,
            comment='**On 2022-08-28 I found out that large objects use OIDs, and that [OIDs are limited](https://www.postgresql.org/docs/current/datatype-oid.html):\n\n> The oid type is currently implemented as an unsigned four-byte integer. Therefore, it is not large enough to provide database-wide uniqueness in large databases, or even in large individual tables.\n\n* * *\n\nSequence of bytes uniquely associated with an `id`.\n\nThis is the heart of the `fmv1992_backup_system` schema.\n\n# Relevant extracts of the documentation:\n\n*   "Client applications cannot use these functions while a libpq connection is in pipeline mode.".\n\n*   How to import and export:\n\n    ```\n    Oid lo_import(PGconn *conn, const char *filename);\n    ```\n\n    ```\n    int lo_export(PGconn *conn, Oid lobjId, const char *filename);\n    ```\n\n# References:\n\n*   [Chapter 35. Large Objects](https://www.postgresql.org/docs/14/largeobjects.html).\n\n*   [F.20. lo](https://www.postgresql.org/docs/14/lo.html): `lo` stands for "Large Object".',
        ),
        sa.ForeignKeyConstraint(
            ["id"],
            ["fmv1992_backup_system.id_to_binary.id"],
        ),
        sa.PrimaryKeyConstraint("id", "part"),
        schema="fmv1992_backup_system",
    )
    op.alter_column(
        "book",
        "isbn13",
        existing_type=sa.VARCHAR(),
        comment="",
        existing_nullable=False,
        schema="fmv1992_books",
    )
    op.alter_column(
        "book",
        "name",
        existing_type=sa.VARCHAR(),
        comment="",
        existing_nullable=False,
        schema="fmv1992_books",
    )
    op.alter_column(
        "book",
        "citation_abbreviation",
        existing_type=sa.VARCHAR(),
        comment="",
        existing_nullable=False,
        schema="fmv1992_books",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "book",
        "citation_abbreviation",
        existing_type=sa.VARCHAR(),
        comment=None,
        existing_comment="",
        existing_nullable=False,
        schema="fmv1992_books",
    )
    op.alter_column(
        "book",
        "name",
        existing_type=sa.VARCHAR(),
        comment=None,
        existing_comment="",
        existing_nullable=False,
        schema="fmv1992_books",
    )
    op.alter_column(
        "book",
        "isbn13",
        existing_type=sa.VARCHAR(),
        comment=None,
        existing_comment="",
        existing_nullable=False,
        schema="fmv1992_books",
    )
    op.drop_table("id_to_blob_auxiliary_table", schema="fmv1992_backup_system")
    op.drop_table("backup", schema="fmv1992_backup_system")
    op.drop_table("access_record", schema="fmv1992_backup_system")
    op.drop_table("id_to_binary", schema="fmv1992_backup_system")
    # ### end Alembic commands ###
