import datetime
from .namespace import namespaced as namespaced
from _typeshed import Incomplete
from openpyxl import DEBUG as DEBUG
from openpyxl.utils.datetime import from_ISO8601 as from_ISO8601

class Descriptor:
    name: Incomplete
    def __init__(self, name: Incomplete | None = None, **kw) -> None: ...
    def __set__(self, instance, value) -> None: ...

class Typed(Descriptor):
    expected_type: Incomplete
    allow_none: bool
    nested: bool
    __doc__: Incomplete
    def __init__(self, *args, **kw) -> None: ...
    def __set__(self, instance, value) -> None: ...

class Convertible(Typed):
    def __set__(self, instance, value) -> None: ...

class Max(Convertible):
    expected_type = float
    allow_none: bool
    def __init__(self, **kw) -> None: ...
    def __set__(self, instance, value) -> None: ...

class Min(Convertible):
    expected_type = float
    allow_none: bool
    def __init__(self, **kw) -> None: ...
    def __set__(self, instance, value) -> None: ...

class MinMax(Min, Max): ...

class Set(Descriptor):
    __doc__: Incomplete
    def __init__(self, name: Incomplete | None = None, **kw) -> None: ...
    def __set__(self, instance, value) -> None: ...

class NoneSet(Set):
    def __init__(self, name: Incomplete | None = None, **kw) -> None: ...
    def __set__(self, instance, value) -> None: ...

class Integer(Convertible):
    expected_type = int

class Float(Convertible):
    expected_type = float

class Bool(Convertible):
    expected_type = bool
    def __set__(self, instance, value) -> None: ...

class String(Typed):
    expected_type = str

class Text(String, Convertible): ...

class ASCII(Typed):
    expected_type = bytes

class Tuple(Typed):
    expected_type = tuple

class Length(Descriptor):
    def __init__(self, name: Incomplete | None = None, **kw) -> None: ...
    def __set__(self, instance, value) -> None: ...

class Default(Typed):
    def __init__(self, name: Incomplete | None = None, **kw) -> None: ...
    def __call__(self): ...

class Alias(Descriptor):
    alias: Incomplete
    def __init__(self, alias) -> None: ...
    def __set__(self, instance, value) -> None: ...
    def __get__(self, instance, cls): ...

class MatchPattern(Descriptor):
    allow_none: bool
    test_pattern: Incomplete
    def __init__(self, name: Incomplete | None = None, **kw) -> None: ...
    def __set__(self, instance, value) -> None: ...

class DateTime(Typed):
    expected_type = datetime.datetime
    def __set__(self, instance, value) -> None: ...
