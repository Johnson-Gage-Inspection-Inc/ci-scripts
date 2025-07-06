from .cell_range import CellRange as CellRange
from _typeshed import Incomplete
from openpyxl.cell.cell import MergedCell as MergedCell
from openpyxl.descriptors import Integer as Integer, Sequence as Sequence
from openpyxl.descriptors.serialisable import Serialisable as Serialisable
from openpyxl.styles.borders import Border as Border

class MergeCell(CellRange):
    tagname: str
    ref: Incomplete
    __attrs__: Incomplete
    def __init__(self, ref: Incomplete | None = None) -> None: ...
    def __copy__(self): ...

class MergeCells(Serialisable):
    tagname: str
    count: Incomplete
    mergeCell: Incomplete
    __elements__: Incomplete
    __attrs__: Incomplete
    def __init__(self, count: Incomplete | None = None, mergeCell=()) -> None: ...
    @property
    def count(self): ...

class MergedCellRange(CellRange):
    ws: Incomplete
    start_cell: Incomplete
    def __init__(self, worksheet, coord) -> None: ...
    def format(self) -> None: ...
    def __contains__(self, coord) -> bool: ...
    def __copy__(self): ...
