from ._writer import WorksheetWriter as WorksheetWriter
from .worksheet import Worksheet as Worksheet
from _typeshed import Incomplete
from openpyxl.cell import Cell as Cell, WriteOnlyCell as WriteOnlyCell
from openpyxl.utils.exceptions import WorkbookAlreadySaved as WorkbookAlreadySaved
from openpyxl.workbook.child import _WorkbookChild

class WriteOnlyWorksheet(_WorkbookChild):
    mime_type: Incomplete
    add_chart: Incomplete
    add_image: Incomplete
    add_table: Incomplete
    tables: Incomplete
    print_titles: Incomplete
    print_title_cols: Incomplete
    print_title_rows: Incomplete
    freeze_panes: Incomplete
    print_area: Incomplete
    sheet_view: Incomplete
    def __init__(self, parent, title) -> None: ...
    @property
    def closed(self): ...
    def close(self) -> None: ...
    def append(self, row) -> None: ...
