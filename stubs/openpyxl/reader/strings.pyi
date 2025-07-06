from openpyxl.cell.rich_text import CellRichText as CellRichText
from openpyxl.cell.text import Text as Text
from openpyxl.xml.constants import SHEET_MAIN_NS as SHEET_MAIN_NS
from openpyxl.xml.functions import iterparse as iterparse

def read_string_table(xml_source): ...
def read_rich_text(xml_source): ...
