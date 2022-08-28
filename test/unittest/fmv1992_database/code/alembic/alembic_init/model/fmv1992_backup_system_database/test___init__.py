import unittest

class TestX(unittest.TestCase):
    def test_fails(self):
        raise RuntimeError("Fail.")
