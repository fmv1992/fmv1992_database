import unittest
import os

class TestX(unittest.TestCase):
    def test_fails(self):
        # raise RuntimeError("Fail.")
        pass

class TestEnsureTestsExecuted(unittest.TestCase):
    def test_tests_are_done(self):
        with open(os.path.join('/', 'tmp', '.test_semantic_python.tests_are_done'), 'wt') as f:
                f.write('')
