"""Create the `book` table.

Revision ID: 0258c51e7b25
Revises: aaaaaaaaaaaa
Create Date: 2022-09-07 14:01:24.234027

"""
from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision = "0258c51e7b25"
down_revision = "aaaaaaaaaaaa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "book",
        sa.Column(
            "isbn13",
            sa.String(),
            nullable=False,
            comment="(non empty)\n\nhttps://github.com/sqlalchemy/alembic/issues/1085",
        ),
        sa.Column(
            "name",
            sa.String(),
            nullable=False,
            comment="(non empty)\n\nhttps://github.com/sqlalchemy/alembic/issues/1085",
        ),
        sa.Column(
            "citation_abbreviation",
            sa.String(),
            nullable=False,
            comment="(non empty)\n\nhttps://github.com/sqlalchemy/alembic/issues/1085",
        ),
        sa.PrimaryKeyConstraint("isbn13"),
        schema="fmv1992_books",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("book", schema="fmv1992_books")
    # ### end Alembic commands ###