from _typeshed import Incomplete
from collections.abc import Generator
from itertools import accumulate as accumulate
from openpyxl.compat.product import prod as prod

def dataframe_to_rows(df, index: bool = True, header: bool = True) -> Generator[Incomplete]: ...
def expand_index(index, header: bool = False) -> Generator[Incomplete]: ...
