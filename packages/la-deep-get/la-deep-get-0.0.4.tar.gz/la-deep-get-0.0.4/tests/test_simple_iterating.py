import unittest
from unittest import TestCase

from la_deep_get import dget


class TestSimpleIterating(TestCase):
    def test_string(self):
        string = "test"

        assert dget(string, 0) == "t"
        assert dget(string, 1) == "e"
        assert dget(string, 2) == "s"
        assert dget(string, 3) == "t"
        assert dget(string, 4) == None
        assert dget(string, -1) == "t"
        assert dget(string, -2) == "s"
        assert dget(string, -3) == "e"
        assert dget(string, -4) == "t"

    def test_list(self):
        list_ = [1, 2, 3, 4]

        assert dget(list_, 0) == 1
        assert dget(list_, 1) == 2
        assert dget(list_, 2) == 3
        assert dget(list_, 3) == 4

    def test_dict(self):
        dict_ = {"foo": "bar", 10: 5, 0.5: 4.2}

        assert dget(dict_, "foo") == "bar"
        assert dget(dict_, 10) == 5
        assert dget(dict_, 0.5) == 4.2


if __name__ == "__main__":
    unittest.main()
