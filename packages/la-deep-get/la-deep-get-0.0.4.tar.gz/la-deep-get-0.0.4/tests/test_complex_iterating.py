import unittest
from unittest import TestCase

from la_deep_get import dget


class TestComplexIterating(TestCase):
    def test_dict(self):
        dict_ = {
            "first": [
                "alpha",
                "beta",
                "charles",
            ],
            "second": {
                "primeiro": [
                    "one",
                    "two",
                    "three",
                ],
                "segundo": {
                    "um": "start",
                    "dois": "middle",
                    "três": "end",
                }
            }
        }

        assert isinstance(dget(dict_, "first"), list)
        assert dget(dict_, "first", 0) == dict_["first"][0]
        assert dget(dict_, "first", 1) == dict_["first"][1]
        assert dget(dict_, "first", 2) == dict_["first"][2]

        assert isinstance(dget(dict_, "first", 0), str)
        assert dget(dict_, "first", 0, 0) == dict_["first"][0][0]
        assert dget(dict_, "first", 0, 1) == dict_["first"][0][1]
        assert dget(dict_, "first", 0, 2) == dict_["first"][0][2]

        assert isinstance(dget(dict_, "second"), dict)
        assert dget(dict_, "second", "primeiro") == dict_["second"]["primeiro"]
        assert dget(dict_, "second", "segundo") == dict_["second"]["segundo"]

        assert isinstance(dget(dict_, "second", "primeiro"), list)
        assert dget(dict_, "second", "primeiro", 0) == dict_["second"]["primeiro"][0]
        assert dget(dict_, "second", "primeiro", 1) == dict_["second"]["primeiro"][1]
        assert dget(dict_, "second", "primeiro", 2) == dict_["second"]["primeiro"][2]

        assert isinstance(dget(dict_, "second", "segundo"), dict)
        assert dget(dict_, "second", "segundo", "um") == dict_["second"]["segundo"]["um"]
        assert dget(dict_, "second", "segundo", "dois") == dict_["second"]["segundo"]["dois"]
        assert dget(dict_, "second", "segundo", "três") == dict_["second"]["segundo"]["três"]

        # Test not finding

        assert dget(dict_, "first", 4) == None
        assert dget(dict_, "first", 0, 5) == None
        assert dget(dict_, "second", "terceiro") == None
        assert dget(dict_, "second", "primeiro", 3) == None
        assert dget(dict_, "second", "segundo", "quatro") == None
    
    def test_list(self):
        list_ = [
            [
                "first",
                "second",
                "third",
            ],
            {
                "primeiro": [
                    "alpha",
                    "beta",
                    "charles",
                ],
                "segundo": {
                    "um": "start",
                    "dois": "middle",
                    "três": "end",
                },
            }
        ]

        assert isinstance(dget(list_, 0), list)
        assert dget(list_, 0, 0) == list_[0][0]
        assert dget(list_, 0, 1) == list_[0][1]
        assert dget(list_, 0, 2) == list_[0][2]

        assert isinstance(dget(list_, 1), dict)
        assert dget(list_, 1, "primeiro") == list_[1]["primeiro"]
        assert dget(list_, 1, "segundo") == list_[1]["segundo"]

        assert isinstance(dget(list_, 1, "primeiro"), list)
        assert dget(list_, 1, "primeiro", 0) == list_[1]["primeiro"][0]
        assert dget(list_, 1, "primeiro", 1) == list_[1]["primeiro"][1]
        assert dget(list_, 1, "primeiro", 2) == list_[1]["primeiro"][2]

        assert isinstance(dget(list_, 1, "segundo"), dict)
        assert dget(list_, 1, "segundo", "um") == list_[1]["segundo"]["um"]
        assert dget(list_, 1, "segundo", "dois") == list_[1]["segundo"]["dois"]
        assert dget(list_, 1, "segundo", "três") == list_[1]["segundo"]["três"]

        # Test not finding

        assert dget(list_, 0, 3) == None
        assert dget(list_, 1, "terceiro") == None
        assert dget(list_, 1, "primeiro", 3) == None
        assert dget(list_, 1, "segundo", "quatro") == None

if __name__ == "__main__":
    unittest.main()
