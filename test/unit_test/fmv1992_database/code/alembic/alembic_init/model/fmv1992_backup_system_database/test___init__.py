"""Test the respective `__init__.py` file.

That file is
`code/alembic/alembic_init/model/fmv1992_backup_system_database/__init__.py`.
"""
import sys
import unittest
import os

import sqlalchemy as sa

import fmv1992_database.lib
from fmv1992_database.lib import get_fmv1992_database_engine
import fmv1992_backup_system_database
import fmv1992_books_database


class TestIdToBlob(unittest.TestCase):
    def test_id_to_blob_column_type_is_not_OID(self):
        """Assert that we are not working with the OID limited type.

        See
        `fmv1992_database:0e26200:code/alembic/alembic_init/model/fmv1992_backup_system_database/__init__.py:99`:

        > The oid type is currently implemented as an unsigned four-byte
        integer. Therefore, it is not large enough to provide database-wide
        uniqueness in large databases, or even in large individual tables.

        Due to this we had to move the `binary` column out of `id_to_binary` to
        an auxiliary table.

        """
        maybe_binary_column = (
            fmv1992_backup_system_database.IdToBlob.__table__.columns.get(
                "binary"
            )
        )
        if maybe_binary_column is None:
            pass
        else:
            self.assertNotIsInstance(
                column_binary.type, (sa.dialects.postgresql.OID,)
            )


class TestGeneralIdeas(unittest.TestCase):
    def test_pythonpath_refers_to_directories(self):
        for dir_ in filter(None, os.environ["PYTHONPATH"].split(":")):
            with self.subTest(pythonpath_dir=dir_):
                self.assertTrue(os.path.isdir(dir_))


class TestEnsureTestsExecuted(unittest.TestCase):
    def test_tests_are_done(self):
        with open(
            os.path.join("/", "tmp", ".test_semantic_python.tests_are_done"),
            "wt",
        ) as f:
            f.write("")
