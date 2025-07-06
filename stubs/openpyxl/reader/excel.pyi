from ..tests import KEEP_VBA as KEEP_VBA
from .drawings import find_images as find_images
from .strings import read_rich_text as read_rich_text, read_string_table as read_string_table
from .workbook import WorkbookParser as WorkbookParser
from _typeshed import Incomplete
from openpyxl.cell import MergedCell as MergedCell
from openpyxl.chartsheet import Chartsheet as Chartsheet
from openpyxl.comments.comment_sheet import CommentSheet as CommentSheet
from openpyxl.drawing.spreadsheet_drawing import SpreadsheetDrawing as SpreadsheetDrawing
from openpyxl.packaging.core import DocumentProperties as DocumentProperties
from openpyxl.packaging.custom import CustomPropertyList as CustomPropertyList
from openpyxl.packaging.manifest import Manifest as Manifest, Override as Override
from openpyxl.packaging.relationship import RelationshipList as RelationshipList, get_dependents as get_dependents, get_rels_path as get_rels_path
from openpyxl.pivot.table import TableDefinition as TableDefinition
from openpyxl.styles.stylesheet import apply_stylesheet as apply_stylesheet
from openpyxl.utils.exceptions import InvalidFileException as InvalidFileException
from openpyxl.worksheet._read_only import ReadOnlyWorksheet as ReadOnlyWorksheet
from openpyxl.worksheet._reader import WorksheetReader as WorksheetReader
from openpyxl.worksheet.table import Table as Table
from openpyxl.xml.constants import ARC_CONTENT_TYPES as ARC_CONTENT_TYPES, ARC_CORE as ARC_CORE, ARC_CUSTOM as ARC_CUSTOM, ARC_THEME as ARC_THEME, ARC_WORKBOOK as ARC_WORKBOOK, COMMENTS_NS as COMMENTS_NS, SHARED_STRINGS as SHARED_STRINGS, XLSM as XLSM, XLSX as XLSX, XLTM as XLTM, XLTX as XLTX
from openpyxl.xml.functions import fromstring as fromstring

SUPPORTED_FORMATS: Incomplete

class ExcelReader:
    archive: Incomplete
    valid_files: Incomplete
    read_only: Incomplete
    keep_vba: Incomplete
    data_only: Incomplete
    keep_links: Incomplete
    rich_text: Incomplete
    shared_strings: Incomplete
    def __init__(self, fn, read_only: bool = False, keep_vba=..., data_only: bool = False, keep_links: bool = True, rich_text: bool = False) -> None: ...
    package: Incomplete
    def read_manifest(self) -> None: ...
    def read_strings(self) -> None: ...
    parser: Incomplete
    wb: Incomplete
    def read_workbook(self) -> None: ...
    def read_properties(self) -> None: ...
    def read_custom(self) -> None: ...
    def read_theme(self) -> None: ...
    def read_chartsheet(self, sheet, rel) -> None: ...
    def read_worksheets(self) -> None: ...
    def read(self) -> None: ...

def load_workbook(filename, read_only: bool = False, keep_vba=..., data_only: bool = False, keep_links: bool = True, rich_text: bool = False): ...
