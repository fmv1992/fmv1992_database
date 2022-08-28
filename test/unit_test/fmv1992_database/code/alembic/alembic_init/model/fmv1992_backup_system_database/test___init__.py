"""Test the respective `__init__.py` file.

That file is
`code/alembic/alembic_init/model/fmv1992_backup_system_database/__init__.py`.
"""
import sys
import unittest
import os

import fmv1992_database.lib
from fmv1992_database.lib import get_fmv1992_database_engine
# import fmv1992_backup_system_database
# import fmv1992_books_database
# # IdToBlob


# class TestX(unittest.TestCase):
#     def test_fails(self):
#         pass
#         import ipdb
#         ipdb.set_trace()
#         pass
#         raise RuntimeError("Fail.")


class TestGeneralIdeas(unittest.TestCase):
    def test_pythonpath_refers_to_directories(self):
        pass
        import ipdb
        ipdb.set_trace()
        pass
        print("", file=sys.stderr)
        for dir_ in filter(None, os.environ["PYTHONPATH"].split(":")):
            with self.subTest(pythonpath_dir=dir_):
                self.assertTrue(os.path.isdir(dir_))
                print(dir_, file=sys.stderr)


class TestEnsureTestsExecuted(unittest.TestCase):
    def test_tests_are_done(self):
        with open(
            os.path.join("/", "tmp", ".test_semantic_python.tests_are_done"),
            "wt",
        ) as f:
            f.write("")
