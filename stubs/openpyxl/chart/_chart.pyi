from .data_source import AxDataSource as AxDataSource, NumRef as NumRef
from .layout import Layout as Layout
from .legend import Legend as Legend
from .reference import Reference as Reference
from .series import attribute_mapping as attribute_mapping
from .series_factory import SeriesFactory as SeriesFactory
from .shapes import GraphicalProperties as GraphicalProperties
from .title import TitleDescriptor as TitleDescriptor
from _typeshed import Incomplete
from openpyxl.descriptors import Alias as Alias, Bool as Bool, Integer as Integer, MinMax as MinMax, Set as Set, Typed as Typed
from openpyxl.descriptors.sequence import ValueSequence as ValueSequence
from openpyxl.descriptors.serialisable import Serialisable as Serialisable

class AxId(Serialisable):
    val: Incomplete
    def __init__(self, val) -> None: ...

def PlotArea(): ...

class ChartBase(Serialisable):
    legend: Incomplete
    layout: Incomplete
    roundedCorners: Incomplete
    axId: Incomplete
    visible_cells_only: Incomplete
    display_blanks: Incomplete
    graphical_properties: Incomplete
    ser: Incomplete
    series: Incomplete
    title: Incomplete
    anchor: str
    width: int
    height: float
    style: Incomplete
    mime_type: str
    __elements__: Incomplete
    plot_area: Incomplete
    pivotSource: Incomplete
    pivotFormats: Incomplete
    idx_base: int
    def __init__(self, axId=(), **kw) -> None: ...
    def __hash__(self): ...
    def __iadd__(self, other): ...
    def to_tree(self, namespace: Incomplete | None = None, tagname: Incomplete | None = None, idx: Incomplete | None = None): ...
    def set_categories(self, labels) -> None: ...
    def add_data(self, data, from_rows: bool = False, titles_from_data: bool = False) -> None: ...
    def append(self, value) -> None: ...
    @property
    def path(self): ...
