from _typeshed import Incomplete
from openpyxl.descriptors import Alias as Alias, Bool as Bool, DateTime as DateTime, Float as Float, Integer as Integer, MinMax as MinMax, NoneSet as NoneSet, Sequence as Sequence, Set as Set, String as String, Typed as Typed
from openpyxl.descriptors.excel import CellRange as CellRange, ExtensionList as ExtensionList
from openpyxl.descriptors.sequence import ValueSequence as ValueSequence
from openpyxl.descriptors.serialisable import Serialisable as Serialisable
from openpyxl.utils import absolute_coordinate as absolute_coordinate

class SortCondition(Serialisable):
    tagname: str
    descending: Incomplete
    sortBy: Incomplete
    ref: Incomplete
    customList: Incomplete
    dxfId: Incomplete
    iconSet: Incomplete
    iconId: Incomplete
    def __init__(self, ref: Incomplete | None = None, descending: Incomplete | None = None, sortBy: Incomplete | None = None, customList: Incomplete | None = None, dxfId: Incomplete | None = None, iconSet: Incomplete | None = None, iconId: Incomplete | None = None) -> None: ...

class SortState(Serialisable):
    tagname: str
    columnSort: Incomplete
    caseSensitive: Incomplete
    sortMethod: Incomplete
    ref: Incomplete
    sortCondition: Incomplete
    extLst: Incomplete
    __elements__: Incomplete
    def __init__(self, columnSort: Incomplete | None = None, caseSensitive: Incomplete | None = None, sortMethod: Incomplete | None = None, ref: Incomplete | None = None, sortCondition=(), extLst: Incomplete | None = None) -> None: ...
    def __bool__(self) -> bool: ...

class IconFilter(Serialisable):
    tagname: str
    iconSet: Incomplete
    iconId: Incomplete
    def __init__(self, iconSet: Incomplete | None = None, iconId: Incomplete | None = None) -> None: ...

class ColorFilter(Serialisable):
    tagname: str
    dxfId: Incomplete
    cellColor: Incomplete
    def __init__(self, dxfId: Incomplete | None = None, cellColor: Incomplete | None = None) -> None: ...

class DynamicFilter(Serialisable):
    tagname: str
    type: Incomplete
    val: Incomplete
    valIso: Incomplete
    maxVal: Incomplete
    maxValIso: Incomplete
    def __init__(self, type: Incomplete | None = None, val: Incomplete | None = None, valIso: Incomplete | None = None, maxVal: Incomplete | None = None, maxValIso: Incomplete | None = None) -> None: ...

class CustomFilter(Serialisable):
    tagname: str
    val: Incomplete
    operator: Incomplete
    def __init__(self, operator: str = 'equal', val: Incomplete | None = None) -> None: ...
    def convert(self): ...

class BlankFilter(CustomFilter):
    __attrs__: Incomplete
    def __init__(self, **kw) -> None: ...
    @property
    def operator(self): ...
    @property
    def val(self): ...

class NumberFilter(CustomFilter):
    operator: Incomplete
    val: Incomplete
    def __init__(self, operator: str = 'equal', val: Incomplete | None = None) -> None: ...

string_format_mapping: Incomplete

class StringFilter(CustomFilter):
    operator: Incomplete
    val: Incomplete
    exclude: Incomplete
    def __init__(self, operator: str = 'contains', val: Incomplete | None = None, exclude: bool = False) -> None: ...
    def to_tree(self, tagname: Incomplete | None = None, idx: Incomplete | None = None, namespace: Incomplete | None = None): ...

class CustomFilters(Serialisable):
    tagname: str
    customFilter: Incomplete
    __elements__: Incomplete
    def __init__(self, _and: Incomplete | None = None, customFilter=()) -> None: ...

class Top10(Serialisable):
    tagname: str
    top: Incomplete
    percent: Incomplete
    val: Incomplete
    filterVal: Incomplete
    def __init__(self, top: Incomplete | None = None, percent: Incomplete | None = None, val: Incomplete | None = None, filterVal: Incomplete | None = None) -> None: ...

class DateGroupItem(Serialisable):
    tagname: str
    year: Incomplete
    month: Incomplete
    day: Incomplete
    hour: Incomplete
    minute: Incomplete
    second: Incomplete
    dateTimeGrouping: Incomplete
    def __init__(self, year: Incomplete | None = None, month: Incomplete | None = None, day: Incomplete | None = None, hour: Incomplete | None = None, minute: Incomplete | None = None, second: Incomplete | None = None, dateTimeGrouping: Incomplete | None = None) -> None: ...

class Filters(Serialisable):
    tagname: str
    blank: Incomplete
    calendarType: Incomplete
    filter: Incomplete
    dateGroupItem: Incomplete
    __elements__: Incomplete
    def __init__(self, blank: Incomplete | None = None, calendarType: Incomplete | None = None, filter=(), dateGroupItem=()) -> None: ...

class FilterColumn(Serialisable):
    tagname: str
    colId: Incomplete
    col_id: Incomplete
    hiddenButton: Incomplete
    showButton: Incomplete
    filters: Incomplete
    top10: Incomplete
    customFilters: Incomplete
    dynamicFilter: Incomplete
    colorFilter: Incomplete
    iconFilter: Incomplete
    extLst: Incomplete
    __elements__: Incomplete
    def __init__(self, colId: Incomplete | None = None, hiddenButton: bool = False, showButton: bool = True, filters: Incomplete | None = None, top10: Incomplete | None = None, customFilters: Incomplete | None = None, dynamicFilter: Incomplete | None = None, colorFilter: Incomplete | None = None, iconFilter: Incomplete | None = None, extLst: Incomplete | None = None, blank: Incomplete | None = None, vals: Incomplete | None = None) -> None: ...

class AutoFilter(Serialisable):
    tagname: str
    ref: Incomplete
    filterColumn: Incomplete
    sortState: Incomplete
    extLst: Incomplete
    __elements__: Incomplete
    def __init__(self, ref: Incomplete | None = None, filterColumn=(), sortState: Incomplete | None = None, extLst: Incomplete | None = None) -> None: ...
    def __bool__(self) -> bool: ...
    def add_filter_column(self, col_id, vals, blank: bool = False) -> None: ...
    def add_sort_condition(self, ref, descending: bool = False) -> None: ...
