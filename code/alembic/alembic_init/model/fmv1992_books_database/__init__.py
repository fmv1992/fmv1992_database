"""

???: `fmv1992_books:ccc6fd6:readme.md:1`.
"""
import sqlalchemy as sa

from fmv1992_database import Base, ColumnNonNull

SCHEMA = "fmv1992_books"


class Book(Base):
    __tablename__ = "book"
    __table_args__ = {"schema": SCHEMA}

    isbn13 = ColumnNonNull(
        sa.types.String(),
        primary_key=True,
        comment="""
""".strip(),
    )
    name = ColumnNonNull(
        sa.types.String(),
        comment="""
""".strip(),
    )
    citation_abbreviation = ColumnNonNull(
        sa.types.String(),
        comment="""
""".strip(),
    )
