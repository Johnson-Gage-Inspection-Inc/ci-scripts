from .alignment import Alignment as Alignment
from .borders import Border as Border
from .cell_style import CellStyle as CellStyle, StyleArray as StyleArray
from .fills import Fill as Fill, PatternFill as PatternFill
from .fonts import Font as Font
from .numbers import BUILTIN_FORMATS_MAX_SIZE as BUILTIN_FORMATS_MAX_SIZE, BUILTIN_FORMATS_REVERSE as BUILTIN_FORMATS_REVERSE, NumberFormatDescriptor as NumberFormatDescriptor
from .protection import Protection as Protection
from _typeshed import Incomplete
from openpyxl.compat import safe_string as safe_string
from openpyxl.descriptors import Bool as Bool, Integer as Integer, Sequence as Sequence, String as String, Typed as Typed
from openpyxl.descriptors.excel import ExtensionList as ExtensionList
from openpyxl.descriptors.serialisable import Serialisable as Serialisable

class NamedStyle(Serialisable):
    font: Incomplete
    fill: Incomplete
    border: Incomplete
    alignment: Incomplete
    number_format: Incomplete
    protection: Incomplete
    builtinId: Incomplete
    hidden: Incomplete
    name: Incomplete
    def __init__(self, name: str = 'Normal', font: Incomplete | None = None, fill: Incomplete | None = None, border: Incomplete | None = None, alignment: Incomplete | None = None, number_format: Incomplete | None = None, protection: Incomplete | None = None, builtinId: Incomplete | None = None, hidden: bool = False) -> None: ...
    def __setattr__(self, attr, value) -> None: ...
    def __iter__(self): ...
    def bind(self, wb) -> None: ...
    def as_tuple(self): ...
    def as_xf(self): ...
    def as_name(self): ...

class NamedStyleList(list):
    def __init__(self, iterable=()) -> None: ...
    @property
    def names(self): ...
    def __getitem__(self, key): ...
    def append(self, style) -> None: ...

class _NamedCellStyle(Serialisable):
    tagname: str
    name: Incomplete
    xfId: Incomplete
    builtinId: Incomplete
    iLevel: Incomplete
    hidden: Incomplete
    customBuiltin: Incomplete
    extLst: Incomplete
    __elements__: Incomplete
    def __init__(self, name: Incomplete | None = None, xfId: Incomplete | None = None, builtinId: Incomplete | None = None, iLevel: Incomplete | None = None, hidden: Incomplete | None = None, customBuiltin: Incomplete | None = None, extLst: Incomplete | None = None) -> None: ...

class _NamedCellStyleList(Serialisable):
    tagname: str
    count: Incomplete
    cellStyle: Incomplete
    __attrs__: Incomplete
    def __init__(self, count: Incomplete | None = None, cellStyle=()) -> None: ...
    @property
    def count(self): ...
    def remove_duplicates(self): ...
