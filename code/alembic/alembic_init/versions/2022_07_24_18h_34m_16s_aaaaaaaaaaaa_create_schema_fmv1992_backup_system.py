"""Create the `fmv1992_backup_system` schema.

Revision ID: aaaaaaaaaaaa
Revises:
Create Date: 2022-08-21T17:30:47-0300

"""
from alembic import op
import sqlalchemy as sa

import fmv1992_backup_system_database
import fmv1992_books_database

# revision identifiers, used by Alembic.
revision = "aaaaaaaaaaaa"
down_revision = "7e64e2a8f778"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    for schema_ in [
        fmv1992_backup_system_database.SCHEMA,
        fmv1992_books_database.SCHEMA,
    ]:
        op.execute(f'create schema "{schema_}";')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    for schema_ in [
        fmv1992_backup_system_database.SCHEMA,
        fmv1992_books_database.SCHEMA,
    ]:
        op.execute(f'drop schema "{schema_}";')
    # ### end Alembic commands ###
