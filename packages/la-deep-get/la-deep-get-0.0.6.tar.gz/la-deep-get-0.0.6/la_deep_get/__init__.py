from typing import Any, TypeVar

T = TypeVar("T")


def dget(structure: Any, *args, default: T = None) -> Any | T | None:
    for key in args:
        try:
            structure = structure[key]
        except:
            return default

    return structure
