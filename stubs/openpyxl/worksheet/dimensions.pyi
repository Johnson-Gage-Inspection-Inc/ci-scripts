from _typeshed import Incomplete
from openpyxl.compat import safe_string as safe_string
from openpyxl.descriptors import Alias as Alias, Bool as Bool, Float as Float, Integer as Integer, Strict as Strict, String as String
from openpyxl.descriptors.serialisable import Serialisable as Serialisable
from openpyxl.styles.styleable import StyleableObject as StyleableObject
from openpyxl.utils import column_index_from_string as column_index_from_string, get_column_interval as get_column_interval, get_column_letter as get_column_letter, range_boundaries as range_boundaries
from openpyxl.utils.bound_dictionary import BoundDictionary as BoundDictionary
from openpyxl.utils.units import DEFAULT_COLUMN_WIDTH as DEFAULT_COLUMN_WIDTH
from openpyxl.xml.functions import Element as Element

class Dimension(Strict, StyleableObject):
    __fields__: Incomplete
    index: Incomplete
    hidden: Incomplete
    outlineLevel: Incomplete
    outline_level: Incomplete
    collapsed: Incomplete
    style: Incomplete
    def __init__(self, index, hidden, outlineLevel, collapsed, worksheet, visible: bool = True, style: Incomplete | None = None) -> None: ...
    def __iter__(self): ...
    def __copy__(self): ...

class RowDimension(Dimension):
    __fields__: Incomplete
    r: Incomplete
    s: Incomplete
    ht: Incomplete
    height: Incomplete
    thickBot: Incomplete
    thickTop: Incomplete
    def __init__(self, worksheet, index: int = 0, ht: Incomplete | None = None, customHeight: Incomplete | None = None, s: Incomplete | None = None, customFormat: Incomplete | None = None, hidden: bool = False, outlineLevel: int = 0, outline_level: Incomplete | None = None, collapsed: bool = False, visible: Incomplete | None = None, height: Incomplete | None = None, r: Incomplete | None = None, spans: Incomplete | None = None, thickBot: Incomplete | None = None, thickTop: Incomplete | None = None, **kw) -> None: ...
    @property
    def customFormat(self): ...
    @property
    def customHeight(self): ...

class ColumnDimension(Dimension):
    width: Incomplete
    bestFit: Incomplete
    auto_size: Incomplete
    index: Incomplete
    min: Incomplete
    max: Incomplete
    collapsed: Incomplete
    __fields__: Incomplete
    def __init__(self, worksheet, index: str = 'A', width=..., bestFit: bool = False, hidden: bool = False, outlineLevel: int = 0, outline_level: Incomplete | None = None, collapsed: bool = False, style: Incomplete | None = None, min: Incomplete | None = None, max: Incomplete | None = None, customWidth: bool = False, visible: Incomplete | None = None, auto_size: Incomplete | None = None) -> None: ...
    @property
    def customWidth(self): ...
    def reindex(self) -> None: ...
    @property
    def range(self): ...
    def to_tree(self): ...

class DimensionHolder(BoundDictionary):
    worksheet: Incomplete
    max_outline: Incomplete
    default_factory: Incomplete
    def __init__(self, worksheet, reference: str = 'index', default_factory: Incomplete | None = None) -> None: ...
    def group(self, start, end: Incomplete | None = None, outline_level: int = 1, hidden: bool = False) -> None: ...
    def to_tree(self): ...

class SheetFormatProperties(Serialisable):
    tagname: str
    baseColWidth: Incomplete
    defaultColWidth: Incomplete
    defaultRowHeight: Incomplete
    customHeight: Incomplete
    zeroHeight: Incomplete
    thickTop: Incomplete
    thickBottom: Incomplete
    outlineLevelRow: Incomplete
    outlineLevelCol: Incomplete
    def __init__(self, baseColWidth: int = 8, defaultColWidth: Incomplete | None = None, defaultRowHeight: int = 15, customHeight: Incomplete | None = None, zeroHeight: Incomplete | None = None, thickTop: Incomplete | None = None, thickBottom: Incomplete | None = None, outlineLevelRow: Incomplete | None = None, outlineLevelCol: Incomplete | None = None) -> None: ...

class SheetDimension(Serialisable):
    tagname: str
    ref: Incomplete
    def __init__(self, ref: Incomplete | None = None) -> None: ...
    @property
    def boundaries(self): ...
