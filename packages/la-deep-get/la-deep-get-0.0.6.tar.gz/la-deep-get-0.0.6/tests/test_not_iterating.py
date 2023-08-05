import unittest
from unittest import TestCase

from la_deep_get import dget


class TestNotIterating(TestCase):
    def test_int(self):
        assert dget(10) == 10
    
    def test_float(self):
        assert dget(10.5) == 10.5
    
    def test_None(self):
        assert dget(None) == None
    
    def test_string(self):
        assert dget("Foobar") == "Foobar"
    
    def test_list(self):
        assert dget([1,2,3]) == [1,2,3]
    
    def test_string(self):
        assert dget({"key": "value"}) == {"key": "value"}


if __name__ == "__main__":
    unittest.main()