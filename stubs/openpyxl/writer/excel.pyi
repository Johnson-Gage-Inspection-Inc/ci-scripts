from .theme import theme_xml as theme_xml
from _typeshed import Incomplete
from openpyxl.comments.comment_sheet import CommentSheet as CommentSheet
from openpyxl.drawing.spreadsheet_drawing import SpreadsheetDrawing as SpreadsheetDrawing
from openpyxl.packaging.manifest import Manifest as Manifest
from openpyxl.packaging.relationship import Relationship as Relationship, RelationshipList as RelationshipList, get_rels_path as get_rels_path
from openpyxl.styles.stylesheet import write_stylesheet as write_stylesheet
from openpyxl.utils.exceptions import InvalidFileException as InvalidFileException
from openpyxl.workbook._writer import WorkbookWriter as WorkbookWriter
from openpyxl.worksheet._writer import WorksheetWriter as WorksheetWriter
from openpyxl.xml.constants import ARC_APP as ARC_APP, ARC_CORE as ARC_CORE, ARC_CUSTOM as ARC_CUSTOM, ARC_ROOT_RELS as ARC_ROOT_RELS, ARC_STYLE as ARC_STYLE, ARC_THEME as ARC_THEME, ARC_WORKBOOK as ARC_WORKBOOK, ARC_WORKBOOK_RELS as ARC_WORKBOOK_RELS, CPROPS_TYPE as CPROPS_TYPE
from openpyxl.xml.functions import fromstring as fromstring, tostring as tostring

class ExcelWriter:
    workbook: Incomplete
    manifest: Incomplete
    vba_modified: Incomplete
    def __init__(self, workbook, archive) -> None: ...
    def write_data(self) -> None: ...
    def write_worksheet(self, ws) -> None: ...
    def save(self) -> None: ...

def save_workbook(workbook, filename): ...
