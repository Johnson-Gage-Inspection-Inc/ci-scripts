from _typeshed import Incomplete
from openpyxl.descriptors import Bool as Bool
from openpyxl.descriptors.serialisable import Serialisable as Serialisable

class Protection(Serialisable):
    tagname: str
    locked: Incomplete
    hidden: Incomplete
    def __init__(self, locked: bool = True, hidden: bool = False) -> None: ...
