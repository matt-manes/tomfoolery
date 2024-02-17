from typing import Any, Callable


def normalize_key(key: str) -> str:
    """Convert `key` to a valid Python variable name."""
    return key.replace(" ", "_").replace("-", "_").lower()


def key_to_classname(key: str) -> str:
    """Convert `key` to a valid Python class name."""
    return "".join(word.capitalize() for word in normalize_key(key).split("_"))


def build_type(obj: Any, optional: bool = False) -> str:
    """Return type string for `obj`.

    Lists and tuples will have internal types listed.

    If `optional` is `True`, the type will be enclosed with `Optional[]`.

    >>> l = [1,"2"]
    >>> build_type(l)
    >>> 'Optional[list[int, str]]'"""
    name: Callable[[Any], str] = lambda obj: type(obj).__name__
    type_ = (
        f"{name(obj)}[{'|'.join(sorted(set(name(item) for item in obj)))}]"
        if type(obj) in [list, tuple]
        else name(obj)
    )
    return f"Optional[{type_}]" if optional else type_
