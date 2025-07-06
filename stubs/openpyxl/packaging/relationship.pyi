from _typeshed import Incomplete
from collections.abc import Generator
from openpyxl.descriptors import Alias as Alias, Sequence as Sequence, String as String
from openpyxl.descriptors.container import ElementList as ElementList
from openpyxl.descriptors.serialisable import Serialisable as Serialisable
from openpyxl.xml.constants import PKG_REL_NS as PKG_REL_NS, REL_NS as REL_NS
from openpyxl.xml.functions import Element as Element, fromstring as fromstring

class Relationship(Serialisable):
    tagname: str
    Type: Incomplete
    Target: Incomplete
    target: Incomplete
    TargetMode: Incomplete
    Id: Incomplete
    id: Incomplete
    def __init__(self, Id: Incomplete | None = None, Type: Incomplete | None = None, type: Incomplete | None = None, Target: Incomplete | None = None, TargetMode: Incomplete | None = None) -> None: ...

class RelationshipList(ElementList):
    tagname: str
    expected_type = Relationship
    def append(self, value) -> None: ...
    def find(self, content_type) -> Generator[Incomplete]: ...
    def get(self, key): ...
    def to_dict(self): ...
    def to_tree(self): ...

def get_rels_path(path): ...
def get_dependents(archive, filename): ...
def get_rel(archive, deps, id: Incomplete | None = None, cls: Incomplete | None = None): ...
