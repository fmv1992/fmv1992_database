"""Module objects for fmv1992_database."""
import os

import sqlalchemy as sa


def get_fmv1992_database_engine():
    conn_string = os.path.expandvars(
        "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
    )
    return sa.create_engine(conn_string)
