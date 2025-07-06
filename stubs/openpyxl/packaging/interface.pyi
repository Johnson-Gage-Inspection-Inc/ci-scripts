import abc
from openpyxl.compat.abc import ABC as ABC

class ISerialisableFile(ABC, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def id(self): ...
